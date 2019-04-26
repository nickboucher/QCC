#!/usr/bin/env python3
from pyquil import Program
from qcc import config
from qcc.compilers import direct_compilers
from qcc.compilers import compilers_to_intermediary
from qcc.interfaces import AsmProgram


class Quil(AsmProgram):
    """ QCC Wrapper for Rigetti's Python Quil representation """

    def __init__(self, program_str=""):
        self.program = Program(program_str)

    @staticmethod
    def get_intermediary_compiler():
        return compilers_to_intermediary.Quil_Intermediary_Compiler()

    @staticmethod
    def get_direct_compiler(target_lang):
        if target_lang in config.rigetti_langs:
            return direct_compilers.Quil_Rigetti_Compiler()
        else:
            raise ValueError("Requested direct compiler does not exist.")
