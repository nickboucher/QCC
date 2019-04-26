#!/usr/bin/env python3
from qcc.config import config
from qcc.interfaces import Program
from qcc.compilers.compilers_from_intermediary import Intermediary_IBM_Compiler


class IntermediaryProgram(Program):
    """ Represents intermediary program used in compiling """

    def __init__(self, program=""):
        """ Instantiate a new Intermediary Program """
        self.program = program

    def get_hardware_compiler(self, target_lang):
        """ Return Compiler from Intermediary Program to the
            target language """
        if target_lang not in config.hw_langs:
            raise ValueError("target_lang must be a valid hardware language")
        if target_lang in config.ibm_langs:
            return Intermediary_IBM_Compiler()
        else:
            raise ValueError("Requested compiler does not exist.")
