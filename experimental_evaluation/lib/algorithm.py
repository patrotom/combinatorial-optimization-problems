import abc
from timeit import default_timer as timer
from copy import deepcopy


class Algorithm:
    def __init__(self, inst, solution_class):
        self.inst = inst
        self.o_inst = deepcopy(inst)
        self.sol = solution_class(inst.size)

    def run(self):
        start = timer()
        self.solve(self.sol.conf, 0, 0, 0)
        end = timer()

        self.sol.time = end - start
        self.sol.conf = "".join(map(lambda x: str(x), self.sol.conf))

        alg_class = self.__class__.__name__
        if alg_class in ['Greedy', 'ReduxGreedy']:
            self._compute_rel_err()


    @abc.abstractmethod
    def solve(self, conf, i, weight, price):
        pass
    
    @abc.abstractmethod
    def _compute_rel_err(self):
        pass
