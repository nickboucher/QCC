#!/usr/bin/env python3
from qcc.interfaces import *
from qcc.hardware import *

## TODO: complete and implement this set of compilers
class Intermediary_IBM_Compiler(Compiler):
    """ Compiles Intermediary Language to IBM """

    def compile(self, source, target_lang):
        ## Implement this
        return IBM("TODO")
