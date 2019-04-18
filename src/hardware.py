#!/usr/bin/env python3
from interfaces import *

# TODO -- Come up with actual list of hardwares and implement
class IBM(HardwareContrainedProgram):
    """ Example class for assembly contrained to a specific hardware """

    def __init__(self, program=""):
        ## TODO: Implement
        self.program = program

    def __str__(self):
        return self.program
