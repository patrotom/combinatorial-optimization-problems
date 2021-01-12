import csv
import glob
from pathlib import Path

from sat.lib.instance import Instance 


class InputProcessor:
    def __init__(self, set_id):
        self.set_id = set_id
    
    def prepare_instances(self):
        l = self.set_id.split("-")[-1]
        pref = f"data/input/wuf-{l}/{self.set_id}"
        i_paths = list(glob.iglob(f"{pref}/*.mwcnf"))
        insts = []

        with open(f"{pref}-opt.dat", "r") as s_file:
            s_lines = s_file.read().splitlines()
            for i_path in i_paths[:100]:
                with open(i_path, "r") as i_file:
                    insts.append(self.__parse_inst(i_path, i_file, s_lines))

        return insts

    def __parse_inst(self, i_path, i_file, s_lines):
        lines = i_file.read().splitlines()
        vars_num = lines[7].split()[2]
        weights = lines[9].split()[1:-1]
        clauses = []
        for line in lines[11:]:
            clause = line.lstrip().split()[:-1]
            clauses.append(clause)
        
        inst_id = lines[8].split(" ")[-1].split("/")[1].rstrip(".cnf")

        opt_sum = next(
            (x for x in s_lines if x.split(" ")[0] == inst_id)
        ).split(" ")[1]

        return Instance(vars_num, weights, clauses, opt_sum, i_path)


class OutputProcessor:
    def __init__(self, sols, set_id, opts, version):
        self.sols = sols
        self.set_id = set_id
        self.opts = opts
        self.version = version

    def write_sols(self):
        l = self.set_id.split("-")[-1]
        dir_path = f"data/output/{self.version}/wuf-{l}/{self.set_id}"
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        of_path = self.__prepare_file_path(dir_path)

        with open(of_path, "w") as o_file:
            writer = csv.writer(o_file, delimiter=";")
            writer.writerow(list(vars(self.sols[0]).keys()))
            for i in range(len(self.sols)):
                self.sols[i].conf = "".join(str(x) for x in self.sols[i].conf)
                csv_data = list(vars(self.sols[i]).values())
                writer.writerow(csv_data)

        self.__write_opts(of_path)

    def __write_opts(self, of_path):
        s_file = of_path.split("/")[-1]
        o_path = f"{of_path.rstrip(s_file)}{self.set_id}-opts.csv"
        
        if not Path(o_path).is_file():
            with open(o_path, "w") as o_file:
                writer = csv.writer(o_file, delimiter=";")
                header = ["fname", "p", "g", "c", "m", "pan", "war"]
                writer.writerow(header)
        
        with open(o_path, "a") as o_file:
            writer = csv.writer(o_file, delimiter=";")
            vals = [
                s_file, self.opts["p"], self.opts["g"], self.opts["c"],
                self.opts["m"], self.opts["pan"], self.opts["war"]
            ]
            writer.writerow(vals)

    def __prepare_file_path(self, dir_path):
        names = list(glob.iglob(f"{dir_path}/*-sol-*.csv"))
        if names == []:
            num = 0
        else:
            max_num = max(
                names, key=lambda x: int(x.split("-")[-1].rstrip(".csv"))
            ).split("-")[-1].rstrip(".csv")
            num = int(max_num) + 1

        return f"{dir_path}/{self.set_id}-sol-{num}.csv"
