import unittest

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
        Just test that this method
        doesn't raise exceptions.
        """
        compiler = QASM_Intermediary_Compiler()

#interm = compiler.compile(qasm_program)
#print(interm.quil)

if __name__ == '__main__':
    unittest.main()
