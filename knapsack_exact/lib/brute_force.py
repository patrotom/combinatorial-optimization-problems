from .algorithm import Algorithm


class BruteForce(Algorithm):
    def _solve(self, conf, i, weight, price):
        if i == self.inst.size:
            self.sol.complexity += 1
            if price >= self.sol.price:
                self.sol.price = price
                self.sol.conf = conf.copy()
            return

        new_weight = self.inst.items[i].weight + weight

        conf[i] = 1
        if new_weight <= self.inst.capacity:
            new_price = self.inst.items[i].price + price
            self._solve(conf, i + 1, new_weight, new_price)

        conf[i] = 0
        self._solve(conf, i + 1, weight, price)
