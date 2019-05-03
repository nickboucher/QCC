#!/usr/bin/env python3
from typing import IO, List, Tuple

import qcc.config
from qcc.assembly import QASM, Quil
from qcc.hardware import ibmq, rigetti
from qcc.hardware.hardware_program_statistics import HardwareConstrainedProgramInfo
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


def compile_from_program(source_lang: str, target_lang: str, source_prog: AsmProgram) -> HardwareConstrainedProgram:
    if qcc.config.direct_compile_from[target_lang] == source_lang:
        print("Direct compilation path found to {}".format(target_lang))
        direct_compiler: Compiler = source_prog.get_direct_compiler(target_lang)
        hardware_prog: HardwareConstrainedProgram = direct_compiler.compile(source_prog, target_lang)
    else:
        print("No direct compilation path found to {}: compiling through".format(target_lang),
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

def compile(source_lang: str, target_lang: str, source_file: IO[str]) -> HardwareConstrainedProgram:
    print("Request: compile", source_lang, "to", target_lang)
    source_prog: AsmProgram = create_source_prog(source_lang, source_file)
    return compile_from_program(source_lang, target_lang, source_prog)

def compile_all(source_lang: str, source_file: IO[str]) -> List[Tuple[str, HardwareConstrainedProgram]]:
    source_prog : AsmProgram = create_source_prog(source_lang, source_file)
    results: List[Tuple[str, HardwareConstrainedProgram]] = []
    for target_lang in qcc.config.hw_langs:
        try:
            prog = compile_from_program(source_lang, target_lang, source_prog)
            results.append((target_lang, prog))
        except:
            pass
    return results

def get_profiles(source_lang: str, source_file: IO[str]) -> List[Tuple[str, HardwareConstrainedProgramInfo]]:
    compilations = compile_all(source_lang, source_file)
    return [(target, prog.get_statistics()) for (target, prog) in compilations]

def compile_to_auto_target(source_lang : str, source_file: IO[str]) -> Tuple[str, HardwareConstrainedProgram]:
    """
    Returns compilation to target language that produces the best result,
    along with the target language used for this compilation
    """
    compilations = compile_all(source_lang, source_file)
    def score(target_prog_pair):
        target, prog = target_prog_pair
        return (target, prog.get_statistics().score())
    return min(compilations, key=score)
