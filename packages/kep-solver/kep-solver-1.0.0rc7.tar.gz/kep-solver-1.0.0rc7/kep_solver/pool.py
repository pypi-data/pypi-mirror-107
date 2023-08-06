"""Handling of KEP pools, which are just the rules, procedures and algorithms
for a particular KEP.
"""

from time import thread_time
from typing import Optional

from kep_solver.entities import Instance
from kep_solver.model import Objective, CycleAndChainModel
from kep_solver.graph import Vertex


class Solution:
    """A solution to one instance of a KEP. Contains the exchanges, and the set
    of objective values attained.
    """

    def __init__(self, exchanges: list[list[Vertex]], scores: list[float],
                 possible: list[tuple[list[Vertex], list[float]]],
                 times: list[tuple[str, float]]):
        """Constructor for Solution. This class essentially just stores any
        information that may be useful.

        :param exchanges: the list of selected exchanges
        :type exchanges: list[list[Vertex]]
        :param scores: the list of scores achieved for each objective
        :type scores: list[float]
        :param possible: the set of possible exchanges, and their values\
        for each objective
        :type possible: list[tuple[list[Vertex], list[float]]]
        :param times: The time taken for various operations. Each is a tuple\
        with a string description of the action, and the time (in seconds)
        :type times: list[tuple[str, float]]
        """
        self._selected: list[list[Vertex]] = exchanges
        self._values: list[float] = scores
        self._possible: list[tuple[list[Vertex], list[float]]] = possible
        self._times: list[tuple[str, float]] = times

    @property
    def times(self) -> list[tuple[str, float]]:
        """Get the time taken for various operations. Each element of the
        returned list is a tuple where the first item is a string description
        of some operation, and the second item is the time taken in seconds.

        :return: the list of times (and their descriptions)
        :rtype: list[tuple[str, float]]
        """
        return self._times

    @property
    def selected(self) -> list[list[Vertex]]:
        """Get the selected solution.

        :return: the list of exchanges selected.
        :rtype: list[list[Vertex]]
        """
        return self._selected

    @property
    def values(self) -> list[float]:
        """Get the Objective values of the selected solution.

        :return: the list of objective values
        :rtype: list[float]
        """
        return self._values

    @property
    def possible(self) -> list[tuple[list[Vertex], list[float]]]:
        """Return a list of all the possible chains and cycles that may be selected.
        For each chain/cycle, there is an associated list of values, such that
        the i'th value for a given chain/cycle is the value that chain/cycle
        has for the i'th objective.

        :return: a list of cycles/chains, and the value of said cycle/chain \
        for each objective
        :rtype: list[tuple[list[Vertex], list[float]]]
        """
        return self._possible


class Pool:
    """A KEP pool."""

    def __init__(self, objectives: list[Objective]):
        # List comprehension here to create a copy of the list object
        self._objectives: list[Objective] = [obj for obj in objectives]

    def solve_single(self, instance: Instance,
                     maxCycleLength: Optional[int] = None,
                     maxChainLength: Optional[int] = None
                     ) -> Optional[Solution]:
        if maxCycleLength is None:
            maxCycleLength = 3
        if maxChainLength is None:
            maxChainLength = 3
        t = thread_time()
        model = CycleAndChainModel(instance, self._objectives,
                                   maxChainLength=maxChainLength,
                                   maxCycleLength=maxCycleLength)
        times = [("Model building", thread_time() - t)]
        t = thread_time()
        solution = model.solve()
        times.append(("Model solving", thread_time() - t))
        if solution is None:
            return None
        values = model.objective_values
        exchange_values = [(exchange, model.exchange_values(exchange))
                           for exchange in model.exchanges]
        return Solution(solution, values, exchange_values, times)
