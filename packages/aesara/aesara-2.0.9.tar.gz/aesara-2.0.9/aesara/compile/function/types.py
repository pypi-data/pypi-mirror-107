"""
Driver of graph construction, optimization, and linking.

"""

import copy
import copyreg
import logging
import os
import pickle
import time
import warnings
from itertools import chain
from typing import List

import numpy as np

import aesara
import aesara.compile.profiling
from aesara.compile.compilelock import lock_ctx
from aesara.compile.io import In, SymbolicInput, SymbolicOutput
from aesara.compile.ops import deep_copy_op, view_op
from aesara.configdefaults import config
from aesara.graph.basic import (
    Constant,
    Variable,
    ancestors,
    clone_get_equiv,
    graph_inputs,
    vars_between,
)
from aesara.graph.destroyhandler import DestroyHandler
from aesara.graph.features import PreserveVariableAttributes
from aesara.graph.fg import FunctionGraph, InconsistencyError
from aesara.graph.op import ops_with_inner_function
from aesara.graph.opt_utils import is_same_graph
from aesara.graph.utils import get_variable_trace_string
from aesara.link.basic import Container
from aesara.link.utils import raise_with_op


_logger = logging.getLogger("aesara.compile.function.types")

__docformat__ = "restructuredtext en"


class UnusedInputError(Exception):
    """
    A symbolic input passed to function is not needed.

    """


def alias_root(v):
    """
    Return the variable to which v is aliased by view_maps and destroy_maps.

    """
    if v.owner is None:
        return v
    vmap = v.owner.op.view_map
    dmap = v.owner.op.destroy_map
    outpos = v.owner.outputs.index(v)
    v_views = vmap.get(outpos, []) + dmap.get(outpos, [])
    if len(v_views) > 1:
        raise NotImplementedError(
            str(v) + " is a view/destroyed version of more then one inputs. "
            "Currently, we only support the case where an output is a view or "
            "a destroyed version of one input."
        )
    elif v_views:
        return alias_root(v.owner.inputs[v_views[0]])
    else:
        return v


def view_tree_set(fgraph, v, treeset):
    """
    Add to `treeset` all variables that are views of v, given that v is
    not a view.

    """
    treeset.add(v)
    for cl, v_input_pos_to_cl in fgraph.clients[v]:
        if cl == "output":
            continue
        vmap = cl.op.view_map
        dmap = cl.op.destroy_map
        for opos, iposlist in chain(vmap.items(), dmap.items()):
            if v_input_pos_to_cl in iposlist:
                if cl.outputs[opos] not in treeset:
                    view_tree_set(fgraph, cl.outputs[opos], treeset)


def infer_reuse_pattern(fgraph, outputs_to_disown):
    """
    Given an fgraph and a list of variables, returns the list or set
    of all variables which may share the same underlying data storage
    as any of the specified variables. Used internally by function,
    FunctionMaker.

    This list (or set) is also referred to as no_recycling sometimes,
    especially by linker code.

    """
    rval = set()
    for o in outputs_to_disown:
        view_tree_set(fgraph, alias_root(o), rval)
    # remove from rval all of the inputs, constants, values.
    rval = {r for r in rval if r.owner is not None}

    return rval


def fgraph_updated_vars(fgraph, expanded_inputs):
    """
    Reconstruct the full "updates" dictionary, mapping from FunctionGraph input
    variables to the fgraph outputs that will replace their values.

    Returns
    -------
    dict variable -> variable

    """
    updated_vars = {}
    potential_values = list(fgraph.outputs)  # copy the list
    if len(expanded_inputs) != len(fgraph.inputs):
        raise ValueError("expanded_inputs must match len(fgraph.inputs)")
    for e_input, ivar in reversed(list(zip(expanded_inputs, fgraph.inputs))):
        if e_input.update is not None:
            updated_vars[ivar] = potential_values.pop()
    return updated_vars


class Supervisor:
    """
    Listener for FunctionGraph events which makes sure that no
    operation overwrites the contents of protected Variables. The
    outputs of the FunctionGraph are protected by default.

    """

    def __init__(self, protected):
        self.protected = list(protected)

    def validate(self, fgraph):
        if config.cycle_detection == "fast" and hasattr(fgraph, "has_destroyers"):
            if fgraph.has_destroyers(self.protected):
                raise InconsistencyError("Trying to destroy a protected" "Variable.")
            return True
        if not hasattr(fgraph, "destroyers"):
            return True
        for r in self.protected + list(fgraph.outputs):
            if fgraph.destroyers(r):
                raise InconsistencyError("Trying to destroy a protected" "Variable.", r)


def std_fgraph(input_specs, output_specs, accept_inplace=False):
    """
    Makes an FunctionGraph corresponding to the input specs and the output
    specs.  Any SymbolicInput in the input_specs, if its update field
    is not None, will add an output to the FunctionGraph corresponding to that
    update. The return value is the FunctionGraph as well as a list of
    SymbolicOutput instances corresponding to the updates.

    If accept_inplace is False, the graph will be checked for inplace
    operations and an exception will be raised if it has any. If
    accept_inplace is True, a DestroyHandler will be added to the FunctionGraph
    if there are any inplace operations.

    The returned FunctionGraph is a clone of the graph between the provided
    inputs and outputs.

    """
    orig_inputs = [spec.variable for spec in input_specs]

    # Extract the updates and the mapping between update outputs and
    # the updated inputs.
    updates = []
    update_mapping = {}
    out_idx = len(output_specs)
    for inp_idx in range(len(input_specs)):
        if input_specs[inp_idx].update:
            updates.append(input_specs[inp_idx].update)
            update_mapping[out_idx] = inp_idx
            out_idx += 1

    orig_outputs = [spec.variable for spec in output_specs] + updates

    fgraph = FunctionGraph(orig_inputs, orig_outputs, update_mapping=update_mapping)

    for node in fgraph.apply_nodes:
        if node.op.destroy_map:
            if not accept_inplace:
                raise TypeError(
                    "Graph must not contain inplace operations", node, node.op
                )
            else:
                fgraph.attach_feature(DestroyHandler())
                break

    # We need to protect all immutable inputs from inplace operations.
    fgraph.attach_feature(
        Supervisor(
            input
            for spec, input in zip(input_specs, fgraph.inputs)
            if not (
                spec.mutable
                or (hasattr(fgraph, "destroyers") and fgraph.has_destroyers([input]))
            )
        )
    )

    # If named nodes are replaced, keep the name
    for feature in std_fgraph.features:
        fgraph.attach_feature(feature())
    return fgraph, list(map(SymbolicOutput, updates))


std_fgraph.features = [PreserveVariableAttributes]


class AliasedMemoryError(Exception):
    """
    Memory is aliased that should not be.

    """


###
# Function
###

# unique id object used as a placeholder for duplicate entries
DUPLICATE = ["DUPLICATE"]


