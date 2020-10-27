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


class ReduxGreedy(Algorithm):
    def _solve(self, *_):
        greedy = Greedy(self.inst)
        greedy._solve()
        greedy_price = greedy.sol.price
        highest_price, complexity = self._find_highest_price()

        self.sol.price = greedy_price if greedy_price > highest_price else highest_price
        self.sol.complexity = greedy.sol.complexity + complexity


    def _find_highest_price(self):
        highest_price = 0
        complexity = 0
        for item in self.inst.items:
            complexity += 1
            if item.price > highest_price and item.weight <= self.inst.capacity:
                highest_price = item.price
        
        return (highest_price, complexity)
