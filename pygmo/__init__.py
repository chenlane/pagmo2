# -*- coding: utf-8 -*-

# Copyright 2017 PaGMO development team
#
# This file is part of the PaGMO library.
#
# The PaGMO library is free software; you can redistribute it and/or modify
# it under the terms of either:
#
#   * the GNU Lesser General Public License as published by the Free
#     Software Foundation; either version 3 of the License, or (at your
#     option) any later version.
#
# or
#
#   * the GNU General Public License as published by the Free Software
#     Foundation; either version 3 of the License, or (at your option) any
#     later version.
#
# or both in parallel, as here.
#
# The PaGMO library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received copies of the GNU General Public License and the
# GNU Lesser General Public License along with the PaGMO library.  If not,
# see https://www.gnu.org/licenses/.

# for python 2.0 compatibility
from __future__ import absolute_import as _ai

# We import the sub-modules into the root namespace
from .core import *
from .plotting import *
from .py_islands import *

# And we explicitly import the submodules
from . import core
from . import plotting
from . import test

# Patch the problem class.
from . import _patch_problem


# Patch the algorithm class.
from . import _patch_algorithm


class thread_safety(object):
    """Thread safety level.

    This enum defines a set of values that can be used to specify the thread safety of problems, algorithms, etc.

    """

    #: No thread safety: any concurrent operation on distinct instances is unsafe
    none = core._thread_safety.none
    #: Basic thread safety: any concurrent operation on distinct instances is safe
    basic = core._thread_safety.basic


# Override of the translate meta-problem constructor.
__original_translate_init = translate.__init__

# NOTE: the idea of having the translate init here instead of exposed from C++ is to allow the use
# of the syntax translate(udp, translation) for all udps


def _translate_init(self, prob=None, translation=[0.]):
    """
    Args:
        prob: a user-defined problem (either Python or C++), or an instance of :class:`~pygmo.problem`
            (if ``None``, the population problem will be :class:`~pygmo.null_problem`)
        translation (array-like object): an array containing the translation to be applied

    Raises:
        ValueError: if the length of *translation* is not equal to the dimension of *prob*
        unspecified: any exception thrown by:

        * the constructor of :class:`pygmo.problem`,
        * the constructor of the underlying C++ class,
        * failures at the intersection between C++ and Python (e.g., type conversion errors, mismatched function
            signatures, etc.)
    """
    if prob is None:
        # Use the null problem for default init.
        prob = null_problem()
    if type(prob) == problem:
        # If prob is a pygmo problem, we will pass it as-is to the
        # original init.
        prob_arg = prob
    else:
        # Otherwise, we attempt to create a problem from it. This will
        # work if prob is an exposed C++ problem or a Python UDP.
        prob_arg = problem(prob)
    __original_translate_init(self, prob_arg, translation)

setattr(translate, "__init__", _translate_init)

# Override of the decompose meta-problem constructor.
__original_decompose_init = decompose.__init__

# NOTE: the idea of having the translate init here instead of exposed from C++ is to allow the use
# of the syntax decompose(udp, ..., ) for all udps


def _decompose_init(self, prob=None, weight=[0.5, 0.5], z=[0., 0.], method='weighted', adapt_ideal=False):
    """
    Args:
        prob: a user-defined problem (either Python or C++), or an instance of :class:`~pygmo.problem`
            (if ``None``, the population problem will be :class:`~pygmo.null_problem`)
        weight (array-like object): the vector of weights :math:`\boldsymbol \lambda`
        z (array-like object): the reference point :math:`\mathbf z^*`
        method (``str``): a string containing the decomposition method chosen
        adapt_ideal (``bool``): when ``True``, the reference point is adapted at each fitness evaluation
            to be the ideal point

    Raises:
        ValueError: if either:

        * *prob* is single objective or constrained,
        * *method* is not one of [``'weighted'``, ``'tchebycheff'``, ``'bi'``],
        * *weight* is not of size :math:`n`,
        * *z* is not of size :math:`n`
        * *weight* is not such that :math:`\\lambda_i > 0, \\forall i=1..n`,
        * *weight* is not such that :math:`\\sum_i \\lambda_i = 1`

        unspecified: any exception thrown by:

        * the constructor of :class:`pygmo.problem`,
        * the constructor of the underlying C++ class,
        * failures at the intersection between C++ and Python (e.g., type conversion errors, mismatched function
            signatures, etc.)

    """
    if prob is None:
        # Use the null problem for default init.
        prob = null_problem(nobj=2)
    if type(prob) == problem:
        # If prob is a pygmo problem, we will pass it as-is to the
        # original init.
        prob_arg = prob
    else:
        # Otherwise, we attempt to create a problem from it. This will
        # work if prob is an exposed C++ problem or a Python UDP.
        prob_arg = problem(prob)
    __original_decompose_init(self, prob_arg, weight, z, method, adapt_ideal)

