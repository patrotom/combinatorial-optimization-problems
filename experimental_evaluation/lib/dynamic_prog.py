from .algorithm import Algorithm


class DynamicWeight(Algorithm):
    def solve(self, *_):
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
        self.sol.conf = self.__construct_conf(capacity)

    def __construct_conf(self, capacity):
        conf = []

        for i in range(self.inst.size, 0, -1):
            if self.table[i][capacity] == self.table[i - 1][capacity]:
                conf.append(0)
            else:
                conf.append(1)
                capacity -= self.inst.items[i - 1].weight

        conf.reverse()

        return conf
