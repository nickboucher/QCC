#!/usr/bin/env python3
import pyquil
from typing import List

backend_names : List[str] = []


def init():
    global backend_names
    backend_names = pyquil.list_quantum_computers()
