from .algorithm import Algorithm


class Greedy(Algorithm):
    def _solve(self, *_):
        self.inst.sort_items()
        capacity = self.inst.capacity
        price = 0

        for item in self.inst.items:
            self.sol.complexity += 1
            if capacity >= item.weight:
                price += item.price
                capacity -= item.weight
            else:
                break
        
        self.sol.price = price
