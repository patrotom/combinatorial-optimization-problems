class Solution:
    def __init__(self, size):
        self.conf = [0] * size
        self.price = 0
        self.time = 0


class ErrorSolution(Solution):
    def __init__(self, size):
        super().__init__(size)
        self.rel_err = 0.0
