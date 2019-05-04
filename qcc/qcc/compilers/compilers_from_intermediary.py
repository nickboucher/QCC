#!/usr/bin/env python3
from pyquil import get_qc

import qcc.assembly
from qcc.compilers.direct_compilers import QASM_IBM_Compiler
from qcc.compilers.dependencies.quil_qasm_transpiler import \
    Quil_QASM_Transpiler
from qcc.hardware import Rigetti
from qcc.interfaces import Compiler

# TODO: Move any functionality out that depends on the specific
#   implementation of the intermediary language.


class Intermediary_IBM_Compiler(Compiler):
    """ Compiles Intermediary Language to IBM """

    def compile(self, source, target_lang):
        """ Compile from the intermediary language to QASM. """

        program = source.quil.program
        transpiler = Quil_QASM_Transpiler()
        circuit = transpiler.transpile(program)
        compiled_circuit = self._compile_circuit(circuit, target_lang)
        return compiled_circuit

    @staticmethod
    def _compile_circuit(circuit, target_lang):
        """ Compile the Qiskit circuit for the specific target hardware. """

        # Not ideal, since we go to QASM then back to the circuit
        qasm = qcc.assembly.QASM(circuit.qasm())
        compiler = QASM_IBM_Compiler()
        return compiler.compile(qasm, target_lang)


class Intermediary_Rigetti_Compiler(Compiler):
    """ Compiles Intermediary Language to Rigetti """

    @staticmethod
    def compile(source, target_lang):
        """ Compile from the intermediary language to a Quil program. """

        program = source.quil.program
        compiler = get_qc(target_lang, as_qvm=True).compiler
        compiled_program = compiler.quil_to_native_quil(program)
        return Rigetti(compiled_program)
