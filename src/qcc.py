#!/usr/bin/env python3
import sys
import argparse
import langs
from assembly import *

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('source-lang', choices=langs.asm_langs)
    parser.add_argument('target-lang', choices=langs.hw_langs)
    parser.add_argument('source', type=argparse.FileType('r'))
    return vars(parser.parse_args())

def create_source_prog(lang, source_file):
    prog_string = source_file.read()
    if lang == langs.qasm_lang:
        return QASM(prog_string)
    elif lang == langs.quil_lang:
        return Quil(prog_string)

def main():
    args = parse()
    print("Request: compile", args['source-lang'], "to", args['target-lang'])

    source_prog = create_source_prog(args['source-lang'], args['source'])

    if langs.direct_compile_from[args['target-lang']] == args['source-lang']:
        print("Direct compilation path found")
        ## TODO: run direct compilation
        return

    print("No direct compilation path found: compiling through intermediary language")
    intermediary_compiler = source_prog.get_intermediary_compiler()
    intermediary_prog = intermediary_compiler.compile(source_prog)
    hardware_compiler = intermediary_prog.get_hardware_compiler(args['target-lang'])
    hardware_prog = hardware_compiler.compile(intermediary_prog)
    print("Result below:", hardware_prog, sep='\n')

if __name__ == '__main__':
    main()
