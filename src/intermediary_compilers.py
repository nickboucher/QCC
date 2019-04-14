#!/usr/bin/env python3
from interfaces import *
from intermediary_lang import *

## TODO: complete and implement this set of compilers
class QASM_Intermediary_Compiler(Compiler):
    """ Compiles QASM to Intermediary Language """

    def compile(self, source):
        ## Implement this
        return IntermediaryProgram("TODO")

class Quil_Intermediary_Compiler(Compiler):
    """ Compiles Quil to Intermediary Language """

    def compile(self, source):
        ## Implement this
        return IntermediaryProgram("TODO")
