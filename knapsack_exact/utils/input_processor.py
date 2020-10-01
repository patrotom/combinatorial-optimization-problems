from .item import Item
from .instance import Instance


class InputProcessor:
    def __init__(self, i_file):
        self.i_file = i_file

    def prepare_instances(self):
        instances = []

        for inst in self.i_file:
            vars = inst.strip().split(' ')
            id, size, cap, min_price = vars[0:4]
            items = self._prepare_items(vars[4:])
            inst = Instance(id, size, cap, min_price, items)
            instances.append(inst)

        return instances
    
    def _prepare_items(self, data):
        items = []
        for i in range(0, len(data), 2):
            item = Item(data[i], data[i+1])
            items.append(item)
        return items
