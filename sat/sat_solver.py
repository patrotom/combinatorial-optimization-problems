#!/usr/bin/env python3

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import argparse as ap

from sat.lib.data_processor import InputProcessor, OutputProcessor
from sat.lib.genetic import Genetic


def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument("id", help="id of the data set")
    return parser.parse_args()


def run():
    id = parse_args().id
    opts = {"p": 200, "g": 200, "c": 0.99, "m": 0.1}
    insts = InputProcessor(id).prepare_instances()
    sols = []

    for inst in insts:
        gen = Genetic(inst, opts)
        gen.run()
        sol = gen.sol
        sols.append(gen.sol)


if __name__ == "__main__":
    run()
