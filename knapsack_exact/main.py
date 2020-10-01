#!/usr/bin/env python3

import sys
from utils.input_processor import InputProcessor


def main():
    fname = sys.argv[1]
    with open(fname, "r") as i_file:
        ip = InputProcessor(i_file)
        print(ip.prepare_instances())


if __name__ == "__main__":
    main()
