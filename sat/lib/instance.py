class Instance:
    def __init__(self, vars_num, weights, clauses, opt_sum, i_path):
        self.vars_num = int(vars_num)
        self.weights = [int(x) for x in weights]
        self.clauses = [[int(v) for v in c] for c in clauses]
        self.cls_num = len(clauses)
        self.opt_sum = int(opt_sum)
        self.i_path = i_path
