#!/usr/bin/env python3
import qcc.config
import qcc.hardware.ibmq
import qcc.hardware.rigetti
from typing import IO
from qcc.assembly import QASM, Quil
from qcc.hardware import ibmq, rigetti
from qcc.interfaces import AsmProgram, Compiler, HardwareConstrainedProgram
from qcc.intermediary_lang import IntermediaryProgram

def create_source_prog(lang: str, source_file: IO[str]) -> AsmProgram:
    prog_string: str = source_file.read()
    if lang == qcc.config.qasm_lang:
        return QASM(prog_string)
    elif lang == qcc.config.quil_lang:
        return Quil(prog_string)
    else:
        raise ValueError("lang is not a valid language.")

def init() -> None:
    ibmq.init()
    qcc.config.add_direct_compile(ibmq.backend_names, qcc.config.qasm_lang)
    qcc.config.add_ibm_langs(ibmq.backend_names)

    rigetti.init()
    qcc.config.add_direct_compile(rigetti.backend_names, qcc.config.quil_lang)
    qcc.config.add_rigetti_langs(rigetti.backend_names)


def compile(source_lang: str, target_lang: str, source_file: IO[str]) -> HardwareConstrainedProgram:
    print("Request: compile", source_lang, "to", target_lang)
    source_prog: AsmProgram = create_source_prog(source_lang, source_file)

    if qcc.config.direct_compile_from[target_lang] == source_lang:
        print("Direct compilation path found: compiling directly")
        direct_compiler: Compiler = source_prog.get_direct_compiler(target_lang)
        hardware_prog: HardwareConstrainedProgram = direct_compiler.compile(source_prog, target_lang)
    else:
        print("No direct compilation path found: compiling through",
              "intermediary language")
        intermediary_compiler: Compiler = source_prog.get_intermediary_compiler()
        intermediary_prog: IntermediaryProgram = intermediary_compiler.compile(
            source_prog)
        hardware_compiler: Compiler = intermediary_prog.get_hardware_compiler(
            target_lang)
        hardware_prog = hardware_compiler.compile(
            intermediary_prog,
            target_lang)

    return hardware_prog