class Function:
    """
    Type of the functions returned by aesara.function or
    aesara.FunctionMaker.create.

    `Function` is the callable object that does computation.  It has the storage
    of inputs and outputs, performs the packing and unpacking of inputs and
    return values. It implements the square-bracket indexing so that you can
    look up the value of a symbolic node.

    Functions are copyable via {{{fn.copy()}}} and {{{copy.copy(fn)}}}.
    When a function is copied, this instance is duplicated. Contrast with
    self.maker (instance of `FunctionMaker`) that is shared between copies.
    The meaning of copying a function is that the containers and their current
    values will all be duplicated. This requires that mutable inputs be
    copied, whereas immutable inputs may be shared between copies.

    A Function instance is hashable, on the basis of its memory
    address (its id).

    A Function instance is only equal to itself.

    A Function instance may be serialized using the `pickle` or
    `cPickle` modules.  This will save all default inputs, the graph,
    and WRITEME to the pickle file.

    A Function instance have a ``trust_input`` field that default to
    False. When True, we don't do extra check of the input to give
    better error message. In some case, python code will still return
    the good results if you pass a python or numpy scalar instead of a
    numpy tensor.  C code should raise an error if you pass an object
    of the wrong type.

    Attributes
    ----------
    finder
    inv_finder

    """

    pickle_aliased_memory_strategy = "warn"
    """
    How to deal with pickling finding aliased storage.

    Meaningful settings are: 'ignore', 'warn', 'raise'.

    If the value is 'warn', then a message will be printed to stderr
    if aliased storage is dectected during pickle.dump.

    If the value is 'raise', then an AliasedMemoryError will be raised
    if aliased storage is detected during pickle.dump.

    """

    input_storage = None
    """
    List of Container instances.

    """

    output_storage = None
    """
    List of Container instances.

    """

    indices = None
    """
    List of (SymbolicInput, indices, [SymbolicInput,...]),
    one tuple for each input.

    The first tuple element is the SymbolicInput object for the corresponding
    function input.

    The second and third tuple elements are used only by Kits, which
    are deprecated.

    """

    defaults = None
    """
    List of 3-tuples, one 3-tuple for each input.

    Tuple element 0: Bool:  Is this input required at each function call?
    Tuple element 1: Bool: Should this inputs value be reverted after
        each call?
    Tuple element 2: Any:  The value associated with this input.

    """

    unpack_single = None
    """
    Bool: for outputs lists of length 1, should the 0'th element be
    returned directly?

    """

    return_none = None
    """
    Bool: whether the function should return None or not.

    """

    maker = None
    """
    FunctionMaker instance.

    """

    fn = None
    """
    A function that evaluates the graph. Typically a linker's make_thunk method
    created this function.

    """

    finder = None
    """
    Dictionary mapping several kinds of things to containers.

    We set an entry in finder for:

    - the index of the input

    - the variable instance the input is based on

    - the name of the input

    All entries map to the container or to DUPLICATE if an ambiguity
    is detected.

    """

    inv_finder = None
    """
    Dict. Reverse lookup of `finder`.

    It maps container -> SymbolicInput

    """

    def __init__(
        self,
        fn,
        input_storage,
        output_storage,
        indices,
        outputs,
        defaults,
        unpack_single,
        return_none,
        output_keys,
        maker,
        name=None,
    ):
        self.fn = fn
        self.input_storage = input_storage
        self.output_storage = output_storage
        self.indices = indices
        self.outputs = outputs
        self.defaults = defaults
        self.unpack_single = unpack_single
        self.return_none = return_none
        self.maker = maker
        self.profile = None  # reassigned in FunctionMaker.create
        self.trust_input = False  # If True, we don't check the input parameter
        self.name = name
        self.nodes_with_inner_function = []
        self.output_keys = output_keys

        # See if we have any mutable / borrow inputs
        # TODO: this only need to be set if there is more then 1 input
        self._check_for_aliased_inputs = False
        for i in maker.inputs:
            # If the input is a shared variable, the memory region is
            # under Aesara control and so we don't need to check if it
            # is aliased as we never do that.
            if (
                isinstance(i, In)
                and not i.shared
                and (getattr(i, "borrow", False) or getattr(i, "mutable", False))
            ):
                self._check_for_aliased_inputs = True
                break

        # We will be popping stuff off this `containers` object.  It is a copy.
        containers = list(self.input_storage)
        finder = {}
        inv_finder = {}

        def distribute(indices, cs, value):
            input.distribute(value, indices, cs)
            for c in cs:
                c.provided += 1

        # Store the list of names of named inputs.
        named_inputs = []
        # Count the number of un-named inputs.
        n_unnamed_inputs = 0

        # Initialize the storage
        # this loop works by modifying the elements (as variable c) of
        # self.input_storage inplace.
        for i, ((input, indices, sinputs), (required, refeed, value)) in enumerate(
            zip(self.indices, defaults)
        ):
            if indices is None:
                # containers is being used as a stack. Here we pop off
                # the next one.
                c = containers[0]
                c.strict = getattr(input, "strict", False)
                c.allow_downcast = getattr(input, "allow_downcast", None)

                if value is not None:
                    # Always initialize the storage.
                    if isinstance(value, Container):
                        # There is no point in obtaining the current value
                        # stored in the container, since the container is
                        # shared.
                        # For safety, we make sure 'refeed' is False, since
                        # there is no need to refeed the defaullt value.
                        assert not refeed
                    else:
                        c.value = value
                c.required = required
                c.implicit = input.implicit
                # this is a count of how many times the input has been
                # provided (reinitialized to 0 on __call__)
                c.provided = 0
                finder[i] = c
                finder[input.variable] = c
                if input.name not in finder:
                    finder[input.name] = c
                else:
                    finder[input.name] = DUPLICATE
                if input.name is None:
                    n_unnamed_inputs += 1
                else:
                    named_inputs.append(input.name)
                inv_finder[c] = input
                containers[:1] = []

        self.finder = finder
        self.inv_finder = inv_finder

        # this class is important in overriding the square-bracket notation:
        #     fn.value[x]
        # self reference is available via the closure on the class
        class ValueAttribute:
            def __getitem__(self, item):
                try:
                    s = finder[item]
                except KeyError:
                    raise TypeError(f"Unknown input or state: {item}")
                if s is DUPLICATE:
                    raise TypeError(
                        f"Ambiguous name: {item} - please check the "
                        "names of the inputs of your function "
                        "for duplicates."
                    )
                if isinstance(s, Container):
                    return s.value
                else:
                    raise NotImplementedError

            def __setitem__(self, item, value):
                try:
                    s = finder[item]
                except KeyError:
                    # Print informative error message.
                    msg = get_info_on_inputs(named_inputs, n_unnamed_inputs)
                    raise TypeError(f"Unknown input or state: {item}. {msg}")
                if s is DUPLICATE:
                    raise TypeError(
                        f"Ambiguous name: {item} - please check the "
                        "names of the inputs of your function "
                        "for duplicates."
                    )
                if isinstance(s, Container):
                    s.value = value
                    s.provided += 1
                else:
                    s(value)

            def __contains__(self, item):
                return finder.__contains__(item)

        # this class is important in overriding the square-bracket notation:
        #     fn.container[x]
        # self reference is available via the closure on the class
        class ContainerAttribute:
            def __getitem__(self, item):
                return finder[item]

            def __contains__(self, item):
                return finder.__contains__(item)

            # You cannot set the container

        self._value = ValueAttribute()
        self._container = ContainerAttribute()

        # Compute self.n_returned_outputs.
        # This is used only when fn.need_update_inputs is False
        # because we're using one of the VM objects and it is
        # putting updates back into the input containers all by itself.
        assert len(self.maker.expanded_inputs) == len(self.input_storage)
        self.n_returned_outputs = len(self.output_storage)
        for input in self.maker.expanded_inputs:
            if input.update is not None:
                self.n_returned_outputs -= 1

        for node in self.maker.fgraph.apply_nodes:
            if node.op in ops_with_inner_function:
                self.nodes_with_inner_function.append(node.op)

    def __contains__(self, item):
        return self.value.__contains__(item)

    def __getitem__(self, item):
        return self.value[item]

    def __setitem__(self, item, value):
        self.value[item] = value

    def __copy__(self):
        """
        Copy a function. Copied function have separate intermediate
        storages and output storages with original function
        """
        return self.copy()

    def copy(
        self,
        share_memory=False,
        swap=None,
        delete_updates=False,
        name=None,
        profile=None,
    ):
        """
        Copy this function. Copied function will have separated maker and
        fgraph with original function. User can choose whether to separate
        storage by changing the share_memory arguments.

        Parameters
        ----------
        share_memory : boolean
            When True, two function share intermediate storages(storages except input and
            output storages). Otherwise two functions will only share partial
            storages and same maker. If two functions share memory and
            allow_gc=False, this will increase executing speed and save memory.

        swap : dict
            Dictionary that map old SharedVariables to new
            SharedVariables. Default is None.
            NOTE: The shared variable swap in only done in the new returned
            function, not in the user graph.

        delete_updates : boolean
            If True, Copied function will not have updates.
        name : string
            If provided, will be the name of the new
            Function. Otherwise, it will be old + " copy"

        profile :
            as aesara.function profile parameter

        Returns
        -------
        aesara.Function
            Copied aesara.Function
        """
        # helper function
        def checkSV(sv_ori, sv_rpl):
            """
            Assert two SharedVariable follow some restirctions:
                1. same type
                2. same shape or dim?
            """
            SharedVariable = aesara.tensor.sharedvar.SharedVariable
            assert isinstance(sv_ori, SharedVariable), (
                "Key of swap should be SharedVariable, given:",
                sv_ori,
                " type",
                type(sv_ori),
            )
            assert isinstance(sv_rpl, SharedVariable), (
                "Value of swap should be SharedVariable, given:",
                sv_rpl,
                "type",
                type(sv_ori),
            )
            assert sv_ori.type == sv_rpl.type, (
                "Type of given SharedVariable conflicts with original one",
                "Type of given SharedVariable:",
                sv_rpl.type,
                "Type of original SharedVariable:",
                sv_ori.type,
            )

        maker = self.maker

        # Copy Ins and their storage.
        # so that they have different storage as their value
        ins = [copy.copy(input) for input in maker.inputs]

        # Delete update output in fgraph and updates In instances if needed
        if delete_updates:
            # The first len(maker.outputs) variables are original variables.
            # The rest are the updates.
            out_vars = maker.fgraph.outputs[: len(maker.outputs)]
        else:
            out_vars = maker.fgraph.outputs

        # Init new fgraph using copied variables and get memo
        # memo: a dict that map old variables to new variables
        memo = clone_get_equiv(maker.fgraph.inputs, out_vars)
        fg_cpy = FunctionGraph(
            [memo[i] for i in maker.fgraph.inputs],
            [memo[o] for o in out_vars],
            clone=False,
        )

        # Re initialize Outs and swap update and variable in Ins
        # By doing this, we can pass FunctionMaker._check_unused_inputs()
        outs = list(map(SymbolicOutput, fg_cpy.outputs[: len(maker.outputs)]))
        for out_ori, out_cpy in zip(maker.outputs, outs):
            out_cpy.borrow = out_ori.borrow

        # swap SharedVariable
        if swap is not None:
            exist_svs = [i.variable for i in maker.inputs]

            # Check if given ShareVariables exist
            for sv in swap.keys():
                if sv not in exist_svs:
                    raise ValueError(f"SharedVariable: {sv.name} not found")

            # Swap SharedVariable in fgraph and In instances
            for index, (i, in_v) in enumerate(zip(ins, fg_cpy.inputs)):
                # Variables in maker.inputs are defined by user, therefore we
                # use them to make comparison and do the mapping.
                # Otherwise we don't touch them.
                var = maker.inputs[index].variable

                if var in swap:
                    swap_sv = swap[var]
                    checkSV(i.variable, swap_sv)

                    # swap variable and value of In instances
                    i.variable = swap_sv
                    i.value = swap_sv.container

                    # In the fgraph we use the cloned SharedVariable
                    swap_sv = swap_sv.clone()

                    # Swap SharedVariable in fgraph
                    # if inputs was replaced, change self.inputs
                    fg_cpy.inputs[index] = swap_sv
                    fg_cpy.replace(in_v, swap_sv, reason="Swap SV")

        # Delete update if needed
        update_i = len(outs)
        for i, in_var in zip(ins, fg_cpy.inputs):
            i.variable = in_var
            if not delete_updates and i.update is not None:
                i.update = fg_cpy.outputs[update_i]
                update_i += 1
            else:
                i.update = None

        # Construct new storage_map that map new variable to old storage,
        # so that the ensuing function shares storage with the original one
        storage_map = self.fn.storage_map
        new_storage_map = {}
        # TODO: We could share the output storage, but we must make sure
        # 2 different function call won't override each other values. This
        # is already done elsewhere, so to reuse it the user would need to
        # use Out(var, borrow=True) and maybe the mutable=True flag too.
        # But to be safe for now as it isn't documented and we aren't sure
        # it is well tested, we don't share the part of the storage_map.
        if share_memory:
            i_o_vars = maker.fgraph.inputs + maker.fgraph.outputs
            for key in storage_map.keys():
                if key not in i_o_vars:
                    new_storage_map[memo[key]] = storage_map[key]

        if not name and self.name:
            name = self.name + " copy"

        input_storage = [i.value for i in ins]
        # reinitialize new maker and create new function
        if profile is None:
            profile = config.profile or config.print_global_stats
            # profile -> True or False
        if profile is True:
            if name:
                message = name
            else:
                message = str(profile.message) + " copy"
            profile = aesara.compile.profiling.ProfileStats(message=message)
            # profile -> object
        elif type(profile) == str:
            profile = aesara.compile.profiling.ProfileStats(message=profile)

        f_cpy = maker.__class__(
            inputs=ins,
            outputs=outs,
            fgraph=fg_cpy,
            mode=maker.mode,
            profile=profile,
            # When removing updates containing variables
            # not used in the output function, copy
            # generates an unused implicit input.
            # We ignore the resulting errors,
            # but could change it to 'warn' if this might
            # cause problems.
            on_unused_input="ignore",
            function_builder=maker.function_builder,
            # As this is an optimized graph, it
            # can contain inplace. DebugMode check
            # that.
            accept_inplace=True,
        ).create(input_storage, storage_map=new_storage_map)

        for in_ori, in_cpy, ori, cpy in zip(
            maker.inputs, f_cpy.maker.inputs, self.input_storage, f_cpy.input_storage
        ):

            # Share immutable ShareVariable and constant input's storage
            swapped = swap is not None and in_ori.variable in swap

            # Using the original storage if SharedVariable will not be updated
            # and is not swapped
            if not in_ori.mutable and not swapped:
                cpy.data = ori.data
                in_cpy.value = in_ori.value

            # Reconstruct Function.finder which map Variable defined by user
            # to container, to make Function.value and Function.data work well.
            # Replace variable in new maker.inputs by the original ones.
            # So that user can swap SharedVariable in a swapped function
            container = f_cpy.finder.pop(in_cpy.variable)
            if not swapped:
                f_cpy.finder[in_ori.variable] = container
                in_cpy.vairable = in_ori.variable
            else:
                f_cpy.finder[swap[in_ori.variable]] = container
                in_cpy.variable = swap[in_ori.variable]

        f_cpy.name = name
        f_cpy.maker.fgraph.name = name
        return f_cpy

    def __call__(self, *args, **kwargs):
        """
        Evaluates value of a function on given arguments.

        Parameters
        ----------
        args : list
            List of inputs to the function. All inputs are required, even when
            some of them are not necessary to calculate requested subset of
            outputs.

        kwargs : dict
            The function inputs can be passed as keyword argument. For this, use
            the name of the input or the input instance as the key.

            Keyword argument ``output_subset`` is a list of either indices of the
            function's outputs or the keys belonging to the `output_keys` dict
            and represent outputs that are requested to be calculated. Regardless
            of the presence of ``output_subset``, the updates are always calculated
            and processed. To disable the updates, you should use the ``copy``
            method with ``delete_updates=True``.

        Returns
        -------
        list
            List of outputs on indices/keys from ``output_subset`` or all of them,
            if ``output_subset`` is not passed.
        """

        def restore_defaults():
            for i, (required, refeed, value) in enumerate(self.defaults):
                if refeed:
                    if isinstance(value, Container):
                        value = value.storage[0]
                    self[i] = value

        profile = self.profile
        t0 = time.time()

        output_subset = kwargs.pop("output_subset", None)
        if output_subset is not None and self.output_keys is not None:
            output_subset = [self.output_keys.index(key) for key in output_subset]

        # Reinitialize each container's 'provided' counter
        if self.trust_input:
            i = 0
            for arg in args:
                s = self.input_storage[i]
                s.storage[0] = arg
                i += 1
        else:
            for c in self.input_storage:
                c.provided = 0

            if len(args) + len(kwargs) > len(self.input_storage):
                raise TypeError("Too many parameter passed to aesara function")

            # Set positional arguments
            i = 0
            for arg in args:
                # TODO: provide a Param option for skipping the filter if we
                #      really want speed.
                s = self.input_storage[i]
                # see this emails for a discuation about None as input
                # https://groups.google.com/group/theano-dev/browse_thread/thread/920a5e904e8a8525/4f1b311a28fc27e5
                if arg is None:
                    s.storage[0] = arg
                else:
                    try:
                        s.storage[0] = s.type.filter(
                            arg, strict=s.strict, allow_downcast=s.allow_downcast
                        )

                    except Exception as e:
                        function_name = "aesara function"
                        argument_name = "argument"
                        if self.name:
                            function_name += ' with name "' + self.name + '"'
                        if hasattr(arg, "name") and arg.name:
                            argument_name += ' with name "' + arg.name + '"'
                        where = get_variable_trace_string(self.maker.inputs[i].variable)
                        if len(e.args) == 1:
                            e.args = (
                                "Bad input "
                                + argument_name
                                + " to "
                                + function_name
                                + f" at index {int(i)} (0-based). {where}"
                                + e.args[0],
                            )
                        else:
                            e.args = (
                                "Bad input "
                                + argument_name
                                + " to "
                                + function_name
                                + f" at index {int(i)} (0-based). {where}"
                            ) + e.args
                        restore_defaults()
                        raise
                s.provided += 1
                i += 1

        # Set keyword arguments
        if kwargs:  # for speed, skip the items for empty kwargs
            for k, arg in kwargs.items():
                self[k] = arg

        if (
            not self.trust_input
            and
            # The getattr is only needed for old pickle
            getattr(self, "_check_for_aliased_inputs", True)
        ):
            # Collect aliased inputs among the storage space
            args_share_memory = []
            for i in range(len(self.input_storage)):
                i_var = self.maker.inputs[i].variable
                i_val = self.input_storage[i].storage[0]
                if hasattr(i_var.type, "may_share_memory"):
                    is_aliased = False
                    for j in range(len(args_share_memory)):

                        group_j = zip(
                            [
                                self.maker.inputs[k].variable
                                for k in args_share_memory[j]
                            ],
                            [
                                self.input_storage[k].storage[0]
                                for k in args_share_memory[j]
                            ],
                        )
                        if any(
                            [
                                (
                                    var.type is i_var.type
                                    and var.type.may_share_memory(val, i_val)
                                )
                                for (var, val) in group_j
                            ]
                        ):

                            is_aliased = True
                            args_share_memory[j].append(i)
                            break

                    if not is_aliased:
                        args_share_memory.append([i])

            # Check for groups of more than one argument that share memory
            for group in args_share_memory:
                if len(group) > 1:
                    # copy all but the first
                    for j in group[1:]:
                        self.input_storage[j].storage[0] = copy.copy(
                            self.input_storage[j].storage[0]
                        )

        # Check if inputs are missing, or if inputs were set more than once, or
        # if we tried to provide inputs that are supposed to be implicit.
        if not self.trust_input:
            for c in self.input_storage:
                if c.required and not c.provided:
                    restore_defaults()
                    raise TypeError(
                        f"Missing required input: {getattr(self.inv_finder[c], 'variable', self.inv_finder[c])}"
                    )
                if c.provided > 1:
                    restore_defaults()
                    raise TypeError(
                        f"Multiple values for input: {getattr(self.inv_finder[c], 'variable', self.inv_finder[c])}"
                    )
                if c.implicit and c.provided > 0:
                    restore_defaults()
                    raise TypeError(
                        f"Tried to provide value for implicit input: {getattr(self.inv_finder[c], 'variable', self.inv_finder[c])}"
                    )

        # Do the actual work
        t0_fn = time.time()
        try:
            outputs = (
                self.fn()
                if output_subset is None
                else self.fn(output_subset=output_subset)
            )
        except Exception:
            restore_defaults()
            if hasattr(self.fn, "position_of_error"):
                # this is a new vm-provided function or c linker
                # they need this because the exception manipulation
                # done by raise_with_op is not implemented in C.
                thunk = None
                if hasattr(self.fn, "thunks"):
                    thunk = self.fn.thunks[self.fn.position_of_error]
                raise_with_op(
                    self.maker.fgraph,
                    node=self.fn.nodes[self.fn.position_of_error],
                    thunk=thunk,
                    storage_map=getattr(self.fn, "storage_map", None),
                )
            else:
                # old-style linkers raise their own exceptions
                raise

        dt_fn = time.time() - t0_fn
        self.maker.mode.fn_time += dt_fn
        if profile:
            profile.vm_call_time += dt_fn

        # Retrieve the values that were computed
        if outputs is None:
            outputs = [x.data for x in self.output_storage]
        assert len(outputs) == len(self.output_storage)

        # Remove internal references to required inputs.
        # These cannot be re-used anyway.
        for c in self.input_storage:
            if c.required:
                c.storage[0] = None

        # if we are allowing garbage collection, remove the
        # output reference from the internal storage cells
        if getattr(self.fn, "allow_gc", False):
            assert len(self.output_storage) == len(self.maker.fgraph.outputs)
            for o_container, o_variable in zip(
                self.output_storage, self.maker.fgraph.outputs
            ):
                if o_variable.owner is not None:
                    # this node is the variable of computation
                    # WARNING: This circumvents the 'readonly' attribute in x
                    o_container.storage[0] = None

        if getattr(self.fn, "need_update_inputs", True):
            # Update the inputs that have an update function
            for input, storage in reversed(
                list(zip(self.maker.expanded_inputs, self.input_storage))
            ):
                if input.update is not None:
                    storage.data = outputs.pop()
        else:
            outputs = outputs[: self.n_returned_outputs]

        # Put default values back in the storage
        restore_defaults()
        #
        # NOTE: This logic needs to be replicated in
        #       scan.
        #       grep for 'PROFILE_CODE'
        #

        dt_call = time.time() - t0
        aesara.compile.profiling.total_fct_exec_time += dt_call
        self.maker.mode.call_time += dt_call
        if profile:
            profile.fct_callcount += 1
            profile.fct_call_time += dt_call
            if hasattr(self.fn, "update_profile"):
                self.fn.update_profile(profile)
            if profile.ignore_first_call:
                profile.reset()
                profile.ignore_first_call = False
        if self.return_none:
            return None
        elif self.unpack_single and len(outputs) == 1 and output_subset is None:
            return outputs[0]
        else:

            if self.output_keys is not None:

                assert len(self.output_keys) == len(outputs)

                if output_subset is None:
                    return dict(zip(self.output_keys, outputs))
                else:
                    return {
                        self.output_keys[index]: outputs[index]
                        for index in output_subset
                    }

            if output_subset is None:
                return outputs
            else:
                return [outputs[i] for i in output_subset]

    value = property(
        lambda self: self._value,
        None,  # this property itself is not settable
        doc="dictionary-like access to the values associated with Variables",
    )
    container = property(
        lambda self: self._container,
        None,  # this property itself is not settable
        doc=("dictionary-like access to the containers associated with " "Variables"),
    )

    def free(self):
        """
        When allow_gc = False, clear the Variables in storage_map
        """
        # 1.no allow_gc return False
        # 2.has allow_gc, if allow_gc is False, return True
        if not getattr(self.fn, "allow_gc", True):
            for key in self.fn.storage_map:
                if not isinstance(key, Constant):
                    self.fn.storage_map[key][0] = None

            for node in self.nodes_with_inner_function:
                ops_with_inner_function[node.op].free()

    def get_shared(self):
        """
        Return the shared variable read or updated by by this function.
        """
        return [i.variable for i in self.maker.inputs if i.implicit]

    def sync_shared(self):
        if hasattr(aesara, "gpuarray") and aesara.gpuarray.pygpu_activated:
            import pygpu

            for i in self.maker.fgraph.update_mapping.values():
                inp = self.input_storage[i]
                if isinstance(inp.data, pygpu.gpuarray.GpuArray):
                    inp.data.sync()


