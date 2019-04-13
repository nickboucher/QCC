#!/usr/bin/env python3
import sys
import argparse
from assembly import *

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('source-lang', choices=['qasm', 'quil'])
    parser.add_argument('target-lang', choices=['ibm01'])
    parser.add_argument('source', type=argparse.FileType('r'))
    return vars(parser.parse_args())

def createSourceProg(lang, sourceFile):
    progString = sourceFile.read()
    if lang == 'qasm':
        return QASM(progString)
    elif lang == 'quil':
        return Quil(progString)

def main():
    args = parseArgs()
    sourceProg = createSourceProg(args['source-lang'], args['source'])

if __name__ == '__main__':
    main()
