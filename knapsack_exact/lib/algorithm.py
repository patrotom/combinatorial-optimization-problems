import abc
from timeit import default_timer as timer
from .solution import Solution


class Algorithm:
    def __init__(self, inst):
        self.inst = inst
        self.sol = Solution(inst.size)

    def solve(self):
        conf = self.sol.conf
        start = timer()
        self._solve(conf, 0, 0, 0)
        end = timer()
        self.sol.solvable = self.inst.capacity == self.sol.weight
        self.sol.time = end - start
        self.sol.conf = "".join(map(lambda x: str(x), self.sol.conf))

    @abc.abstractmethod
    def _solve(self, conf, i, weight, price):
        pass
