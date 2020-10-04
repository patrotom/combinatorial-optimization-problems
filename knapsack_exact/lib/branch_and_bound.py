from .algorithm import Algorithm


class BranchAndBound(Algorithm):
    def _solve(self, conf, i, weight, price):
        if i == self.inst.size:
            self.sol.complexity += 1
            if price >= self.sol.price:
                self.sol.price = price
                self.sol.conf = conf.copy()
            return

        new_weight = self.inst.items[i].weight + weight
        new_price = self.inst.items[i].price + price
        upper_bound = price + self.inst.prices_sum(i=i)

        conf[i] = 1
        if (new_weight <= self.inst.capacity) and (upper_bound >= self.sol.price):
            self._solve(conf, i + 1, new_weight, new_price)

        conf[i] = 0
        self._solve(conf, i + 1, weight, price)