setattr(decompose, "__init__", _decompose_init)

# Override of the unconstrain meta-problem constructor.
__original_unconstrain_init = unconstrain.__init__

# NOTE: the idea of having the unconstrain init here instead of exposed from C++ is to allow the use
# of the syntax unconstrain(udp, ... ) for all udps


def _unconstrain_init(self, prob=None, method="death penalty", weights=[]):
    """
    Args:
        prob: a user-defined problem (either C++ or Python - note that *udp* will be deep-copied
              and stored inside the :class:`~pygmo.unconstrained` instance)
        method (``str``): a string containing the unconstrain method chosen, one of [``'death penalty'``, ``'kuri'``, ``'weighted'``, ``'ignore_c'``, ``'ignore_o'``]
        weights (array-like object): the vector of weights to be used if the method chosen is "weighted"

    Raises:
        ValueError: if either:

        * *prob* is unconstrained,
        * *method* is not one of [``'death penalty'``, ``'kuri'``, ``'weighted'``, ``'ignore_c'``, ``'ignore_o'``],
        * *weight* is not of the same size as the problem constraints (if the method ``'weighted'`` is selcted), or not empty otherwise.

        unspecified: any exception thrown by:

        * the constructor of :class:`pygmo.problem`,
        * the constructor of the underlying C++ class,
        * failures at the intersection between C++ and Python (e.g., type conversion errors, mismatched function
            signatures, etc.)

    """
    if prob is None:
        # Use the null problem for default init.
        prob = null_problem(nobj=2, nec=3, nic=4)
    if type(prob) == problem:
        # If prob is a pygmo problem, we will pass it as-is to the
        # original init.
        prob_arg = prob
    else:
        # Otherwise, we attempt to create a problem from it. This will
        # work if prob is an exposed C++ problem or a Python UDP.
        prob_arg = problem(prob)
    __original_unconstrain_init(self, prob_arg, method, weights)

setattr(unconstrain, "__init__", _unconstrain_init)

# Override of the mbh meta-algorithm constructor.
__original_mbh_init = mbh.__init__
# NOTE: the idea of having the mbh init here instead of exposed from C++ is to allow the use
# of the syntax mbh(uda, ...) for all udas


def _mbh_init(self, algo=None, stop=5, perturb=1e-2, seed=None):
    """
    Args:
        algo: a user-defined algorithm (either C++ or Python - note that *algo* will be deep-copied
             and stored inside the :class:`~pygmo.mbh` instance)
        stop (``int``): consecutive runs of the inner algorithm that need to result in no improvement for
             :class:`~pygmo.mbh` to stop
        perturb (``float`` or array-like object): perturb the perturbation to be applied to each component
        seed (``int``): seed used by the internal random number generator

    Raises:
        ValueError: if *perturb* (or one of its components, if *perturb* is an array) is not in the
             (0,1] range
        unspecified: any exception thrown by the constructor of :class:`pygmo.algorithm`, or by
             failures at the intersection between C++ and Python (e.g., type conversion errors, mismatched function
             signatures, etc.)

    """
    if algo is None:
        # Use the null problem for default init.
        algo = compass_search()
    if type(algo) == algorithm:
        # If algo is a pygmo algorithm, we will pass it as-is to the
        # original init.
        algo_arg = algo
    else:
        # Otherwise, we attempt to create an algorithm from it. This will
        # work if algo is an exposed C++ algorithm or a Python UDA.
        algo_arg = algorithm(algo)
    if type(perturb) is float:
        perturb = [perturb]
    if seed is None:
        __original_mbh_init(self, algo_arg, stop, perturb)
    else:
        __original_mbh_init(self, algo_arg, stop, perturb, seed)

