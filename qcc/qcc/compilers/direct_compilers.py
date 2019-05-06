#!/usr/bin/env python3
import qcc.util
from qiskit.compiler import transpile, assemble
from qiskit.converters import qobj_to_circuits
from pyquil import get_qc
from qcc.interfaces import Compiler
from qcc.hardware import IBM, Rigetti, ibmq
import warnings


class QASM_IBM_Compiler(Compiler):
    """ Compiles QASM to IBM """

    def compile(self, source, target_lang):
        qcc.util.qprint("Beginning QASM compilation...", priority=2)

        try:
            backend = ibmq.backends[target_lang]
            # Requires Qiskit >= 0.9.0
            new_circuit = transpile(
                source.circuit,
                backend=backend,
                optimization_level=2
            )
            compiled_qobj = assemble(
                new_circuit,
                backend=backend
            )
        except:
            raise ValueError("Failed to compile to the specified hardware.")

        qcc.util.qprint("Finished QASM compilation!", priority=2)

        # reader who lives in a qiskit Terra >= 0.9 future: This code filters a
        # deprecation warning for `qiskit.converter.qobj_to_circuit` which has
        # been replaced with `qiskit.compiler.disassemble_circuits`. The new
        # function is not available at the time of the writing of this comment,
        # but if it is available to you, please kindly remove the supressal
        # of the warning and replace the call with the non-deprecated function.
        warnings.filterwarnings('ignore')
        compiled_circuit = qobj_to_circuits(compiled_qobj)[0]
        warnings.filters.pop(0)
        return IBM(compiled_circuit)


class Quil_Rigetti_Compiler(Compiler):
    """ Compiles Quil to Rigetti """

    def compile(self, source, target_lang):
        qc = get_qc(target_lang, as_qvm=True)
        compiled_quil = qc.compiler.quil_to_native_quil(source.program)
        return Rigetti(compiled_quil)
