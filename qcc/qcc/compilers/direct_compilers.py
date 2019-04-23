#!/usr/bin/env python3
import qiskit
from pyquil import get_qc

import qcc.hardware.ibmq
from qcc.interfaces import *
from qcc.hardware import *

## TODO: complete and implement this set of compilers
class QASM_IBM_Compiler(Compiler):
    """ Compiles QASM to IBM """

    def compile(self, source, target_lang):
        ## TODO: Implement this
        r = qiskit.compile(source.circuit, ibmq.backends[target_lang])
        return IBM("TODO(Juan)")

class Quil_Rigetti_Compiler(Compiler):
    """ Compiles Quil to Rigetti """

    def compile(self, source, target_lang):
        qc = get_qc(target_lang)
        qc.compiler.quil_to_native_quil(source.program)
        return Rigetti("TODO")
