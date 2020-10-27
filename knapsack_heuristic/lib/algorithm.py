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

        self._determine_validity()
        self.sol.time = end - start
        self.sol.conf = "".join(map(lambda x: str(x), self.sol.conf))

    @abc.abstractmethod
    def _solve(self, conf, i, weight, price):
        pass

    def _determine_validity(self):
        alg_class = self.__class__.__name__
        if (alg_class in ['Greedy', 'ReduxGreedy'] and
                self.sol.price != self.inst.opt_price):
            self.sol.valid = False
        elif self.sol.price != self.inst.opt_price:
            raise ComputationError(self.inst.id, self.sol.price)


class ComputationError(Exception):
    def __init__(self, id, price):
        self.message = f"Incorrect result '{price}' (ID {id})"
        super().__init__(self.message)

    def __str__(self):
        return self.message
