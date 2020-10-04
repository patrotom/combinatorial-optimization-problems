#!/usr/bin/env python3

import sys
from utils.input_processor import InputProcessor
from lib.brute_force import BruteForce


def main():
    fname = sys.argv[1]
    with open(fname, "r") as i_file:
        ip = InputProcessor(i_file)
        ists = ip.prepare_instances()

    for ist in ists:
        sol = BruteForce(ist)
        sol.solve()
        s = sol.sol
        print(s.solvable, s.conf, s.price)


if __name__ == "__main__":
    main()
