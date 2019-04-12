#!/usr/bin/env python3
from interfaces import *

# TODO -- Come up with actual list of hardwares and implement
class IBM_01(HardwareContrainedProgram):
    """ Example class for assembly contrained to a specific hardware """

    def __init__(self, program=[]):
        self.program = program
        raise NotImplementedError