# pickling/deepcopy support for Function
def _pickle_Function(f):
    # copy of the input storage list
    ins = list(f.input_storage)
    input_storage = []

    for (input, indices, inputs), (required, refeed, default) in zip(
        f.indices, f.defaults
    ):
        input_storage.append(ins[0])
        del ins[0]

    inputs_data = [x.data for x in f.input_storage]

    # HACK to detect aliased storage.
    # This is here because aliased relationships are not [currently]
    # preserved across the pickle operation
    if not (f.pickle_aliased_memory_strategy == "ignore"):
        all_data = input_storage + inputs_data
        for i, d_i in enumerate(all_data):
            for j, d_j in enumerate(all_data):
                if (
                    (i < j)
                    and isinstance(d_i, np.ndarray)
                    and isinstance(d_j, np.ndarray)
                ):
                    if np.may_share_memory(d_i, d_j):
                        if f.pickle_aliased_memory_strategy == "warn":
                            _logger.warning(
                                "aliased relationship between "
                                f"Function arguments {d_i}, {d_j} "
                                "will not be preserved by "
                                "un-pickling operation"
                            )
                        else:
                            raise AliasedMemoryError(d_i, d_j)
    # The user can override trust_input. Our doc tell that.  We should
    # not do that anymore and make sure the Maker have all the
    # information needed.
    rval = (_constructor_Function, (f.maker, input_storage, inputs_data, f.trust_input))
    return rval


