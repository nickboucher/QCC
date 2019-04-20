#!/usr/bin/env python3
import qiskit

import ibmq
from interfaces import *
from hardware import *

## TODO: complete and implement this set of compilers
class QASM_IBM_Compiler(Compiler):
    """ Compiles QASM to IBM """

    def compile(self, source, target_lang):
        ## TODO: Implement this
        qiskit.compile(source.circuit, ibmq.backends[target_lang])
        return IBM("TODO(Juan)")

class Quil_Rigetti_Compiler(Compiler):
    """ Compiles Quil to Rigetti """

    def compile(self, source, target_lang):
        ## TODO: Implement this
        return Rigetti("TODO")
