#!/usr/bin/env python3


class HardwareConstrainedProgramInfo:
    def __init__(self, num_insts):
        # TODO: determine what statistics we want to take in
        self.num_insts = num_insts
        pass

    def score(self):
        return self.num_insts

    def __str__(self):
        return "Number of instructions: {}".format(self.num_insts)
