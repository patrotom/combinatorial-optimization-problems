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
    versions = ["t1", "t2", "c1", "c2", "c3"]
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


def tune_params2(set_id, insts, version):
    opts = {"c": 0.999, "m": 0.10, "pan": False, "war": False}
    ps = [200, 350, 500]
    gs = [200, 350, 500]

    for p in ps:
        for g in gs:
            opts["p"] = p
            opts["g"] = g
            run(opts, insts, set_id, version)


def compute1(set_id, insts, version):
    opts = {"p": 500, "g": 200, "c": 0.999, "m": 0.1, "pan": False, "war": False}
    run(opts, insts, set_id, version)


def compute2(set_id, insts, version):
    opts = {"p": 500, "g": 200, "c": 0.999, "m": 0.1, "pan": True, "war": False}
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
    elif version == "t2":
        tune_params2(set_id, insts, version)
    elif version == "c1":
        compute1(set_id, insts, version)
    elif version == "c2":
        compute2(set_id, insts, version)


if __name__ == "__main__":
    main()
