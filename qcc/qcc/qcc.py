#!/usr/bin/env python3
from qcc import config
import qcc.hardware.ibmq
import qcc.hardware.rigetti
from qcc.assembly import QASM, Quil
from qcc.hardware import ibmq, rigetti


def create_source_prog(lang, source_file):
    prog_string = source_file.read()
    if lang == qcc.config.qasm_lang:
        return QASM(prog_string)
    elif lang == qcc.config.quil_lang:
        return Quil(prog_string)


def init():
    ibmq.init()
    config.add_direct_compile(ibmq.backend_names, qcc.config.qasm_lang)
    config.add_ibm_langs(ibmq.backend_names)

    rigetti.init()
    config.add_direct_compile(rigetti.backend_names, config.quil_lang)
    config.add_rigetti_langs(rigetti.backend_names)


def compile(source_lang, target_lang, source_file):

    print("Request: compile", source_lang, "to", target_lang)
    source_prog = create_source_prog(source_lang, source_file)

    if qcc.config.direct_compile_from[target_lang] == source_lang:
        print("Direct compilation path found: compiling directly")
        direct_compiler = source_prog.get_direct_compiler(target_lang)
        hardware_prog = direct_compiler.compile(source_prog, target_lang)
    else:
        print("No direct compilation path found: compiling through",
              "intermediary language")
        intermediary_compiler = source_prog.get_intermediary_compiler()
        intermediary_prog = intermediary_compiler.compile(
            source_prog)
        hardware_compiler = intermediary_prog.get_hardware_compiler(
            target_lang)
        hardware_prog = hardware_compiler.compile(
            intermediary_prog,
            target_lang)

    return hardware_prog
