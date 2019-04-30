#!/usr/bin/env python3
import qcc.config
from qcc.assembly.quil import Quil
from qcc.interfaces import Program
from qcc.compilers.compilers_from_intermediary import \
    Intermediary_IBM_Compiler, Intermediary_Rigetti_Compiler


class IntermediaryProgram(Program):
    """ Represents intermediary program used in compiling as a Quil Program"""

    def __init__(self, quil: Quil = None):
        """ Instantiate a new Intermediary Program """
        self.quil = quil

    def get_hardware_compiler(self, target_lang):
        """ Return Compiler from Intermediary Program to the
            target language """
        if target_lang not in qcc.config.hw_langs:
            raise ValueError("target_lang must be a valid hardware language")
        if target_lang in qcc.config.ibm_langs:
            return Intermediary_IBM_Compiler()
        elif target_lang in qcc.config.rigetti_langs:
            return Intermediary_Rigetti_Compiler()
        else:
            raise ValueError("Requested compiler does not exist.")
