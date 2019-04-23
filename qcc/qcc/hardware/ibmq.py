#!/usr/bin/env python3
import qiskit
from qcc.config import config

backends = {}
backend_names = []

def init():
    global backends, backend_names
    print("Loading ibmqx account and information...")
    qiskit.IBMQ.enable_account(config["IBMQ_API_TOKEN"])

    backend_objs = list(filter(filter_backend, load_backends()))
    backend_names = [b.name() for b in backend_objs]

    for b in backend_objs:
        backends[b.name()] = b

def filter_backend(backends):
    return True
    ## filter out local qasm simulator
    ## compiling to this local simulator may be useful for testing
    # return 'qasm' not in backends.name()

def init_ibmq_accounts():
    qiskit.IBMQ.load_accounts()

def load_backends():
    return qiskit.IBMQ.backends()