setattr(mbh, "__init__", _mbh_init)

# Override of the cstrs_self_adaptive meta-algorithm constructor.
__original_cstrs_self_adaptive_init = cstrs_self_adaptive.__init__
# NOTE: the idea of having the cstrs_self_adaptive init here instead of exposed from C++ is to allow the use
# of the syntax cstrs_self_adaptive(uda, ...) for all udas


def _cstrs_self_adaptive_init(self, iters=1, algo=None, seed=None):
    """
    Args:
        iter (``int``): number of iterations (i.e. calls to the innel algorithm evolve)
        algo: a user-defined algorithm (either C++ or Python - note that *algo* will be deep-copied
             and stored inside the :class:`~pygmo.cstrs_self_adaptive` instance)
        seed (``int``): seed used by the internal random number generator

    Raises:
        ValueError: if *iters* is negative or greater than an implementation-defined value
        unspecified: any exception thrown by the constructor of :class:`pygmo.algorithm`, or by
             failures at the intersection between C++ and Python (e.g., type conversion errors, mismatched function
             signatures, etc.)

    """
    if algo is None:
        # Use the null problem for default init.
        algo = de()
    if type(algo) == algorithm:
        # If algo is a pygmo algorithm, we will pass it as-is to the
        # original init.
        algo_arg = algo
    else:
        # Otherwise, we attempt to create an algorithm from it. This will
        # work if algo is an exposed C++ algorithm or a Python UDA.
        algo_arg = algorithm(algo)
    if seed is None:
        __original_cstrs_self_adaptive_init(self, iters, algo_arg)
    else:
        __original_cstrs_self_adaptive_init(self, iters, algo_arg, seed)

setattr(cstrs_self_adaptive, "__init__", _cstrs_self_adaptive_init)


# Override of the population constructor.
__original_population_init = population.__init__


def _population_init(self, prob=None, size=0, seed=None):
    # NOTE: the idea of having the pop init here instead of exposed from C++ is that like this we don't need
    # to expose a new pop ctor each time we expose a new problem: in this method we will use the problem ctor
    # from a C++ problem, and on the C++ exposition side we need only to
    # expose the ctor of pop from pagmo::problem.
    """
    Args:
        prob: a user-defined problem (either Python or C++), or an instance of :class:`~pygmo.problem`
            (if ``None``, the population problem will be :class:`~pygmo.null_problem`)
        size (``int``): the number of individuals
        seed (``int``): the random seed (if ``None``, it will be randomly-generated)

    Raises:
        TypeError: if *size* is not an ``int`` or *seed* is not ``None`` and not an ``int``
        OverflowError:  is *size* or *seed* are negative
        unspecified: any exception thrown by the invoked C++ constructors or by the constructor of
            :class:`~pygmo.problem`, or by failures at the intersection between C++ and
            Python (e.g., type conversion errors, mismatched function signatures, etc.)

    """
    import sys
    int_types = (int, long) if sys.version_info[0] < 3 else (int,)
    # Check input params.
    if not isinstance(size, int_types):
        raise TypeError("the 'size' parameter must be an integer")
    if not seed is None and not isinstance(seed, int_types):
        raise TypeError("the 'seed' parameter must be None or an integer")
    if prob is None:
        # Use the null problem for default init.
        prob = null_problem()
    if type(prob) == problem:
        # If prob is a pygmo problem, we will pass it as-is to the
        # original init.
        prob_arg = prob
    else:
        # Otherwise, we attempt to create a problem from it. This will
        # work if prob is an exposed C++ problem or a Python UDP.
        prob_arg = problem(prob)
    if seed is None:
        __original_population_init(self, prob_arg, size)
    else:
        __original_population_init(self, prob_arg, size, seed)

setattr(population, "__init__", _population_init)

# Add the problem property (see comments in core.pp).


