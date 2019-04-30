#!/usr/bin/env python3
from qcc.interfaces import Compiler
from qcc.hardware import IBM, Rigetti


# TODO: complete and implement this set of compilers
class Intermediary_IBM_Compiler(Compiler):
    """ Compiles Intermediary Language to IBM """

    def compile(self, source, target_lang):
        # Implement this
        return IBM("TODO")


class Intermediary_Rigetti_Compiler(Compiler):
    """ Compiles Intermediary Language to Rigetti """

    def compile(self, source, target_lang):
        # Implement this
        return Rigetti("TODO")
