#!/usr/bin/env python3
import sys
import argparse

import qcc.config
import qcc.hardware.ibmq
import qcc.hardware.rigetti

from qcc.assembly import *

from qcc import *
from qcc.hardware import *

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('source-lang', choices=config.asm_langs)
    print(config.hw_langs)
    parser.add_argument('target-lang', choices=config.hw_langs)
    parser.add_argument('source', type=argparse.FileType(mode='r', encoding='utf-8'))
    return vars(parser.parse_args())

def create_source_prog(lang, source_file):
    prog_string = source_file.read()
    if lang == config.qasm_lang:
        return QASM(prog_string)
    elif lang == config.quil_lang:
        return Quil(prog_string)

def main():
    ibmq.init()
    config.add_direct_compile(ibmq.backend_names, config.qasm_lang)
    config.add_ibm_langs(ibmq.backend_names)

    rigetti.init()
    config.add_direct_compile(rigetti.backend_names, config.quil_lang)
    # config.add_rigetti_config(rigetti.backend_names) This doesn't exist.

    args = parse()

    print("Request: compile", args['source-lang'], "to", args['target-lang'])
    source_prog = create_source_prog(args['source-lang'], args['source'])

    if config.direct_compile_from[args['target-lang']] == args['source-lang']:
        print("Direct compilation path found: compiling directly")
        direct_compiler = source_prog.get_direct_compiler(args['target-lang'])
        hardware_prog = direct_compiler.compile(source_prog, args['target-lang'])
    else:
        print("No direct compilation path found: compiling through intermediary language")
        intermediary_compiler = source_prog.get_intermediary_compiler()
        intermediary_prog = intermediary_compiler.compile(source_prog, args['target-lang'])
        hardware_compiler = intermediary_prog.get_hardware_compiler(args['target-lang'])
        hardware_prog = hardware_compiler.compile(intermediary_prog, args['target-lang'])

    print("Result below:", hardware_prog, sep='\n')

if __name__ == '__main__':
    main()
