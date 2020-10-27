import math
from .algorithm import Algorithm


class DynamicProg(Algorithm):
    def _solve(self, *_):
        prices_sum = self.inst.prices_sum()
        rows, cols = (prices_sum + 1, self.inst.size + 1)
        self._prepare_table(rows, cols)

        for i in range(1, cols):
            for j in range(1, rows):
                self.sol.complexity += 1

                weight = self.table[j][i-1]
                idx = j - self.inst.items[i - 1].price

                if idx < 0:
                    self.table[j][i] = weight
                elif self.table[idx][i - 1] == math.inf:
                    self.table[j][i] = min(weight, self.table[idx][i - 1])
                else:
                    self.table[j][i] = min(
                        weight,
                        self.table[idx][i - 1] + self.inst.items[i - 1].weight
                    )
        
        price, price_idx = self._find_optimal_price()
        conf = self._construct_conf(price_idx)

        self.sol.price = price
        self.sol.conf = conf

    def _prepare_table(self, rows, cols):
        self.table = [[0 for i in range(cols)] for j in range(rows)]
        
        for i in range(1, rows):
            self.sol.complexity += 1
            self.table[i][0] = math.inf
        
        for i in range(1, cols):
            self.sol.complexity += 1
            if self.inst.items[i - 1].price == 1:
                self.table[1][i] = self.inst.items[i - 1].weight
            else:
                self.table[1][i] = math.inf
    
    def _find_optimal_price(self):
        price = 0
        price_idx = 0

        for i in range(len(self.table) - 1, -1, -1):
            self.sol.complexity += 1
            price_idx = i
            if self.table[i][self.inst.size] <= self.inst.capacity:
                price = i
                break
        
        return (price, price_idx)
    
    def _construct_conf(self, price_idx):
        size = self.inst.size
        conf = [0] * size

        while price_idx > 0:
            self.sol.complexity += 1
            size -= 1
            if self.table[price_idx][size + 1] != self.table[price_idx][size]:
                price_idx -= self.inst.items[size].price
                conf[size] = 1

        return conf
