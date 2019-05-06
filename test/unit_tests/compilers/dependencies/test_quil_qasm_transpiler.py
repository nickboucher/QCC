import os
import unittest

from pyquil import Program
from qcc.compilers import Quil_QASM_Transpiler
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


class QuilQASMTranspilerTests(unittest.TestCase):
    def _get_transpilation_output(self, name):
        my_path = os.path.abspath(os.path.dirname(__file__))
        quil_file_path = os.path.join(
            my_path, "../../../resources/quil/%s" % name
        )
        with open(quil_file_path, 'r') as quil_file:
            quil_program = Program(quil_file.read())
            transpiler = Quil_QASM_Transpiler()
            return transpiler.transpile(quil_program)

    def test_quil_qasm_transpiler_init(self):
        """ Test that transpiler creation doesn't raise any exceptions. """
        Quil_QASM_Transpiler()

    def test_quil_qasm_transpiler_transpile(self):
        """ Test that transpilation doesn't raise exceptions. """
        self._get_transpilation_output("src_01.quil")

    def testquil_qasm_transpiler_transpile_01(self):
        """ Test for the correct transpilation of src_01.quil. """
        qasm_circuit = self._get_transpilation_output("src_01.quil")
        qr_name = qasm_circuit.qregs[0].name
        qrs = QuantumRegister(1, name=qr_name)
        cr_name = qasm_circuit.cregs[0].name
        crs = ClassicalRegister(1, name=cr_name)
        expected = QuantumCircuit(qrs, crs)
        expected.iden(qrs[0])
        expected.measure(qrs[0], crs[0])
        assert(qasm_circuit == expected)

    def testquil_qasm_transpiler_transpile_02(self):
        """ Test for the correct transpilation of src_02.quil. """
        qasm_circuit = self._get_transpilation_output("src_02.quil")
        qr_name = qasm_circuit.qregs[0].name
        qrs = QuantumRegister(1, name=qr_name)
        cr_name = qasm_circuit.cregs[0].name
        crs = ClassicalRegister(1, name=cr_name)
        expected = QuantumCircuit(qrs, crs)
        expected.x(qrs[0])
        expected.measure(qrs[0], crs[0])
        assert(qasm_circuit == expected)

    def testquil_qasm_transpiler_transpile_03(self):
        """ Test for the correct transpilation of src_03.quil. """
        qasm_circuit = self._get_transpilation_output("src_03.quil")
        qr_name = qasm_circuit.qregs[0].name
        qrs = QuantumRegister(1, name=qr_name)
        cr_name = qasm_circuit.cregs[0].name
        crs = ClassicalRegister(1, name=cr_name)
        expected = QuantumCircuit(qrs, crs)
        expected.y(qrs[0])
        expected.measure(qrs[0], crs[0])
        assert(qasm_circuit == expected)

    def testquil_qasm_transpiler_transpile_04(self):
        """ Test for the correct transpilation of src_04.quil. """
        qasm_circuit = self._get_transpilation_output("src_04.quil")
        qr_name = qasm_circuit.qregs[0].name
        qrs = QuantumRegister(1, name=qr_name)
        cr_name = qasm_circuit.cregs[0].name
        crs = ClassicalRegister(1, name=cr_name)
        expected = QuantumCircuit(qrs, crs)
        expected.z(qrs[0])
        expected.measure(qrs[0], crs[0])
        assert(qasm_circuit == expected)

    def testquil_qasm_transpiler_transpile_05(self):
        """ Test for the correct transpilation of src_05.quil. """
        qasm_circuit = self._get_transpilation_output("src_05.quil")
        qr_name = qasm_circuit.qregs[0].name
        qrs = QuantumRegister(1, name=qr_name)
        cr_name = qasm_circuit.cregs[0].name
        crs = ClassicalRegister(1, name=cr_name)
        expected = QuantumCircuit(qrs, crs)
        expected.h(qrs[0])
        expected.measure(qrs[0], crs[0])
        assert(qasm_circuit == expected)

    def testquil_qasm_transpiler_transpile_06(self):
        """ Test for the correct transpilation of src_06.quil. """
        qasm_circuit = self._get_transpilation_output("src_06.quil")
        qr_name = qasm_circuit.qregs[0].name
        qrs = QuantumRegister(1, name=qr_name)
        cr_name = qasm_circuit.cregs[0].name
        crs = ClassicalRegister(1, name=cr_name)
        expected = QuantumCircuit(qrs, crs)
        expected.rx(0, qrs[0])
        expected.measure(qrs[0], crs[0])
        assert(qasm_circuit == expected)
