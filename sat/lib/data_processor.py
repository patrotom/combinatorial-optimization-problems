import csv
import glob
from pathlib import Path

from sat.lib.instance import Instance 


class InputProcessor:
    def __init__(self, id):
        self.id = id
    
    def prepare_instances(self):
        l = self.id.split("-")[-1]
        pref = f"data/input/wuf-{l}/{self.id}"
        i_paths = list(glob.iglob(f"{pref}/*.mwcnf"))
        insts = []

        with open(f"{pref}-opt.dat", "r") as s_file:
            s_lines = s_file.read().splitlines()
            for i_path in i_paths:
                with open(i_path, "r") as i_file:
                    insts.append(self.__parse_inst(i_file, s_lines))

        return insts

    def __parse_inst(self, i_file, s_lines):
        lines = i_file.read().splitlines()
        vars_num = lines[7].split()[2]
        weights = lines[9].split()[1:-1]
        clauses = []
        for line in lines[11:]:
            clause = line.lstrip().split()[:-1]
            clauses.append(list(map(lambda x: int(x), clause)))
        
        inst_id = lines[8].split(" ")[-1].split("/")[1].rstrip(".cnf")

        opt_sum = next(
            (x for x in s_lines if x.split(" ")[0] == inst_id)
        ).split(" ")[1]

        return Instance(vars_num, weights, clauses, opt_sum)


class OutputProcessor:
    def __init__(self, sols, id):
        self.sols = sols
        self.id = id

    def write_sols(self):
        l = self.id.split("-")[-1]
        dir_path = f"data/output/wuf-{l}/{id}"
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        of_path = self.__prepare_file_path(dir_path)

        with open(of_path, "w") as o_file:
            writer = csv.writer(o_file, delimiter=";")
            writer.writerow(list(vars(self.sols[0]).keys()))
            for i in range(self.sols):
                self.sols[i].conf = "".join(str(x) for x in self.sols[i].conf)
                csv_data = list(vars(self.sols[i]).values())
                writer.writerow(csv_data)

    def __prepare_file_path(self, dir_path):
        names = list(glob.iglob(f"{dir_path}/*.csv"))
        if names == []:
            num = 0
        else:
            max_num = max(
                names, key=lambda x: int(x.split("-")[-1].rstrip(".csv"))
            ).split("-")[-1].rstrip(".csv")
            num = int(max_num) + 1

        return f"{dir_path}/{self.id}-sol-{num}.csv"
