#!/usr/bin/env python3
from typing import List
import subprocess
import atexit
import pyquil

backend_names: List[str] = []


def init():
    global backend_names
    backend_names = pyquil.list_quantum_computers()
    start_quilc()


def start_quilc():
    try:
        subprocess.run(['quilc', '-v'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise EnvironmentError("quilc is not accesible on the system path. "
                               "Have you installed quilc?")
    quilc = subprocess.Popen(
        "quilc -S",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

    def kill_quilc():
        quilc.terminate()
        try:
            quilc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            quilc.kill()

    atexit.register(kill_quilc)
