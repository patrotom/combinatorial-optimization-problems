#!/usr/bin/env python3

import sys
import argparse as ap
from utils.input_processor import InputProcessor
from lib.brute_force import BruteForce


def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument("input_file", help="path to the input file")
    parser.add_argument("-b", "--branch-and-bound", action='store_true',
                        help="use B&B instead of the brute force")

    return parser.parse_args()


def knapsack_exact():
    args = parse_args()
    if args.branch_and_bound:
        pass
    else:
        solver_class = BruteForce

    with open(args.input_file, "r") as i_file:
        insts = InputProcessor(i_file).prepare_instances()
        for inst in insts:
            solver = solver_class(inst)
            solver.solve()
            sol = solver.sol
            print(sol.solvable, sol.conf, sol.price, sol.time, sol.complexity)


if __name__ == "__main__":
    knapsack_exact()
