#!/usr/bin/env python3

import sys
import argparse as ap
from utils.input_processor import InputProcessor
from utils.output_formatter import OutputFormatter
from lib.brute_force import BruteForce
from lib.branch_and_bound import BranchAndBound
from lib.algorithm import ComputationError
from lib.solution import Solution


def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument("input_file", help="path to the input file")
    parser.add_argument("solution_file", help="path to the solution file")
    versions = ["bf", "bb", "dp", "gh", "rgh", "fptas"]
    help = (
        "version of the algorithm - "
        "bf (Brute Force), "
        "bb (Branch & Bound), "
        "dp (Dynamic Programming), "
        "gh (Greedy Heuristic), "
        "rgh (Redux Greedy Heuristic), "
        "fptas (FPTAS Algorithm)"
    )
    parser.add_argument(
        "-v", "--version",
        required=True,
        choices=versions,
        help=help
    )

    return parser.parse_args()


def solver_class(v):
    switcher = {
        "bf": BruteForce,
        "bb": BranchAndBound,
        # "dp": DynamicProg,
        # "gh": Greedy,
        # "rgh": ReduxGreedy,
        # "fptas": Fptas,
    }
    return switcher.get(v, BruteForce)


def knapsack_heuristic():
    args = parse_args()
    sc = solver_class(args.version)

    sols = []

    with open(args.input_file, "r") as i_file, open(args.solution_file, "r") as s_file:
        insts = InputProcessor(i_file, s_file).prepare_instances()

    for inst in insts:
        solver = sc(inst)
        solver.solve()
        sols.append(solver.sol)

    OutputFormatter(sols, args.input_file, args.version).save_data()


if __name__ == "__main__":
    try:
        knapsack_heuristic()
    except (FileNotFoundError, ComputationError) as e:
        print(e)
        exit(1)
