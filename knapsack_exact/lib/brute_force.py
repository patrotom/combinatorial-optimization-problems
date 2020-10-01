from solution import Solution


class BruteForce:
    def __init__(self, inst):
        self.inst = inst
        self.sol = Solution(inst.size)

    def solve(self):
        conf = self.sol.conf
        self._solve(conf, 0, 0, 0)

    def _solve(self, conf, i, weight, price):
        if i == self.inst.size:
            if price >= self.inst.price:
                self.inst.price = price
                self.inst.conf = conf[:]
            return
        
        new_weight = self.inst.items[i].weight + weight

        conf[i] = 1
        if new_weight <= self.inst.capacity:
            new_price = self.inst.items[i].price + price
            self._solve(conf, i + 1, new_weight, new_price)
        
        conf[i] = 0
        self._solve(conf, i + 1, weight, price)
