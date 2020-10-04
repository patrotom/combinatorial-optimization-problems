#!/usr/bin/env python3

import sys
import argparse as ap
from utils.input_processor import InputProcessor
from utils.output_formatter import OutputFormatter
from lib.brute_force import BruteForce
from lib.branch_and_bound import BranchAndBound


def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument("input_file", help="path to the input file")
    parser.add_argument("-b", "--branch-and-bound", action='store_true',
                        help="use B&B instead of the brute force")

    return parser.parse_args()


def knapsack_exact():
    args = parse_args()
    if args.branch_and_bound:
        solver_class = BranchAndBound
    else:
        solver_class = BruteForce

    sols = []

    with open(args.input_file, "r") as i_file:
        insts = InputProcessor(i_file).prepare_instances()
        for inst in insts:
            solver = solver_class(inst)
            solver.solve()
            sols.append(solver.sol)

    alg = "bb" if args.branch_and_bound else "bf"
    OutputFormatter(sols, args.input_file, alg).save_data()


if __name__ == "__main__":
    try:
        knapsack_exact()
    except FileNotFoundError as e:
        print(e)
