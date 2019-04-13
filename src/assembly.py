#!/usr/bin/env python3
from interfaces import *

class QASM(AsmProgram):
    """ QCC Wrapper for QisKit's Python QASM representation """

    def __init__(self, program=""):
        self.program = program
        raise NotImplementedError

    def get_intermediary_compiler(self):
      """ Returns an intermediary language compiler for
      the given assembly language of the subclass """
      pass

class Quil(AsmProgram):
    """ QCC Wrapper for Rigetti's Python Quil representation """

    def __init__(self, program=""):
        self.program = program
        raise NotImplementedError

    def get_intermediary_compiler(self):
      """ Returns an intermediary language compiler for
      the given assembly language of the subclass """
      pass
