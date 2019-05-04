#!/usr/bin/env python3
import sys

import argparse
import qcc.config as config
import qcc
from  qcc.util import qprint

def exactly_one_true(*bools : bool) -> bool:
    """ Return True iff exactly one of the arguments is True """
    return sum(bools) == 1

def parse_cli_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source-file',
        type=argparse.FileType(mode='r', encoding='utf-8'))
    parser.add_argument('--target-lang', dest='target-lang', type=str)
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

    hw_target = args['target-lang']

    if hw_target.startswith("ibmq"):
        print("Asssuming platform is IBM, loading HW description")
        qcc.qcc.init_ibmq()

    if hw_target not in config.hw_langs:
        # if targets starts with ibmq, assume it's an ibm platform and actually
        # make a call to their API (doing this to minimize network footprint)
        parser.error("Target {} not supported  (must be one of {}) or an IBM platform"\
                .format(hw_target, config.hw_langs))

    return args


def main(should_init=True, input_args=None):
    # load languages
    if should_init:
        qcc.init()
    args = parse_cli_args(input_args)
    source_lang = qcc.get_source_lang(args['source-file'])
    if "verbosity" not in args:
        config.current_verbosity = 2
    else:
        config.current_verbosity = args["verbosity"]

    if args["output_file"]:
        output_file = open(args["output_file"], 'w')
    else:
        output_file = sys.stdout
    if args['target-lang'] is not None:
        prog = qcc.compile(
            source_lang,
            args['target-lang'],
            args['source-file'])

        qprint("*" * 50)
        if args['print_stats']:
            qprint(prog.get_statistics(), file=output_file, priority=1)
        else:
            qprint(prog, file=output_file, priority=1)
    elif args['profiles']:
        qprint("*" * 50)
        profiles = qcc.get_profiles(source_lang, args['source-file'])
        for target, stats in profiles:
            qprint("*" * 10, target, "*" * 10, file=output_file, priority=1)
            qprint(stats, file=output_file, priority=1)
    elif args['auto-target']:
        target, prog = qcc.compile_to_auto_target(source_lang, args['source-file'])
        # TODO: turn this into a commment depending on the hardware?
        qprint("Chosen target:", target, priority=1)
        qprint("*" * 50)
        if args['print_stats']:
            qprint(prog.get_statistics(), file=output_file, priority=1)
        else:
            qprint(prog, file=output_file, priority=1)

    if args['source-file']:
        args['source-file'].close()
