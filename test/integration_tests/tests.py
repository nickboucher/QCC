import os
import unittest

from util import Capturing
import qcc.command_line

class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
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

        qcc.init()

    def directory_tester(self, sources, get_args, expected_output_dir_name):
        """
        Check that each expected output in the given directory
            matches the actual output on the corresponding input.
        Assumes directory is flat and contains files of the form
            [target_lang]_[test_num].*
        Uses [target_lang] for target language, and src_[test_num]
            for source file
        sources should be a map like self.src_qasm or self.src_quil
        """
        output_path = os.path.join(self.my_path, expected_output_dir_name)
        for filename in os.listdir(output_path):
            filepath = os.path.join(output_path, filename)
            namesplit = os.path.splitext(filename)[0].split("_")
            trgt = '_'.join(namesplit[:-1])
            src_num = namesplit[-1]
            with Capturing() as actual_output:
                qcc.command_line.main(False, get_args(sources[src_num], trgt))
            actual_output_str = '\n'.join(actual_output)
            with open(filepath, 'r') as f:
                expected_output_str = '\A' + f.read() + '\n\Z'
                self.assertRegex(actual_output_str, expected_output_str)

    def test_qasm_to_ibm(self):
        def get_args(src, trgt):
            return ["qasm", src, "--target-lang", trgt, "-v", "1"]
        self.directory_tester(self.src_qasm, get_args, "qasm_to_ibm")

    def test_quil_to_rigetti(self):
        def get_args(src, trgt):
            return ["quil", src, "--target-lang", trgt, "-v", "1"]
        self.directory_tester(self.src_quil, get_args, "quil_to_rigetti")

    def test_quil_to_ibm(self):
        def get_args(src, trgt):
            return ["quil", src, "--target-lang", trgt, "-v", "1"]
        self.directory_tester(self.src_quil, get_args, "quil_to_ibm")

    def test_qasm_to_rigetti(self):
        def get_args(src, trgt):
            return ["qasm", src, "--target-lang", trgt, "-v", "1"]
        self.directory_tester(self.src_qasm, get_args, "qasm_to_rigetti")

if __name__ == '__main__':
    unittest.main()
