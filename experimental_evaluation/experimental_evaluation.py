import subprocess

from lib.brute_force import BruteForce
from lib.branch_and_bound import BranchAndBound
from lib.greedy import Greedy, ReduxGreedy
from lib.dynamic_prog import DynamicWeight
from lib.solution import Solution, ErrorSolution
from utils.input_processor import InputProcessor


class KnapsackSolver:
    def __init__(self, version, gen_opts):
        self.version = version
        self.gen_opts = gen_opts
        self.sols = []
        self.valid = True

    def run(self):
        solv_class = self.__solver_class()
        solu_class = self.__solution_class()
        self.__generate_instances()

        for inst in self.instances:
            solver = solv_class(inst, solu_class)
            solver.run()
            self.sols.append(solver.sol)
    
    def __solver_class(self):
        switcher = {
            "bf": BruteForce,
            "bb": BranchAndBound,
            "dw": DynamicWeight,
            "gh": Greedy,
            "rgh": ReduxGreedy,
        }
        return switcher.get(self.version, BruteForce)

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
        
    def __generate_command(self):
        command = ['generator/kg2']
        for opt, val in self.gen_opts.items():
            if type(val) is float:
                val = "{:.20f}".format(val)
            else:
                val = str(val)
            command.extend([f"-{opt}", val])
        
        return command
