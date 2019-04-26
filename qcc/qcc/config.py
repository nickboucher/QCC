#!/usr/bin/env python3
from configparser import ConfigParser
from os.path import dirname, realpath, exists

config_parser = ConfigParser()
config_file = f"{dirname(realpath(__file__))}/config.ini"
if exists(config_file):
    config_parser.read(config_file)
# Use default section keys
config = config_parser["DEFAULT"]


qasm_lang = "qasm"
quil_lang = "quil"

asm_langs = [qasm_lang, quil_lang]
ibm_langs = []
rigetti_langs = []
hw_langs = []

# load ibm hardware from IBM backends

direct_compile_from = {
}

# add mapping from a list of hardwares to a source language. Currently in
# use for ibmq from main to load hardware using our account, but we can also use it
# for Rigetti.
def add_direct_compile(hws, src_lang):
    direct_compile_from.update([(hw,src_lang) for hw in hws])


# similar use to the above
def add_ibm_langs(hws):
    ibm_langs.extend(hws)
    hw_langs.extend(hws)

# similar use to the above
def add_rigetti_langs(hws):
    rigetti_langs.extend(hws)
    hw_langs.extend(hws)