def _constructor_Function(maker, input_storage, inputs_data, trust_input=False):
    if not config.unpickle_function:
        return None

    f = maker.create(input_storage, trustme=True)
    assert len(f.input_storage) == len(inputs_data)
    for container, x in zip(f.input_storage, inputs_data):
        assert (
            (container.data is x)
            or (isinstance(x, np.ndarray) and (container.data == x).all())
            or (container.data == x)
        )
    f.trust_input = trust_input
    return f


copyreg.pickle(Function, _pickle_Function)


###
# FunctionMaker
###
def insert_deepcopy(fgraph, wrapped_inputs, wrapped_outputs):
    """
    Insert deepcopy in the fgraph to break aliasing of outputs
    """
    # This loop was inserted to remove aliasing between outputs when
    # they all evaluate to the same value. Originally it was OK for
    # outputs to be aliased, but some of the outputs can be shared
    # variables, and is not good for shared variables to be
    # aliased. It might be possible to optimize this by making sure
    # there is no aliasing only between shared variables.

    # If some outputs are constant, we add deep copy to respect the
    # memory contract

    # We don't insert deep copy when the output.borrow is True for all
    # concerned outputs.

    assert len(wrapped_inputs) == len(fgraph.inputs)
    assert len(wrapped_outputs) == len(fgraph.outputs)
    reason = "insert_deepcopy"
    updated_fgraph_inputs = {
        fgraph_i
        for i, fgraph_i in zip(wrapped_inputs, fgraph.inputs)
        if getattr(i, "update", False)
    }

    # We can't use fgraph.inputs as this don't include Constant Value.
    all_graph_inputs = list(graph_inputs(fgraph.outputs))
    has_destroyers_attr = hasattr(fgraph, "has_destroyers")

    for i in range(len(fgraph.outputs)):
        views_of_output_i = set()
        view_tree_set(fgraph, alias_root(fgraph.outputs[i]), views_of_output_i)
        copied = False
        # do not allow outputs to be aliased
        for j in range(i + 1, len(fgraph.outputs)):
            # We could don't put deep copy if both outputs have borrow==True
            # and not(wrapped_outputs[i].borrow and wrapped_outputs[j].borrow):
            if fgraph.outputs[j] in views_of_output_i:
                if wrapped_outputs[i].borrow and wrapped_outputs[j].borrow:
                    fgraph.change_input(
                        "output", i, view_op(fgraph.outputs[i]), reason=reason
                    )
                else:
                    fgraph.change_input(
                        "output", i, deep_copy_op(fgraph.outputs[i]), reason=reason
                    )
                copied = True
                break

        if not copied:
            for input_j in all_graph_inputs:
                # do not allow outputs to be aliased to an inputs (j), unless
                # a) that j'th input has been 'destroyed' by
                #    e.g. in-place computations
                # b) that j'th input is a shared variable that is also
                #    being updated
                if input_j in updated_fgraph_inputs:
                    continue
                if input_j in views_of_output_i and not (
                    has_destroyers_attr and fgraph.has_destroyers([input_j])
                ):
                    # We don't put deep_copy_op if the input and the
                    # output have borrow==True
                    if input_j in fgraph.inputs:
                        j = fgraph.inputs.index(input_j)
                        if wrapped_outputs[i].borrow and wrapped_inputs[j].borrow:
                            fgraph.change_input(
                                "output",
                                i,
                                view_op(fgraph.outputs[i]),
                                reason="insert_deepcopy",
                            )
                            break
                        else:
                            fgraph.change_input(
                                "output",
                                i,
                                deep_copy_op(fgraph.outputs[i]),
                                reason="insert_deepcopy",
                            )
                            break
                    elif wrapped_outputs[i].borrow:
                        fgraph.change_input(
                            "output",
                            i,
                            view_op(fgraph.outputs[i]),
                            reason="insert_deepcopy",
                        )
                        break
                    else:
                        fgraph.change_input(
                            "output",
                            i,
                            deep_copy_op(fgraph.outputs[i]),
                            reason="insert_deepcopy",
                        )
                        break


