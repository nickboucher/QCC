#!/usr/bin/env python3
from interfaces import *
from intermediary_compilers import *

class QASM(AsmProgram):
    """ QCC Wrapper for QisKit's Python QASM representation """

    def __init__(self, program=""):
        self.program = program

    def get_intermediary_compiler(self):
      return QASM_Intermediary_Compiler()

class Quil(AsmProgram):
    """ QCC Wrapper for Rigetti's Python Quil representation """

    def __init__(self, program=""):
        self.program = program

    def get_intermediary_compiler(self):
        return Quil_Intermediary_Compiler()
