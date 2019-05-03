from typing import List
from pyquil.quilbase import AbstractInstruction, DefGate


class Program:
    defined_gates: List[DefGate]
    instructions: List[AbstractInstruction]

    def is_protoquil(self) -> bool: ...


class QuantumComputer:
    pass


def get_qc(name: str) -> QuantumComputer: ...
