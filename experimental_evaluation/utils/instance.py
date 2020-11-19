from math import floor
from functools import reduce 


class Instance:
    def __init__(self, id, size, capacity, items):
        self.id = int(id)
        self.size = int(size)
        self.capacity = int(capacity)
        self.items = items

    def prices_sum(self, i=0):
        return sum(item.price for item in self.items[i:])
    
    def sort_items(self):
        self.items.sort(key=lambda i: i.price / i.weight, reverse=True)
