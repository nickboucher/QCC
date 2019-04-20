#!/usr/bin/env python3
from interfaces import *

# TODO -- Come up with actual list of hardwares and implement
class IBM(HardwareContrainedProgram):
    """ Represents an IBM quantum device """

    def __init__(self, program=""):
        ## TODO: Implement
        self.program = program

    def __str__(self):
        return self.program

class Rigetti(HardwareContrainedProgram):
    """ Represents a Rigetti quantum device """

    def __init__(self, program=""):
        ## TODO: Implement
        self.program = program

    def __str__(self):
        return self.program
