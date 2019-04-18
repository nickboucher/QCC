#!/usr/bin/env python3
from interfaces import *
from intermediary_compilers import *

class QASM(AsmProgram):
    """ QCC Wrapper for QisKit's Python QASM representation """

    def __init__(self, program=""):
        self.program = program

    @staticmethod
    def get_intermediary_compiler():
      return QASM_Intermediary_Compiler()

    @staticmethod
    def direct_compile(src, target_backend, ibmq_session):
        # TODO: actually compile using qiskit API
        return "TODO(Juan)"


class Quil(AsmProgram):
    """ QCC Wrapper for Rigetti's Python Quil representation """

    def __init__(self, program=""):
        self.program = program

    @staticmethod
    def get_intermediary_compiler():
        return Quil_Intermediary_Compiler()