NODEFAULT = ["NODEFAULT"]


class FunctionMaker:
    """
    `FunctionMaker` is the class to `create` `Function` instances.

    This class has the fgraph, the optimizer, and the linker. When
    copying a `Function`, there is no need to duplicate the
    `FunctionMaker` instance. Deepcopy still copies both, which can
    variable in re-compilation.

    Parameters
    ----------
    inputs : list of SymbolicInput instances
    outputs : list of SymbolicOutput instances
        Outputs may also be a single Variable (not a list), in which case the
        functions produced by FunctionMaker will return their output value
        directly.
    mode : Mode instance
        Telling FunctionMaker how to optimize and link. None means to use the
        `config.mode`.
    accept_inplace : bool
        True iff it is acceptable to have inplace operations in the graph from
        the inputs to the outputs.
    on_unused_input : {'raise', 'warn', 'ignore', None}
        What to do if a variable in the 'inputs' list is not used in the graph.
        Possible values are:
        - 'raise': raise an error
        - 'warn': log a warning
        - 'ignore': do not do anything
        - None: Use the value in the Aesara flags on_unused_input.
    name : str
        An optional name for this function. If used, the profile mode will
        print the time spent in this function.

    """

    @staticmethod
    def wrap_in(input):
        if isinstance(input, (SymbolicInput)):
            return input
        elif isinstance(input, Variable):
            # r -> SymbolicInput(variable=r)
            return SymbolicInput(input)
        elif isinstance(input, (list, tuple)):
            # (r, u) -> SymbolicInput(variable=r, update=u)
            if len(input) == 2:
                return SymbolicInput(input[0], update=input[1])
            else:
                raise TypeError("Expected two elements in the list or tuple.", input)
        else:
            raise TypeError(
                f"Unknown input type: {type(input)} ({input}), expected Variable "
                "instance"
            )

    @staticmethod
    def expand_in(sinput, rinputs):
        # For SymbolicInputKits, this extracts a list of SymbolicInput
        # instances and corresponding indices such that these
        # SymbolicInputs are representative of some of the Variable
        # instances in inputs.  For SymbolicInput, this returns None
        # as the list of indices and a list with just the
        # SymbolicInput.
        # if isinstance(sinput, SymbolicInputKit):
        #    return sinput.complete(rinputs)
        # elif isinstance(sinput, SymbolicInput):
        if isinstance(sinput, SymbolicInput):
            return [None, [sinput]]

    @staticmethod
    def wrap_out(output):
        if isinstance(output, SymbolicOutput):
            return output
        elif isinstance(output, Variable):
            return SymbolicOutput(output)
        else:
            raise TypeError(f"Unknown output type: {type(output)} ({output})")

    def optimize_graph_with_cache(self, optimizer, inputs, outputs):
        # This function is not finished
        graph_db_file = os.path.join(config.compiledir, "optimized_graphs.pkl")

        # the inputs, outputs, and size of the graph to be optimized
        inputs_new = [inp.variable for inp in inputs]
        outputs_new = [out.variable for out in outputs]
        size_new = len(self.fgraph.apply_nodes)

        # Beginning of cache optimizations.
        # Could be refactored in different functions.

        def load_graph_db():
            if os.path.isfile(graph_db_file):
                print("graph_db already exists")
            else:
                # create graph_db
                with open(graph_db_file, "wb") as f:
                    print(f"create new graph_db in {graph_db_file}")
            # load the graph_db dictionary
            try:
                with open(graph_db_file, "rb") as f, config.change_flags(
                    unpickle_function=False
                ):
                    # Temporary hack to allow
                    # tests.scan.test_scan.T_Scan to
                    # finish. Should be changed in definitive version.
                    graph_db = pickle.load(f)
                print("graph_db loaded and it is not empty")
            except EOFError as e:
                # the file has nothing in it
                print(e)
                print("graph_db loaded and it is empty")
                graph_db = {}

            return graph_db

        def find_same_graph_in_db(graph_db):
            # If found_graph_in_db is None, then need to optimize.
            # Otherwise, return the graph found.
            found_graph_in_db = None
            # The sole purpose of this loop is to set 'need_optimize' by
            # going through graph_db, looking for graph that has the same
            # computation performed.
            for graph_old, graph_optimized in graph_db.items():
                inputs_old = graph_old.inputs
                outputs_old = graph_old.outputs
                size_old = len(graph_old.apply_nodes)
                # Some heuristics to check is the same graphs have
                # already been optimized before.
                if len(inputs_new) != len(inputs_old):
                    # If the inputs are of different size,
                    # two graphs are for sure different
                    print("need to optimize, because input size is different")
                    continue
                elif len(outputs_new) != len(outputs_old):
                    # If the inputs are of different size,
                    # two graphs are for sure different
                    print("need to optimize, because output size is different")
                    continue
                elif not all(
                    input_new.type == input_old.type
                    for input_new, input_old in zip(inputs_new, inputs_old)
                ):
                    print("need to optimize, because inputs are of different " "types")
                    continue
                elif not all(
                    output_new.type == output_old.type
                    for output_new, output_old in zip(outputs_new, outputs_old)
                ):
                    print("need to optimize, because outputs are of different " "types")
                    continue
                elif not size_old == size_new:
                    print(
                        "need to optimize, because numbers of nodes in graph"
                        " are different"
                    )
                    continue
                else:
                    flags = []
                    for i, (output_new, output_old) in enumerate(
                        zip(outputs_new, outputs_old)
                    ):
                        print("loop through outputs node for both graphs")
                        graph_old.variables = set(
                            vars_between(graph_old.inputs, graph_old.outputs)
                        )

                        # using clone allowed to avoid a lot of errors
                        # deep copy seemed to had.
                        f2 = graph_old.clone(check_integrity=False)
                        t1 = output_new
                        t2 = f2.outputs[i]

                        givens = dict(
                            zip(
                                graph_inputs([t1]),
                                graph_inputs([t2]),
                            )
                        )

                        temp = dict(
                            zip(
                                graph_inputs([t1]),
                                graph_inputs([t2]),
                            )
                        )

                        # hack to remove inconstent entry in givens
                        # seems to work that but source of inconsistency
                        # could be worth investigating.
                        for key, value in temp.items():
                            if key.type != value.type:
                                del givens[key]

                        flag = is_same_graph(t1, t2, givens=givens)

                        flags.append(flag)

                    is_same = all(flags)
                    if is_same:
                        # found the match
                        print("found a match, no need to optimize")
                        found_graph_in_db = graph_optimized
                        break
            return found_graph_in_db

        with lock_ctx():
            graph_db = load_graph_db()
            print(f"loaded graph_db from {graph_db_file}, size={len(graph_db)}")
            found_graph = find_same_graph_in_db(graph_db)
            if found_graph:
                self.fgraph = found_graph
                optimizer_profile = None
            else:
                # this is a brand new graph, optimize it, save it to graph_db
                print("graph not found in graph_db, optimizing the graph")
                self.fgraph.variables = set(
                    vars_between(self.fgraph.inputs, self.fgraph.outputs)
                )
                # check_integrity parameters was added to ignore
                # "excess cached variables" errors. Works that way
                # but once again the error couldbe worth
                # investigating.
                before_opt = self.fgraph.clone(check_integrity=False)
                optimizer_profile = optimizer(self.fgraph)
                graph_db.update({before_opt: self.fgraph})
                with open(graph_db_file, "wb") as f:
                    pickle.dump(graph_db, f, -1)
                print("new graph saved into graph_db")

        return optimizer_profile

    def __init__(
        self,
        inputs,
        outputs,
        mode=None,
        accept_inplace=False,
        function_builder=Function,
        profile=None,
        on_unused_input=None,
        fgraph=None,
        output_keys=None,
        name=None,
    ):
        # Save the provided mode, not the instanciated mode.
        # The instanciated mode don't pickle and if we unpickle an Aesara
        # function and it get re-compiled, we want the current optimizer to be
        # used, not the optimizer when it was saved.
        self.mode = mode
        mode = aesara.compile.mode.get_mode(mode)

        # Assert old way of working isn't used
        if getattr(mode, "profile", None):
            raise TypeError("profile passed via 'mode'. This isn't supported anymore")
        self.profile = profile
        if profile:
            # This is very important:
            # 1) We preload the cache here to don't have its timming
            #    included in optimization that compile function.
            # 2) Do not refresh the cache here by default. It cause
            #    too much execution time during testing as we compile
            #    much more functions then the number of compile c
            #    module.
            aesara.link.c.basic.get_module_cache().refresh()
        # Handle the case where inputs and/or outputs is a single
        # Variable (not in a list)
        unpack_single = False
        return_none = False
        if outputs is None:
            return_none = True
            outputs = []
        if not isinstance(outputs, (list, tuple)):
            unpack_single = True
            outputs = [outputs]
        if not isinstance(inputs, (list, tuple)):
            inputs = [inputs]

        # Wrap them in In or Out instances if needed.
        inputs = [self.wrap_in(i) for i in inputs]
        outputs = [self.wrap_out(o) for o in outputs]
        _inputs = list(
            graph_inputs(
                [o.variable for o in outputs]
                + [i.update for i in inputs if getattr(i, "update", False)]
            )
        )

        # Check if some input variables are unused
        self._check_unused_inputs(inputs, outputs, on_unused_input)

        # Make a list of (SymbolicInput|SymblicInputKits, indices,
        # [SymbolicInput,...]), one tuple for each input. (See
        # Function.indices for more details)
        indices = [[input] + self.expand_in(input, _inputs) for input in inputs]

        if fgraph is None:
            need_opt = True
            # make the fgraph (copies the graph, creates NEW INPUT AND
            # OUTPUT VARIABLES)
            fgraph, additional_outputs = std_fgraph(inputs, outputs, accept_inplace)
            fgraph.profile = profile
        else:
            # fgraph is already an optimized one
            need_opt = False
            updates = [spec.update for spec in inputs if spec.update]
            additional_outputs = list(map(SymbolicOutput, updates))

        self.fgraph = fgraph

        # Fetch the optimizer and linker
        optimizer, linker = mode.optimizer, copy.copy(mode.linker)
        if need_opt:
            # Why we add stack on node when it get done in output var?
            try:
                start_optimizer = time.time()

                # In case there is an error during optimization.
                optimizer_profile = None
                opt_time = None

                with config.change_flags(
                    compute_test_value=config.compute_test_value_opt,
                    traceback__limit=config.traceback__compile_limit,
                ):
                    # now optimize the graph
                    if config.cache_optimizations:
                        optimizer_profile = self.optimize_graph_with_cache(
                            optimizer, inputs, outputs
                        )
                    else:
                        optimizer_profile = optimizer(fgraph)

                    end_optimizer = time.time()
                    opt_time = end_optimizer - start_optimizer
                    _logger.debug(f"Optimizing took {opt_time:f} seconds")

                    # Add deep copy to respect the memory interface
                    insert_deepcopy(fgraph, inputs, outputs + additional_outputs)
            finally:

                # If the optimizer got interrupted
                if opt_time is None:
                    end_optimizer = time.time()
                    opt_time = end_optimizer - start_optimizer

                aesara.compile.profiling.total_graph_opt_time += opt_time

                if profile:
                    if optimizer_profile is None and hasattr(optimizer, "pre_profile"):
                        optimizer_profile = optimizer.pre_profile

                    profile.optimizer_time += opt_time

                    if config.profile_optimizer:
                        profile.optimizer_profile = (optimizer, optimizer_profile)
                # IF False, if mean the profile for that function was
                # explicitly disabled
                elif config.profile_optimizer and profile is not False:
                    warnings.warn(
                        (
                            "config.profile_optimizer requires config.profile to "
                            " be set to True as well"
                        ),
                        stacklevel=3,
                    )

        # initialize the linker
        if not hasattr(linker, "accept"):
            raise ValueError(
                "'linker' parameter of FunctionMaker should be "
                f"a Linker with an accept method or one of {list(aesara.compile.mode.predefined_linkers.keys())}"
            )

        # the 'no_borrow' outputs are the ones for which that we can't
        # return the internal storage pointer.
        assert len(fgraph.outputs) == len(outputs + additional_outputs)
        no_borrow = [
            output
            for output, spec in zip(fgraph.outputs, outputs + additional_outputs)
            if not spec.borrow
        ]
        if no_borrow:
            self.linker = linker.accept(
                fgraph,
                no_recycling=infer_reuse_pattern(fgraph, no_borrow),
                profile=profile,
            )
        else:
            self.linker = linker.accept(fgraph, profile=profile)

        if hasattr(linker, "accept_var_updates"):
            # hacky thing so VMLinker knows about updates
            self.linker.accept_var_updates(fgraph_updated_vars(fgraph, inputs))
        fgraph.name = name
        self.indices = indices
        self.inputs = inputs
        self.expanded_inputs = inputs
        self.outputs = outputs
        self.unpack_single = unpack_single
        self.return_none = return_none
        self.accept_inplace = accept_inplace
        self.function_builder = function_builder
        self.on_unused_input = on_unused_input  # Used for the pickling/copy
        self.output_keys = output_keys
        self.name = name

        self.required = [(i.value is None) for i in self.inputs]
        self.refeed = [
            (
                i.value is not None
                and not isinstance(i.value, Container)
                and i.update is None
            )
            for i in self.inputs
        ]

    def _check_unused_inputs(self, inputs, outputs, on_unused_input):
        if on_unused_input is None:
            on_unused_input = config.on_unused_input

        if on_unused_input == "ignore":
            return

        # There should be two categories of variables in inputs:
        #  - variables that have to be provided (used_inputs)
        #  - shared variables that will be updated
        used_inputs = list(
            ancestors(
                (
                    [o.variable for o in outputs]
                    + [i.update for i in inputs if getattr(i, "update", False)]
                ),
                blockers=[i.variable for i in inputs],
            )
        )

        msg = (
            "aesara.function was asked to create a function computing "
            "outputs given certain inputs, but the provided input "
            "variable at index %i is not part of the computational graph "
            "needed to compute the outputs: %s.\n%s"
        )
        warn_msg = (
            "To make this warning into an error, you can pass the "
            "parameter on_unused_input='raise' to aesara.function. "
            "To disable it completely, use on_unused_input='ignore'."
        )
        err_msg = (
            "To make this error into a warning, you can pass the "
            "parameter on_unused_input='warn' to aesara.function. "
            "To disable it completely, use on_unused_input='ignore'."
        )

        for i in inputs:
            if (i.variable not in used_inputs) and (i.update is None):
                if on_unused_input == "warn":
                    warnings.warn(
                        msg % (inputs.index(i), i.variable, warn_msg), stacklevel=6
                    )
                elif on_unused_input == "raise":
                    raise UnusedInputError(msg % (inputs.index(i), i.variable, err_msg))
                else:
                    raise ValueError(
                        "Invalid value for keyword "
                        "on_unused_input of aesara.function: "
                        "'%s'.\nValid values are 'raise', "
                        "'warn', and 'ignore'." % on_unused_input
                    )

    def create(self, input_storage=None, trustme=False, storage_map=None):
        """
        Create a function.

        Parameters
        ----------
        input_storage
            A list matching the inputs list and providing default values if the
            default for an input is None, then that input is a required input.
            For an input with an update, the default acts as initialization.
        trustme
            Disables some exceptions, used internally.

        """

        if input_storage is None:
            input_storage = [None] * len(self.inputs)
        # list of independent one-element lists, will be passed to the linker
        input_storage_lists = []
        defaults = []

        # The following loop is to fill in the input_storage_lists and
        # defaults lists.
        assert len(self.indices) == len(input_storage)
        for i, ((input, indices, subinputs), input_storage_i) in enumerate(
            zip(self.indices, input_storage)
        ):

            # Replace any default value given as a variable by its
            # container.  Note that this makes sense only in the
            # context of shared variables, but for now we avoid
            # dealing directly with them to avoid dependency on the
            # shared variables work-in-progress repository.
            if isinstance(input_storage_i, Variable):
                input_storage_i = input_storage_i.container

            if isinstance(input_storage_i, Container):
                # If the default is a Container, this means we want to
                # share the same storage. This is done by appending
                # input_storage_i.storage to input_storage_lists.
                if indices is not None:
                    raise TypeError(
                        "Cannot take a Container instance as "
                        "default for a SymbolicInputKit."
                    )
                input_storage_lists.append(input_storage_i.storage)

                storage = input_storage[i].storage[0]

            else:
                # Normal case: one new, independent storage unit
                input_storage_lists.append([input_storage_i])

                storage = input_storage_i

            required = self.required[i]
            refeed = self.refeed[i]
            # sanity check-- if an input is required it should not
            # need to be refed
            assert not (required and refeed)

            # shared variables need neither be input by the user nor refed
            if input.shared:
                assert not required
                assert not refeed
                storage = None

            # if an input is required, it never need be refed
            if required:
                storage = None

            # make sure that we only store a value if we actually need it
            if storage is not None:
                assert refeed or not required

            defaults.append((required, refeed, storage))

        # Get a function instance
        start_linker = time.time()
        start_import_time = aesara.link.c.cmodule.import_time

        with config.change_flags(traceback__limit=config.traceback__compile_limit):
            _fn, _i, _o = self.linker.make_thunk(
                input_storage=input_storage_lists, storage_map=storage_map
            )

        end_linker = time.time()

        linker_time = end_linker - start_linker
        aesara.compile.profiling.total_time_linker += linker_time
        _logger.debug(f"Linker took {linker_time:f} seconds")
        if self.profile:
            self.profile.linker_time += linker_time
            _fn.time_thunks = self.profile.flag_time_thunks
            import_time = aesara.link.c.cmodule.import_time - start_import_time
            self.profile.import_time += import_time

        fn = self.function_builder(
            _fn,
            _i,
            _o,
            self.indices,
            self.outputs,
            defaults,
            self.unpack_single,
            self.return_none,
            self.output_keys,
            self,
            name=self.name,
        )

        fn.profile = self.profile
        return fn


