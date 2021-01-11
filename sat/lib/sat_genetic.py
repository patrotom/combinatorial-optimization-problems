from sat.lib.solution import Solution


class SatGenetic:
    def __init__(self, inst):
        self.inst = inst
        self.opts = inst.opts
        self.sol = Solution(inst.var_num)

    def run(self):
        pass

    

