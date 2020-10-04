class Instance:
    def __init__(self, id, size, capacity, minimal_price, items):
        self.id = int(id)
        self.size = int(size)
        self.capacity = int(capacity)
        self.minimal_price = int(minimal_price)
        self.items = items
