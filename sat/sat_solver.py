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
    parser.add_argument("set_id", help="id of the data set")
    versions = ["t1", "t2", "c1", "c2"]
    parser.add_argument(
        "-v", "--version",
        required=True,
        choices=versions,
        help="version of the algorithm run"
    )

    return parser.parse_args()


def tune_params1(set_id, insts, version):
    opts = {"p": 200, "g": 200, "pan": False, "war": False}
    cs = [0.97, 0.99, 0.999]
    ms = [0.01, 0.05, 0.1]

    for c in cs:
        for m in ms:
            opts["c"] = c
            opts["m"] = m
            run(opts, insts, set_id, version)


def run(opts, insts, set_id, version):
    sols = []

    for inst in insts:
        gen = Genetic(inst, opts)
        gen.run()
        sols.append(gen.sol)

    OutputProcessor(sols, set_id, opts, version).write_sols()


def main():
    args = parse_args()
    set_id = args.set_id
    version = args.version
    insts = InputProcessor(set_id).prepare_instances()

    if version == "t1":
        tune_params1(set_id, insts, version)


if __name__ == "__main__":
    main()