def _constructor_FunctionMaker(kwargs):
    # Needed for old pickle
    # Old pickle have at least the problem that output_keys where not saved.
    if config.unpickle_function:
        if config.reoptimize_unpickled_function:
            del kwargs["fgraph"]
        return FunctionMaker(**kwargs)
    else:
        return None


__checkers: List = []


def check_equal(x, y):
    for checker in __checkers:
        try:
            return checker(x, y)
        except Exception:
            continue
    return x == y


def register_checker(checker):
    __checkers.insert(0, checker)


def orig_function(
    inputs,
    outputs,
    mode=None,
    accept_inplace=False,
    name=None,
    profile=None,
    on_unused_input=None,
    output_keys=None,
):
    """
    Return a Function that will calculate the outputs from the inputs.

    Parameters
    ----------
    inputs : list of `SymbolicInput` or `In` instances
    outputs : a SymbolicOutput or a list of `SymbolicOutput` or `Out` instances
        The return value of the returned function will match the format of this
        argument (either the value itself or a list of one or more return
        values).
    mode : descriptive string or Mode instance
        Default of None means to use `config.mode` (see below for descriptive
        string list).
    name : str
        An optional name for this function. If used, the profile mode will print the
        time spent in this function.
    accept_inplace : bool
        True iff the graph can contain inplace operations prior to the
        optimization phase (default is False).
    profile : None or ProfileStats instance
    on_unused_input : {'raise', 'warn', 'ignore', None}
        What to do if a variable in the 'inputs' list is not used in the graph.
    output_keys :
        If the outputs were provided to aesara.function as a list, then
        output_keys is None. Otherwise, if outputs were provided as a dict,
        output_keys is the sorted list of keys from the outputs.

    Notes
    -----
    Currently, the library provides the following mode strings:

    - FAST_RUN (default) (optimize without too much time)

    - FAST_COMPILE (minimal optimization)

    - DebugMode: verify many internal conditions that are normally assumed
      (slow)

    """

    # Every element of the input list will be upgraded to an `In` instance if
    # necessary, using the rules implemented by the `convert_function_input`
    # function.

    # Similarly, every element of the output list will be upgraded to an `Out`
    # instance if necessary:

    t1 = time.time()
    mode = aesara.compile.mode.get_mode(mode)

    inputs = list(map(convert_function_input, inputs))
    if outputs is not None:
        if isinstance(outputs, (list, tuple)):
            outputs = list(map(FunctionMaker.wrap_out, outputs))
        else:
            outputs = FunctionMaker.wrap_out(outputs)

    defaults = [getattr(input, "value", None) for input in inputs]

    if isinstance(mode, (list, tuple)):  # "mode comparison" semantics
        raise Exception("We do not support the passing of multiple modes")
    fn = None
    try:
        Maker = getattr(mode, "function_maker", FunctionMaker)
        m = Maker(
            inputs,
            outputs,
            mode,
            accept_inplace=accept_inplace,
            profile=profile,
            on_unused_input=on_unused_input,
            output_keys=output_keys,
            name=name,
        )
        with config.change_flags(compute_test_value="off"):
            fn = m.create(defaults)
    finally:
        t2 = time.time()
        if fn and profile:
            profile.compile_time += t2 - t1
            # TODO: append
            profile.nb_nodes = len(fn.maker.fgraph.apply_nodes)

    return fn


