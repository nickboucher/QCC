#!/usr/bin/env python3
import sys
import argparse
import langs

import ibmq

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
    print("Loading ibmqx account and information...")
    ibmq_session = ibmq.IBMQ()
    langs.add_direct_compile(ibmq_session.backend_names, langs.qasm_lang)
    langs.add_hw_lang(ibmq_session.backend_names)

    args = parse()

    print("Request: compile", args['source-lang'], "to", args['target-lang'])

    if langs.direct_compile_from[args['target-lang']] == args['source-lang']:
        if args['source-lang'] == langs.qasm_lang:
            hardware_prog = \
                QASM.direct_compile(args['source'].read(), args['target-lang'], ibmq_session)
        elif args['source-lang'] == langs.quil_lang:
            # TODO: figure out how to compile quil
            hardware_prog = "TODO"
            pass
    else:
        print("No direct compilation path found: compiling through intermediary language")
        source_prog = create_source_prog(args['source-lang'], args['source'])

        intermediary_compiler = source_prog.get_intermediary_compiler()
        intermediary_prog = intermediary_compiler.compile(source_prog)
        hardware_compiler = intermediary_prog.get_hardware_compiler(args['target-lang'])
        hardware_prog = hardware_compiler.compile(intermediary_prog)

    print("Result below:", hardware_prog, sep='\n')

if __name__ == '__main__':
    main()
