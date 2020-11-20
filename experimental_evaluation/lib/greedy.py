from .algorithm import Algorithm
from .branch_and_bound import BranchAndBound
from .solution import Solution, ErrorSolution


class Heuristic(Algorithm):
    def _compute_rel_err(self):
        bb = BranchAndBound(self.o_inst, Solution)
        bb.run()

        max_price = max(bb.sol.price, self.sol.price)

        self.sol.rel_err = 0.0 if max_price == 0 else \
            abs(self.sol.price - bb.sol.price) / max_price

class Greedy(Heuristic):
    def solve(self, *_):
        self.inst.sort_items()
        capacity = self.inst.capacity
        price = 0

        for item in self.inst.items:
            if capacity >= item.weight:
                price += item.price
                capacity -= item.weight
                self.sol.conf[item.index] = 1
        
        self.sol.price = price


class ReduxGreedy(Heuristic):
    def solve(self, *_):
        greedy = Greedy(self.inst, ErrorSolution)
        greedy.solve()
        highest_price, index = self.__find_highest_price()

        if greedy.sol.price > highest_price:
            self.sol.price = greedy.sol.price
            self.sol.conf = greedy.sol.conf
        else:
            self.sol.price = highest_price
            self.sol.conf[index] = 1

    def __find_highest_price(self):
        highest_price = 0
        index = -1
        for item in self.inst.items:
            if item.price > highest_price and item.weight <= self.inst.capacity:
                highest_price = item.price
                index = item.index
        
        return (highest_price, index)