def convert_function_input(input):
    """
    Upgrade a input shortcut to an In instance.

    The rules for upgrading are as follows:

    - a `Variable` instance r will be upgraded like `In`(r)

    - a tuple (name, r) will be `In`(r, name=name)

    - a tuple (r, val) will be `In`(r, value=value, autoname=True)

    - a tuple ((r,up), val) will be
      `In`(r, value=value, update=up, autoname=True)

    - a tuple (name, r, val) will be `In`(r, name=name, value=value)

    - a tuple (name, (r,up), val) will be
      `In`(r, name=name, value=val, update=up, autoname=True)

    """
    if isinstance(input, SymbolicInput):
        return input
    elif isinstance(input, Constant):
        raise TypeError("A Constant instance is not a legal function input", input)
    elif isinstance(input, Variable):
        return In(input)
    elif isinstance(input, (list, tuple)):
        orig = input
        if not input:
            raise TypeError(f"Nonsensical input specification: {input}")
        if isinstance(input[0], str):
            name = input[0]
            input = input[1:]
        else:
            name = None
        if isinstance(input[0], (list, tuple)):
            if len(input[0]) != 2 or len(input) != 2:
                raise TypeError(
                    f"Invalid input syntax: {orig} (check "
                    "documentation or use an In instance)"
                )
            (variable, update), value = input
        elif isinstance(input[0], Variable):
            if len(input) == 1:
                variable, update, value = input[0], None, None
            elif len(input) == 2:
                (variable, value), update = input, None
            else:
                raise TypeError(
                    f"Invalid input syntax: {orig} (check "
                    "documentation or use an In instance)"
                )
        elif isinstance(input[0], SymbolicInput):
            if len(input) == 1:
                return input[0]
            elif len(input) == 2:
                input, value = input
                if name is not None:
                    input.name = name
                input.value = value
                return input
        else:
            raise TypeError(f"The input specification is not valid: {input}")

        if not isinstance(variable, Variable):
            raise TypeError(
                f"Unknown input type: {type(variable)}, expected Variable instance",
                variable,
            )
        if update is not None and not isinstance(update, Variable):
            raise TypeError(
                f"Unknown update type: {type(update)}, expected Variable instance",
                update,
            )
        if value is not None and isinstance(value, (Variable, SymbolicInput)):
            raise TypeError(
                f"The value for input {variable} should not be a Variable "
                f"or SymbolicInput instance (got: {value})"
            )

        return In(variable, name=name, value=value, update=update)
    else:
        raise TypeError(
            f"Unknown input type: {type(input)}, expected Variable instance", input
        )


