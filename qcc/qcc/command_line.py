#!/usr/bin/env python3
import argparse
import qcc.config as config
import qcc


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source-lang', choices=config.asm_langs)
    parser.add_argument('target-lang', choices=config.hw_langs)
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
    return vars(parser.parse_args())


def main():
    # load languages
    qcc.init()
    args = parse_cli_args()
    prog = qcc.compile(
        args['source-lang'],
        args['target-lang'],
        args['source-file'])

    print("Result below:", prog, sep='\n')
