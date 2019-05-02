import os
import unittest

from util import Capturing
import qcc.command_line

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.my_path = os.path.abspath(os.path.dirname(__file__))
        resources_path = os.path.join(self.my_path, "../resources/")
        src_qasm_path = os.path.join(resources_path, "qasm")
        src_quil_path = os.path.join(resources_path, "quil")
        ## maps filename suffix (e.g. "01") to absolute path of src file
        self.src_qasm = {}
        self.src_quil = {}
        ## Extract source qasm and quil from resources directory
        for filename in os.listdir(src_qasm_path):
            src_num = os.path.splitext(filename)[0].split("_")[1]
            filepath = os.path.join(src_qasm_path, filename)
            self.src_qasm[src_num] = filepath
        for filename in os.listdir(src_quil_path):
            src_num = os.path.splitext(filename)[0].split("_")[1]
            filepath = os.path.join(src_quil_path, filename)
            self.src_quil[src_num] = filepath

    def test_quil_to_rigetti(self):
        output_path = os.path.join(self.my_path, "quil_to_rigetti")
        for filename in os.listdir(output_path):
            filepath = os.path.join(output_path, filename)
            trgt, src_num = os.path.splitext(filename)[0].split("_")
            with Capturing() as actual_output:
                qcc.command_line.main(["quil", self.src_quil[src_num], "--target-lang", trgt])
            actual_output_str = '\n'.join(actual_output)
            with open(filepath, 'r') as f:
                expected_output_str = f.read() + '\n'
                self.assertEqual(actual_output_str, expected_output_str)

if __name__ == '__main__':
    unittest.main()
