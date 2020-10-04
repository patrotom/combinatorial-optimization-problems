import abc
from .solution import Solution


class Algorithm:
    def __init__(self, inst):
        self.inst = inst
        self.sol = Solution(inst.size)

    def solve(self):
        conf = self.sol.conf
        self._solve(conf, 0, 0, 0)

    @abc.abstractmethod
    def _solve(self, conf, i, weight, price):
        pass
