from math import floor
from functools import reduce 


class Instance:
    def __init__(self, id, size, capacity, items, opt_price):
        self.id = int(id)
        self.size = int(size)
        self.capacity = int(capacity)
        self.items = items
        self.opt_price = int(opt_price)
        self.eps = 0

    def prices_sum(self, i=0):
        return sum(item.price for item in self.items[i:])
    
    def sort_items(self):
        self.items.sort(key=lambda i: i.price / i.weight, reverse=True)

    def floor_prices(self, k):
        for item in self.items:
            item.price = int(floor(item.price / k))
            if item.price < 1:
                item.price = 1
