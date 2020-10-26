from .item import Item
from .instance import Instance


class InputProcessor:
    def __init__(self, i_file, s_file):
        self.i_file = i_file
        self.s_file = s_file

    def prepare_instances(self):
        instances = []

        opt_prices = self._prepare_opt_prices()

        for i_line in self.i_file:
            i_vars = i_line.strip().split(' ')
            id, size, cap = i_vars[0:3]
            items = self._prepare_items(i_vars[3:])
            opt_price = opt_prices[abs(int(id))]

            inst = Instance(id, size, cap, items, opt_price)
            instances.append(inst)

        return instances
    
    def _prepare_items(self, data):
        items = []
        for i in range(0, len(data), 2):
            item = Item(data[i], data[i+1])
            items.append(item)
        return items

    def _prepare_opt_prices(self):
        opt_prices = {}

        for s_line in self.s_file:
            s_vars = s_line.strip().split(' ')
            opt_prices[int(s_vars[0])] = s_vars[2]

        return opt_prices
