#!/usr/bin/env python3

import sys
import os
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import argparse as ap

from genetic.lib.ga import Genetic
from genetic.lib.instance import Instance
from genetic.lib.item import Item

# def parse_args():
#     parser = ap.ArgumentParser()
#     parser.add_argument("input_file", help="path to the input file")
#     parser.add_argument("solution_file", help="path to the solution file")
#     parser.add_argument("-p", required=True, type=int, help="population size")
#     parser.add_argument("-g", required=True, type=int, help="number of generations")
#     parser.add_argument("-st", required=True, choices=['tour', 'rank', 'scale'],
#                                               help="selection type")
#     parser.add_argument("-cp", required=True, type=float, help="crossover probability")
#     parser.add_argument("-ct", required=True, type=float, help="crossover type")
#     parser.add_argument("-m", required=True, type=float, help="mutation rate")

#     return parser.parse_args()


# def run():
#     args = parse_args()
    

if __name__ == "__main__":
    id = 1
    size = 40
    capacity = 3429

    data = [36, 3, 43, 1129, 202, 94, 149, 2084, 28, 646, 54, 737, 147, 300, 151, 605, 16, 1420, 214, 1142, 68, 2253, 238, 1541, 245, 1413, 8, 221, 7, 1939, 137, 1284, 165, 1174, 183, 500, 122, 1525, 23, 1003, 136, 221, 200, 1755, 127, 741, 173, 80, 165, 2339, 130, 834, 33, 75, 213, 1676, 43, 1428, 137, 875, 48, 1503, 245, 1599, 198, 415, 235, 147, 209, 2072, 18, 883, 74, 1635, 186, 405, 220, 1324, 59, 492]

    items = []
    index = 0

    for i in range(0, len(data), 2):
        item = Item(data[i], data[i+1], index)
        items.append(item)
        index += 1

    inst = Instance(id, size, capacity, items, 38667)

    opts = {
        "p": 50,
        "g": 100,
        "cp": 0.9,
        "m": 0.01
    }

    gen = Genetic(inst, opts)
    gen.run()

    pass

    # try:
    #     run()
    # except FileNotFoundError as e:
    #     print(e)
    #     exit(1)
