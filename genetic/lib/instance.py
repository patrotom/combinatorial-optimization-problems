class Instance:
    def __init__(self, id, size, capacity, items, opt_price):
        self.id = int(id)
        self.size = int(size)
        self.capacity = int(capacity)
        self.items = items
        self.opt_price = int(opt_price)

    def calc_price(self, conf):
        price = 0
        for i in range(self.size):
            price += conf[i] * self.items[i].price
        
        return price

    def calc_weight(self, conf):
        weight = 0
        for i in range(self.size):
            weight += conf[i] * self.items[i].weight
        
        return weight
