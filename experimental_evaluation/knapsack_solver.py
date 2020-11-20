import subprocess
import sys
import os
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
import numpy as np

from lib.branch_and_bound import BranchAndBound
from lib.greedy import Greedy, ReduxGreedy
from lib.dynamic_prog import DynamicWeight
from lib.solution import Solution, ErrorSolution
from utils.input_processor import InputProcessor


class KnapsackSolver:
    def __init__(self, version, gen_opts):
        self.version = version
        self.gen_opts = gen_opts
        self.valid = True

    def run(self):
        self.__generate_instances()
        self.sols = self.__run()

    def run_perms(self):
        self.perm_sols = []
        self.__generate_instances()
        self.sols = self.__run()
        perm_instances = self.__generate_permurations()

        for perm_instance in perm_instances:
            self.instances = perm_instance
            self.perm_sols.append(self.__run())

    def time_mean(self):
        times = list(map(lambda x: x.time, self.sols))
        return np.mean(times) * 1000

    def perm_time_means(self):
        times = []
        for perm_sol in self.perm_sols:
            t = list(map(lambda x: x.time, perm_sol))
            times.append(np.mean(t) * 1000)
        return times
    
    def rel_err_mean(self):
        rel_errs = list(map(lambda x: x.rel_err, self.sols))
        return np.mean(rel_errs) * 1000
    
    def perm_rel_err_means(self):
        rel_errs = []
        for perm_sol in self.perm_sols:
            t = list(map(lambda x: x.rel_err, perm_sol))
            rel_errs.append(np.mean(t) * 1000)
        return rel_errs

    def __run(self):
        solv_class = self.__solver_class()
        solu_class = self.__solution_class()

        sols = []

        for inst in self.instances:
            solver = solv_class(inst, solu_class)
            solver.run()
            sols.append(solver.sol)

        return sols

    def __solver_class(self):
        switcher = {
            "bb": BranchAndBound,
            "dw": DynamicWeight,
            "gh": Greedy,
            "rgh": ReduxGreedy,
        }
        return switcher.get(self.version, BranchAndBound)

    def __solution_class(self):
        if self.version in ["gh", "rgh"]:
            return ErrorSolution
        else:
            return Solution

    def __generate_instances(self):
        if not type(self.gen_opts) is dict:
            self.valid = False
            self.instances = []
            return

        command = self.__generate_command()
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            self.valid = False
            self.instances = []
            return

        self.instances = InputProcessor(result.stdout).prepare_instances()
        self.stdout = result.stdout
    
    def __generate_permurations(self):
        file_dir = os.path.dirname(__file__)
        rel_path = "generator/kg_perm"
        command = [os.path.join(file_dir, rel_path), "-d", "100", "-N", "5"]
        
        result = subprocess.run(
            command, capture_output=True, text=True,
            input=self.stdout, encoding="ascii"
        )

        return InputProcessor(result.stdout).prepare_permutations(5)

    def __generate_command(self):
        file_dir = os.path.dirname(__file__)
        rel_path = "generator/kg2"
        command = [os.path.join(file_dir, rel_path)]
        for opt, val in self.gen_opts.items():
            if type(val) is float:
                val = "{:.20f}".format(val)
            else:
                val = str(val)
            command.extend([f"-{opt}", val])
        
        return command
