#!/usr/bin/env python3
from qcc.interfaces import *

# TODO -- Come up with actual list of hardwares and implement
class IBM(HardwareContrainedProgram):
    """ Represents an IBM quantum device """

    def __init__(self, circuit):
        ## TODO: Implement
        self.program = circuit

    def __str__(self):
        return self.program.qasm()

    def get_statistics(self):
        # TODO: implement
        pass


class Rigetti(HardwareContrainedProgram):
    """ Represents a Rigetti quantum device """

    def __init__(self, quil_program):
        ## TODO: Implement
        self.program = quil_program

    def __str__(self):
        return self.program.out()

    def get_statistics(self):
        # TODO: implement
        pass

