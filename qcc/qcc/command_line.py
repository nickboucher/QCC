#!/usr/bin/env python3
import sys

import argparse
import qcc.config as config
import qcc

def exactly_one_true(*bools : bool) -> bool:
    """ Return True iff exactly one of the arguments is True """
    return sum(bools) == 1

def parse_cli_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('source-lang', choices=config.asm_langs)
    parser.add_argument(
        'source-file',
        type=argparse.FileType(mode='r', encoding='utf-8'))
    parser.add_argument('--target-lang', dest='target-lang', choices=config.hw_langs)
    parser.add_argument('--auto-target', dest='auto-target', action='store_true')
    parser.add_argument('--profiles', action='store_true')
    parser.add_argument(
        '--stats',
        dest='print_stats',
        action='store_true',
        help='Print statistics about program rather than source')
    parser.add_argument('-v', '--verbose', dest='verbosity', type=int, choices=[1,2], default=2)
    parser.add_argument('-o', dest='output_file', type=str)
    args = vars(parser.parse_args(args))
    if not exactly_one_true(args['target-lang'] is not None, args['profiles'], args['auto-target']):
        parser.error("Must choose exactly one of {--target-lang, --auto-target, --profiles}")
    if args['profiles'] and args['print_stats']:
        parser.error("Cannot use --stats flag with --profiles.")

    return args


def main(should_init=True, input_args=None):
    # load languages
    if should_init:
        qcc.init()
    args = parse_cli_args(input_args)
    config.verbosity = args["verbosity"]
    if args["output_file"]:
        output_file = open(args["output_file"], 'w')
    else:
        output_file = sys.stdout
    if args['target-lang'] is not None:
        prog = qcc.compile(
            args['source-lang'],
            args['target-lang'],
            args['source-file'])

        print("*" * 50)
        if args['print_stats']:
            print(prog.get_statistics(), file=output_file)
        else:
            print(prog, file=output_file)
    elif args['profiles']:
        print("*" * 50)
        profiles = qcc.get_profiles(args['source-lang'], args['source-file'])
        for target, stats in profiles:
            print("*" * 10, target, "*" * 10, file=output_file)
            print(stats, file=output_file)
    elif args['auto-target']:
        target, prog = qcc.compile_to_auto_target(args['source-lang'], args['source-file'])
        print("Chosen target:", target)
        print("*" * 50)
        if args['print_stats']:
            print(prog.get_statistics(), file=output_file)
        else:
            print(prog, file=output_file)

    if args['source-file']:
        args['source-file'].close()
