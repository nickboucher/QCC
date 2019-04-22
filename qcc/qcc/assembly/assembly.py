#!/usr/bin/env python3
from qcc.compilers import direct_compilers
from qcc import config
from qcc.compilers import compilers_to_intermediary
from qcc.interfaces import *
from qiskit.qasm import Qasm

class QASM(AsmProgram):
    """ QCC Wrapper for QisKit's Python QASM representation """

    def __init__(self, prog_str=""):
        self.program = Qasm(data=prog_str).parse()

    @staticmethod
    def get_intermediary_compiler():
        return compilers_to_intermediary.QASM_Intermediary_Compiler()

    @staticmethod
    def get_direct_compiler(target_lang):
        if target_lang in config.ibm_langs:
            return direct_compilers.QASM_IBM_Compiler()
        else:
            raise ValueError("Requested direct compiler does not exist.")


class Quil(AsmProgram):
    """ QCC Wrapper for Rigetti's Python Quil representation """

    def __init__(self, program=""):
        self.program = program

    @staticmethod
    def get_intermediary_compiler():
        return compilers_to_intermediary.Quil_Intermediary_Compiler()

    @staticmethod
    def get_direct_compiler(target_lang):
        if target_lang in config.rigetti_langs:
            return direct_compilers.Quil_Rigetti_Compiler()
        else:
            raise ValueError("Requested direct compiler does not exist.")