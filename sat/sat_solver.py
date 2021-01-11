#!/usr/bin/env python3

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import argparse as ap

from sat.lib.data_processor import InputProcessor, OutputProcessor


def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument("id", help="id of the data set")
    return parser.parse_args()


def run():
    id = parse_args().id
    insts = InputProcessor(id).prepare_instances()
    pass


if __name__ == "__main__":
    run()
