import math
from copy import deepcopy
from .algorithm import Algorithm
from .solution import Solution


class DynamicPrice(Algorithm):
    def _solve(self, *_):
        prices_sum = self.inst.prices_sum()
        rows, cols = (prices_sum + 1, self.inst.size + 1)
        self._prepare_table(rows, cols)

        for i in range(1, cols):
            for j in range(1, rows):
                left = self.table[i - 1][j]
                left_b = self.table[i - 1][j - self.inst.items[i - 1].price]
                self.table[i][j] = min(
                    left,
                    left_b + self.inst.items[i - 1].weight
                )

        self.sol.price = self._find_optimal_price(prices_sum)
        self.sol.conf = self._construct_conf(self.sol.price)

    def _prepare_table(self, rows, cols):
        self.table = [
            [None if x > 0 else 0 for x in range(rows)] if x > 0 \
                else [math.inf if x > 0 else 0 for x in range(rows)] \
                    for x in range(cols)
        ]
    
    def _find_optimal_price(self, prices_sum):
        price = 0

        for i, w in enumerate(reversed(self.table[self.inst.size])):
            if w is not None and 0 < w <= self.inst.capacity:
                price = prices_sum - i
                break
        
        return price
    
    def _construct_conf(self, price):
        conf = []

        for i in range(self.inst.size, 0, -1):
            if self.table[i][price] == self.table[i - 1][price]:
                conf.append(0)
            else:
                conf.append(1)
                price -= self.inst.items[i - 1].price

        conf.reverse()

        return conf


class DynamicWeight(Algorithm):
    def _solve(self, *_):
        capacity = self.inst.capacity
        size = self.inst.size
        self.table = [[0 for x in range(capacity + 1)] for x in range(size + 1)]

        for i in range(size + 1):
            for w in range(capacity + 1):
                weight = self.inst.items[i - 1].weight
                price = self.inst.items[i - 1].price

                if i == 0 or w == 0:
                    self.table[i][w] = 0
                elif weight <= w:
                    self.table[i][w] = max(
                        price + self.table[i - 1][w - weight],
                        self.table[i - 1][w]
                    )
                else:
                    self.table[i][w] = self.table[i - 1][w]

        self.sol.price = self.table[size][capacity]
        self.sol.conf = self._construct_conf(capacity)

    def _construct_conf(self, capacity):
        conf = []

        for i in range(self.inst.size, 0, -1):
            if self.table[i][capacity] == self.table[i - 1][capacity]:
                conf.append(0)
            else:
                conf.append(1)
                capacity -= self.inst.items[i - 1].weight

        conf.reverse()

        return conf


class Fptas(Algorithm):
    def _solve(self, *_):
        removed_items = self._remove_large_items()
        max_price = max(self.inst.items, key=lambda x: x.price).price
        k = (self.inst.eps * max_price) / self.inst.size
        original_prices = list(map(lambda x: x.price, self.inst.items))
        self.inst.floor_prices(k)

        dynamic_price = DynamicPrice(self.inst, Solution)
        dynamic_price._solve()

        dyn_conf = dynamic_price.sol.conf
        self.sol.time = dynamic_price.sol.time
        self.sol.price = sum(
            [p for i, p in enumerate(original_prices) if dyn_conf[i] == 1]
        )

        self.sol.conf = self._construct_conf(removed_items, dyn_conf)

    def _remove_large_items(self):
        removed_items = []
        for i, item in enumerate(self.inst.items):
            if item.weight > self.inst.capacity:
                removed_items.append(self.inst.items.pop(i))
                self.inst.size -= 1

        return removed_items

    def _construct_conf(self, removed_items, conf):
        for item in removed_items:
            conf.insert(item.index, 0)

        return conf
