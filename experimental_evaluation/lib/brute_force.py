from .algorithm import Algorithm


class BruteForce(Algorithm):
    def _solve(self, conf, i, weight, price):
        if i == self.inst.size:
            if price >= self.sol.price and weight <= self.inst.capacity:
                self.sol.price = price
                self.sol.conf = conf.copy()
            return

        new_weight = self.inst.items[i].weight + weight
        new_price = self.inst.items[i].price + price

        conf[i] = 1
        self._solve(conf, i + 1, new_weight, new_price)

        conf[i] = 0
        self._solve(conf, i + 1, weight, price)
