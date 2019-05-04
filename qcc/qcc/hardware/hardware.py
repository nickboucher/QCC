#!/usr/bin/env python3
from qcc.interfaces import HardwareConstrainedProgram
from qcc.hardware.hardware_program_statistics import HardwareConstrainedProgramInfo


class IBM(HardwareConstrainedProgram):
    """ Represents an IBM quantum device """

    def __init__(self, circuit):
        self.program = circuit

    def __str__(self):
        return self.program.qasm()

    def get_statistics(self) -> HardwareConstrainedProgramInfo:
        return HardwareConstrainedProgramInfo(num_insts=self.program.size())


class Rigetti(HardwareConstrainedProgram):
    """ Represents a Rigetti quantum device """

    def __init__(self, quil_program):
        self.program = quil_program

    def __str__(self):
        return self.program.out()

    def get_statistics(self) -> HardwareConstrainedProgramInfo:
        insts = self.program.instructions
        return HardwareConstrainedProgramInfo(num_insts=len(insts))
