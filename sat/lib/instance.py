class Instance:
    def __init__(self, vars_num, weights, clauses, opt_sum):
        self.vars_num = int(vars_num)
        self.weights = weights
        self.clauses = clauses
        self.cls_num = len(clauses)
        self.opt_sum = int(opt_sum)
