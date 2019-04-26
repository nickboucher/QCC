#!/usr/bin/env python3
from __future__ import annotations
import pyduktape
import qcc.assembly
from os.path import dirname, realpath, exists
from qcc.interfaces import Compiler
from qcc.intermediary_lang import IntermediaryProgram


class QASM_Intermediary_Compiler(Compiler):
    """ Compiles QASM to Intermediary Language """

    def __init__(self):
        # Create JS interpreter
        self.js_ctx = pyduktape.DuktapeContext()
        # Load quantum-circuit JS package into JS context
        qc_js = f"{dirname(realpath(__file__))}/dependencies/qc.js"
        if exists(qc_js):
            self.js_ctx.eval_js_file(qc_js)
        else:
            raise FileNotFoundError("Missing qc.js dependency.")

    def compile(self, source: qcc.assembly.QASM) -> IntermediaryProgram:
        # Implement this
        return IntermediaryProgram("TODO")


class Quil_Intermediary_Compiler(Compiler):
    """ Compiles Quil to Intermediary Language """

    def compile(self, source: qcc.assembly.Quil) -> IntermediaryProgram:
        # Implement this
        return IntermediaryProgram("TODO")
