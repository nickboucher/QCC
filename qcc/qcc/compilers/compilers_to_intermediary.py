#!/usr/bin/env python3
from qcc.interfaces import *
from qcc.intermediary_lang import *

## TODO: complete and implement this set of compilers
class QASM_Intermediary_Compiler(Compiler):
    """ Compiles QASM to Intermediary Language """

    def compile(self, source, target_lang):
        ## Implement this
        return IntermediaryProgram("TODO")

class Quil_Intermediary_Compiler(Compiler):
    """ Compiles Quil to Intermediary Language """

    def compile(self, source, target_lang):
        ## Implement this
        return IntermediaryProgram("TODO")
