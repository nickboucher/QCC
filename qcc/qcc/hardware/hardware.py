#!/usr/bin/env python3
from qcc.interfaces import HardwareConstrainedProgram
from qcc.hardware.hardware_program_statistics import HardwareConstrainedProgramInfo


# TODO -- Come up with actual list of hardwares and implement
class IBM(HardwareConstrainedProgram):
    """ Represents an IBM quantum device """

    def __init__(self, circuit):
        # TODO: Implement
        self.program = circuit

    def __str__(self):
        return self.program.qasm()

    def get_statistics(self) -> HardwareConstrainedProgramInfo:
        # TODO: implement
        return HardwareConstrainedProgramInfo(num_insts=self.program.size())


class Rigetti(HardwareConstrainedProgram):
    """ Represents a Rigetti quantum device """

    def __init__(self, quil_program):
        # TODO: Implement
        self.program = quil_program

    def __str__(self):
        return self.program.out()

    def get_statistics(self):
        # TODO: implement
        pass
