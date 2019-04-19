#!/usr/bin/env python3
import langs
import direct_compilers, compilers_to_intermediary

from interfaces import *


class QASM(AsmProgram):
    """ QCC Wrapper for QisKit's Python QASM representation """

    def __init__(self, program=""):
        self.program = program

    @staticmethod
    def get_intermediary_compiler():
        return compilers_to_intermediary.QASM_Intermediary_Compiler()

    @staticmethod
    def get_direct_compiler(target_lang):
        if target_lang in langs.ibm_langs:
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
        raise ValueError("Requested direct compiler does not exist.")
