from .item import Item
from .instance import Instance


class InputProcessor:
    def __init__(self, stdout):
        self.stdout = stdout

    def prepare_instances(self):
        instances = []
        lines = self.stdout.split("\n")[:-1]
        for line in lines:
            instances.append(self.__prepare_instance(line))

        return instances

    def prepare_permutations(self, number):
        permutations = [[] for x in range(number)]
        lines = self.stdout.split("\n")[:-1]
        i = 0
        for line in lines:
            if i == number:
                i = 0
            permutations[i].append(self.__prepare_instance(line))
            i += 1
        
        return permutations

    def __prepare_instance(self, line):
        i_vars = line.strip().split(' ')
        id, size, cap = i_vars[0:3]
        items = self.__prepare_items(i_vars[3:])
        inst = Instance(id, size, cap, items)
        return inst
    
    def __prepare_items(self, data):
        items = []
        index = 0
        for i in range(0, len(data), 2):
            item = Item(data[i], data[i+1], index)
            items.append(item)
            index += 1
        return items
