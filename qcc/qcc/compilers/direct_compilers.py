#!/usr/bin/env python3
import sys
import qiskit
from pyquil import get_qc
from qcc.interfaces import Compiler
from qcc.hardware import IBM, Rigetti, ibmq


# TODO: complete and implement this set of compilers
class QASM_IBM_Compiler(Compiler):
    """ Compiles QASM to IBM """

    def compile(self, source, target_lang):
        try:
            compiled_qobj = qiskit.compile(
                source.circuit,
                ibmq.backends[target_lang])
        except:
            raise ValueError("Failed to compile circuit to specified hardware")
        # TODO: It would be nice to use qiskit.converters.qobj_to_circuits
        #       for this. Unfortunately their code throws an error when
        #       I try to use it.
        if (
            len(compiled_qobj.experiments) != 1
            or not compiled_qobj.experiments[0].header
            or not compiled_qobj.experiments[0].header.compiled_circuit_qasm
        ):
            raise ValueError("Compilation failed to produce valid result.")

        compiled_qasm_str = \
            compiled_qobj.experiments[0].header.compiled_circuit_qasm
        compiled_qasm_circuit = \
            qiskit.QuantumCircuit.from_qasm_str(compiled_qasm_str)
        return IBM(compiled_qasm_circuit)


class Quil_Rigetti_Compiler(Compiler):
    """ Compiles Quil to Rigetti """

    def compile(self, source, target_lang):
        qc = get_qc(target_lang, as_qvm=True)
        compiled_quil = qc.compiler.quil_to_native_quil(source.program)
        return Rigetti(compiled_quil)
