#!/usr/bin/env python3
import qcc.util
from qiskit.compiler import transpile, assemble
from qiskit.converters import qobj_to_circuits
from pyquil import get_qc
from qcc.interfaces import Compiler
from qcc.hardware import IBM, Rigetti, ibmq


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
                optimization_level=0
            )
            compiled_qobj = assemble(
                new_circuit,
                backend=backend
            )
        except:
            raise ValueError("Failed to compile to the specified hardware.")

        qcc.util.qprint("Finished QASM compilation!", priority=2)

        compiled_circuit = qobj_to_circuits(compiled_qobj)[0]
        return IBM(compiled_circuit)


class Quil_Rigetti_Compiler(Compiler):
    """ Compiles Quil to Rigetti """

    def compile(self, source, target_lang):
        qc = get_qc(target_lang, as_qvm=True)
        compiled_quil = qc.compiler.quil_to_native_quil(source.program)
        return Rigetti(compiled_quil)
