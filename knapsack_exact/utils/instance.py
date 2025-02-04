from functools import reduce 


class Instance:
    def __init__(self, id, size, capacity, minimal_price, items, opt_price):
        self.id = int(id)
        self.size = int(size)
        self.capacity = int(capacity)
        self.minimal_price = int(minimal_price)
        self.items = items
        self.opt_price = int(opt_price)

    def prices_sum(self, i=0):
        prices = map(lambda x: x.price, self.items[i:])
        return reduce(lambda x, y: x + y, prices)
