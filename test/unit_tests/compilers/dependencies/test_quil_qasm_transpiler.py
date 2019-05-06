import os
import unittest

from pyquil import Program
from qcc.compilers import Quil_QASM_Transpiler
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


class QuilQASMTranspilerTests(unittest.TestCase):
    def _get_quil_file_path(self, name):
        my_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(
            my_path, "../../../resources/quil/%s" % name
        )

    def test_quil_qasm_transpiler_init(self):
        """ Test that transpiler creation doesn't raise any exceptions. """
        Quil_QASM_Transpiler()

    def test_quil_qasm_transpiler_transpile(self):
        """ Test that transpilation doesn't raise exceptions. """
        quil_file_path = self._get_quil_file_path("src_01.quil")
        with open(quil_file_path, 'r') as quil_file:
            quil_program = Program(quil_file.read())
            transpiler = Quil_QASM_Transpiler()
            transpiler.transpile(quil_program)

    def testquil_qasm_transpiler_transpile_01(self):
        """ Test for the correct transpilation of src_01.quil. """
        quil_file_path = self._get_quil_file_path("src_01.quil")
        with open(quil_file_path, 'r') as quil_file:
            quil_program = Program(quil_file.read())
            transpiler = Quil_QASM_Transpiler()
            qasm_circuit = transpiler.transpile(quil_program)

            qr_name = qasm_circuit.qregs[0].name
            qrs = QuantumRegister(1, name=qr_name)
            cr_name = qasm_circuit.cregs[0].name
            crs = ClassicalRegister(1, name=cr_name)
            expected = QuantumCircuit(qrs, crs)
            expected.x(qrs[0])
            expected.measure(qrs[0], crs[0])
            assert(qasm_circuit == expected)