def get_info_on_inputs(named_inputs, n_unnamed_inputs):
    """
    Return a human-readable description of named and un-named inputs.

    """
    n_named_inputs = len(named_inputs)

    def get_plural(n):
        if n > 1:
            return "s"
        else:
            return ""

    if n_named_inputs == 0:
        if n_unnamed_inputs == 0:
            msg = "The function is supposed to have no input."
        else:
            if n_unnamed_inputs == 1:
                msg = (
                    "The function has a single input variable which has no "
                    "name, and thus cannot be assigned through a keyword"
                    " argument (use 'name=...' in a Variable's "
                    "constructor to give it a name)."
                )
            else:
                # Use plural.
                msg = (
                    f"The function has {n_unnamed_inputs} inputs, but none of them is named,"
                    " and thus they cannot be assigned through keyword "
                    "arguments (use 'name=...' in a Variable's "
                    "constructor to give it a name)."
                )
    else:
        if n_unnamed_inputs == 0:
            msg = "The function has {} named input{} ({}).".format(
                n_named_inputs,
                get_plural(n_named_inputs),
                ", ".join(named_inputs),
            )
        else:
            msg = (
                f"The function has {n_named_inputs} named input{get_plural(n_named_inputs)} ({', '.join(named_inputs)}), and {n_unnamed_inputs} unnamed "
                f"input{get_plural(n_unnamed_inputs)} which thus cannot be accessed through keyword "
                f"argument{get_plural(n_unnamed_inputs)} (use 'name=...' in a variable's constructor "
                "to give it a name)."
            )
    return msg