def _problem_prop(self):
    """Population's problem.

    This read-only property gives direct access to the :class:`~pygmo.problem` stored within the population.

    Returns:
        :class:`~pygmo.problem`: a reference to the internal problem
    """
    return self._problem()

population.problem = property(_problem_prop)

# Override of the island constructor.
__original_island_init = island.__init__


def _island_init(self, **kwargs):
    """
    Keyword Args:
        udi: a user-defined island (either Python or C++ - note that *udi* will be deep-copied
          and stored inside the :class:`~pygmo.island` instance)
        algo: a user-defined algorithm (either Python or C++), or an instance of :class:`~pygmo.algorithm`
        pop (:class:`~pygmo.population`): a population
        prob: a user-defined problem (either Python or C++), or an instance of :class:`~pygmo.problem`
        size (``int``): the number of individuals
        seed (``int``): the random seed (if not specified, it will be randomly-generated)

    Raises:
        KeyError: if the set of keyword arguments is invalid
        unspecified: any exception thrown by:

          * the invoked C++ constructors,
          * the deep copy of the UDI,
          * the constructors of :class:`~pygmo.algorithm` and :class:`~pygmo.population`,
          * failures at the intersection between C++ and Python (e.g., type conversion errors, mismatched function
            signatures, etc.)

    """
    if len(kwargs) == 0:
        # Default constructor.
        __original_island_init(self)
        return

    # If we are not dealing with a def ctor, we always need the algo argument.
    if not "algo" in kwargs:
        raise KeyError(
            "the mandatory 'algo' parameter is missing from the list of arguments "
            "of the island constructor")
    algo = kwargs.pop('algo')
    algo = algo if isinstance(algo, algorithm) else algorithm(algo)

    # Population setup. We either need an input pop, or the prob and size,
    # plus optionally seed.
    if 'pop' in kwargs and ('prob' in kwargs or 'size' in kwargs or 'seed' in kwargs):
        raise KeyError(
            "if the 'pop' argument is provided, the 'prob', 'size' and 'seed' "
            "arguments must not be provided")
    elif 'pop' in kwargs:
        pop = kwargs.pop("pop")
    elif 'prob' in kwargs and 'size' in kwargs:
        if 'seed' in kwargs:
            pop = population(kwargs.pop('prob'), kwargs.pop(
                'size'), kwargs.pop('seed'))
        else:
            pop = population(kwargs.pop('prob'), kwargs.pop('size'))
    else:
        raise KeyError(
            "unable to construct a population from the arguments of "
            "the island constructor: you must either pass a population "
            "('pop') or a set of arguments that can be used to build one "
            "('prob', 'size' and, optionally, 'seed')")

    # UDI, if any.
    if 'udi' in kwargs:
        args = [kwargs.pop('udi'), algo, pop]
    else:
        args = [algo, pop]

    if len(kwargs) != 0:
        raise KeyError(
            "unrecognised keyword arguments: {}".format(list(kwargs.keys())))

    __original_island_init(self, *args)


setattr(island, "__init__", _island_init)

# Override of the archi constructor.
__original_archi_init = archipelago.__init__


