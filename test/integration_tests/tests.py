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

    def directory_tester(self, source_lang, expected_output_dir_name, sources):
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
                qcc.command_line.main(False, [source_lang, sources[src_num], "--target-lang", trgt])
            actual_output_str = '\n'.join(actual_output)
            with open(filepath, 'r') as f:
                expected_output_str = f.read() + '\n'
                self.assertEqual(actual_output_str, expected_output_str)

    def test_quil_to_rigetti(self):
        self.directory_tester("quil", "quil_to_rigetti", self.src_quil)

    def test_qasm_to_ibm(self):
        self.directory_tester("qasm", "qasm_to_ibm", self.src_qasm)

if __name__ == '__main__':
    unittest.main()
