#!/usr/bin/env python3


class HardwareConstrainedProgramInfo:
    def __init__(self, num_insts=None, num_2_qubit_gates=None):
        self.num_insts = num_insts
        self.num_2_qubit_gates = num_2_qubit_gates
        pass

    def score(self, metric='num_2_qubit_gates'):
        if getattr(self, metric, None) is None:
            raise NameError("Specified metric does not exist.")
        else:
            return getattr(self, metric)

    def __str__(self):
        return f"Number of instructions: {self.num_insts}\n" \
               f"Number of 2-qubit gates: {self.num_2_qubit_gates}"
