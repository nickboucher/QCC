#!/usr/bin/env python3
import argparse
import qcc.config as config
import qcc


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source-lang', choices=config.asm_langs)
    parser.add_argument('--target-lang', dest='target-lang', choices=config.hw_langs)
    parser.add_argument(
        'source-file',
        type=argparse.FileType(mode='r', encoding='utf-8'))
    parser.add_argument(
        '--stats',
        dest='print_stats',
        action='store_const',
        const=True,
        default=False,
        help='Print statistics about program rather than source')
    args = vars(parser.parse_args())
    if 'target-lang' not in args:
        parser.error("--target-lang required")

    return args


def main():
    # load languages
    qcc.init()
    args = parse_cli_args()
    prog = qcc.compile(
        args['source-lang'],
        args['target-lang'],
        args['source-file'])

    if args['print_stats']:
        print("Result below:", prog.get_statistics(), sep='\n')
    else:
        print("Result below:", prog, sep='\n')
