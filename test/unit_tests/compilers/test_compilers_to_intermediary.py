import os
import unittest

from qcc.assembly.qasm import QASM
from qcc.compilers import QASM_Intermediary_Compiler

class CompilersToIntermediaryTests(unittest.TestCase):

    def test_qasm_intermediary_compiler_init(self):
        """
        Just test that compiler creation
        doesn't raise any exceptions.
        """
        QASM_Intermediary_Compiler()

    def test_qasm_intermediary_compiler_compile(self):
        """
        Just test that compilation
        doesn't raise exceptions.
        """
        my_path = os.path.abspath(os.path.dirname(__file__))
        qasm_file_path = os.path.join(my_path, "../../resources/qasm/src_01.qasm")
        with open(qasm_file_path, 'r') as qasm_file:
            qasm_str = qasm_file.read()
            qasm_prog = QASM(qasm_str)
            compiler = QASM_Intermediary_Compiler()
            compiler.compile(qasm_prog)
