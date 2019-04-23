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
        compiled_qobj = qiskit.compile(source.circuit, ibmq.backends[target_lang])
        ## TODO: It would be nice to use qiskit.converters.qobj_to_circuits
        ##       for this. Unfortunately their code throws an error when
        ##       I try to use it.
        if len(compiled_qobj.experiments) != 1 \
           or not compiled_qobj.experiments[0].header \
           or not compiled_qobj.experiments[0].header.compiled_circuit_qasm:
            raise ValueError("Compilation failed to produce valid result.")

        compiled_qasm = compiled_qobj.experiments[0].header.compiled_circuit_qasm
        return IBM(compiled_qasm)

class Quil_Rigetti_Compiler(Compiler):
    """ Compiles Quil to Rigetti """

    def compile(self, source, target_lang):
        qc = get_qc(target_lang)
        return qc.compiler.quil_to_native_quil(source.program)