def _archi_init(self, n=0, **kwargs):
    """
    The constructor will initialise an archipelago with *n* islands built from *kwargs*.
    The keyword arguments accept the same format as explained in the constructor of
    :class:`~pygmo.island`, with the following differences:

    * *size* is replaced by *pop_size*, for clarity,
    * the *seed* argument, if present, is used to initialise a random number generator
      that, in turn, is used to generate random seeds for each island population. In other
      words, the *seed* argument allows to generate randomly (but deterministically)
      the seeds of the populations in the archipelago. If *seed* is not provided, the seeds
      of the populations will be random and non-deterministic.

    Args:
        n (``int``): the number of islands in the archipelago

    Keyword Args:
        udi: a user-defined island (either Python or C++ - note that *udi* will be deep-copied
          and stored inside the :class:`~pygmo.island` instances)
        algo: a user-defined algorithm (either Python or C++), or an instance of :class:`~pygmo.algorithm`
        pop (:class:`~pygmo.population`): a population
        prob: a user-defined problem (either Python or C++), or an instance of :class:`~pygmo.problem`
        pop_size (``int``): the number of individuals for each island
        seed (``int``): the random seed

    Raises:
        TypeError: if *n* is not an integral type
        ValueError: if *n* is negative
        unspecified: any exception thrown by the constructor of :class:`~pygmo.island`
          or by the underlying C++ constructor

    Examples:
        >>> from pygmo import *
        >>> archi = archipelago(n = 16, algo = de(), prob = rosenbrock(10), pop_size = 20, seed = 32)
        >>> archi #doctest: +SKIP
        Number of islands: 16
        Evolving: false
        <BLANKLINE>
        Islands summaries:
        <BLANKLINE>
                #   Type           Algo                    Prob                                  Size  Evolving
                -------------------------------------------------------------------------------------------------
                0   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                1   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                2   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                3   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                4   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                5   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                6   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                7   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                8   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                9   Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                10  Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                11  Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                12  Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                13  Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                14  Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
                15  Thread island  Differential Evolution  Multidimensional Rosenbrock Function  20    false
        <BLANKLINE>
        >>> archi.evolve()
        >>> archi.wait()
        >>> res = archi.get_champions_f()
        >>> res #doctest: +SKIP
        [array([ 475165.1020545]),
        array([ 807090.7156793]),
        array([ 229737.91987225]),
        array([ 598229.45585525]),
        array([ 560599.11409213]),
        array([ 417323.13905327]),
        array([ 241436.42395722]),
        array([ 393381.06926308]),
        array([ 212331.35741299]),
        array([ 212218.93755491]),
        array([ 497985.30014]),
        array([ 310792.64466701]),
        array([ 421278.03109775]),
        array([ 557967.33605791]),
        array([ 281039.56040264]),
        array([ 215539.10152038])]


    """
    import sys
    int_types = (int, long) if sys.version_info[0] < 3 else (int,)
    # Check n.
    if not isinstance(n, int_types):
        raise TypeError("the 'n' parameter must be an integer")
    if n < 0:
        raise ValueError(
            "the 'n' parameter must be non-negative, but it is {} instead".format(n))

    # Replace the 'pop_size' kw arg with just 'size', for later use in the
    # island ctor.

    if 'size' in kwargs:
        raise KeyError(
            "the 'size' argument cannot appear among the named arguments of the archipelago constructor")

    if 'pop_size' in kwargs:
        # Extract 'pop_size', replace with just 'size'.
        ps_val = kwargs.pop('pop_size')
        kwargs['size'] = ps_val

    # Call the original init, which constructs an empty archi.
    __original_archi_init(self)

    if 'seed' in kwargs:
        # Special handling of the 'seed' argument.
        from random import Random
        from .core import _max_unsigned
        # Create a random engine with own state.
        RND = Random()
        # Get the seed from kwargs.
        seed = kwargs.pop('seed')
        if not isinstance(seed, int_types):
            raise TypeError("the 'seed' parameter must be an integer")
        # Seed the rng.
        RND.seed(seed)
        u_max = _max_unsigned()
        # Push back the islands with different seed.
        for _ in range(n):
            kwargs['seed'] = RND.randint(0, u_max)
            self.push_back(**kwargs)

    else:
        # Push back islands.
        for _ in range(n):
            self.push_back(**kwargs)

setattr(archipelago, "__init__", _archi_init)


def _archi_push_back(self, **kwargs):
    """Add island.

    This method will construct an island from the supplied arguments and add it to the archipelago.
    Islands are added at the end of the archipelago (that is, the new island will have an index
    equal to the size of the archipelago before the call to this method).

    The keyword arguments accept the same format as explained in the constructor of
    :class:`~pygmo.island`.

    Raises:
        unspecified: any exception thrown by the constructor of :class:`~pygmo.island` or by
          the underlying C++ method

    """
    self._push_back(island(**kwargs))

setattr(archipelago, "push_back", _archi_push_back)

# Register the cleanup function.
import atexit as _atexit
from .core import _cleanup as _cpp_cleanup


def _cleanup():
    mp_island._shutdown_pool()
    _cpp_cleanup()


_atexit.register(_cleanup)
