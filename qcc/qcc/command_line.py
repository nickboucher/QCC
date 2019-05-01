#!/usr/bin/env python3
import argparse
import qcc.config as config
import qcc

def exactly_one_true(*bools : bool) -> bool:
    """ Return True iff exactly one of the arguments is True """
    return sum(bools) == 1

def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source-lang', choices=config.asm_langs)
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
    parser.add_argument('--target-lang', dest='target-lang', choices=config.hw_langs)
    parser.add_argument('--profiles', action='store_true')
    args = vars(parser.parse_args())
    if not exactly_one_true(args['target-lang'] is not None, args['profiles']):
        parser.error("Must choose exactly one of {--target-lang, --profiles}")
    if args['profiles'] and args['print_stats']:
        parser.error("Cannot use --stats flag with --profiles")

    return args


def main():
    # load languages
    qcc.init()
    args = parse_cli_args()
    if args['target-lang'] is not None:
        prog = qcc.compile(
            args['source-lang'],
            args['target-lang'],
            args['source-file'])

        if args['print_stats']:
            print("Result below:", prog.get_statistics(), sep='\n')
        else:
            print("Result below:", prog, sep='\n')
    elif args['profiles']:
        print("Profiles below:")
        profiles = qcc.get_profiles(args['source-lang'], args['source-file'])
        for target, stats in profiles:
            print("*" * 10, target, "*" * 10)
            print(stats)
