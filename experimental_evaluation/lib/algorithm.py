import abc
from timeit import default_timer as timer
from .solution import Solution


class Algorithm:
    def __init__(self, inst, solution_class):
        self.inst = inst
        self.sol = solution_class(inst.size)

    def run(self):
        start = timer()
        self.solve(self.sol.conf, 0, 0, 0)
        end = timer()

        self.sol.time = end - start
        self.sol.conf = "".join(map(lambda x: str(x), self.sol.conf))

    @abc.abstractmethod
    def solve(self, conf, i, weight, price):
        pass
