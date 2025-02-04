import csv, os


class OutputFormatter:
    def __init__(self, sols, if_path, alg):
        self.sols = sols
        self.if_path = if_path
        self.alg = alg

    def save_data(self):
        if self.sols == []:
            return

        of_path = self._prepare_file_path()
        with open(of_path, "w") as o_file:
            writer = csv.writer(o_file, delimiter=";")
            writer.writerow(list(vars(self.sols[0]).keys()))
            for sol in self.sols:
                csv_data = list(vars(sol).values())
                writer.writerow(csv_data)

    def _prepare_file_path(self):
        basename = os.path.basename(self.if_path).split('_')[0]
        dset_id = ''.join([i for i in basename if not i.isdigit()])
        return f"data/output/{dset_id}/{self.alg}/{basename}_out.csv"


class FPTASFormatter(OutputFormatter):
    def __init__(self, sols, if_path, alg, eps):
        super().__init__(sols, if_path, alg)
        self.eps = str(eps)
    
    def _prepare_file_path(self):
        basename = os.path.basename(self.if_path).split('_')[0]
        dset_id = ''.join([i for i in basename if not i.isdigit()])
        return f"data/output/{dset_id}/{self.alg}/{self.eps}/{basename}_out.csv"
