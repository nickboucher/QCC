#!/usr/bin/env python3
from typing import List

import pyquil

backend_names: List[str] = []


def init():
    global backend_names
    backend_names = pyquil.list_quantum_computers()
