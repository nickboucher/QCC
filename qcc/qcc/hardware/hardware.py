#!/usr/bin/env python3
from pyquil.quilbase import Gate
from qcc.interfaces import HardwareConstrainedProgram
from qcc.hardware.hardware_program_statistics import HardwareConstrainedProgramInfo


class IBM(HardwareConstrainedProgram):
    """ Represents an IBM quantum device """

    def __init__(self, circuit):
        self.program = circuit

    def __str__(self):
        return self.program.qasm()

    def get_statistics(self) -> HardwareConstrainedProgramInfo:
        insts = (data[0] for data in self.program.data)
        two_qubit_gates = len([inst for inst in insts if inst.num_qubits > 1])
        return HardwareConstrainedProgramInfo(num_insts=self.program.size(),
                                              num_2_qubit_gates=two_qubit_gates)


class Rigetti(HardwareConstrainedProgram):
    """ Represents a Rigetti quantum device """

    def __init__(self, quil_program):
        self.program = quil_program

    def __str__(self):
        return self.program.out()

    def get_statistics(self) -> HardwareConstrainedProgramInfo:
        insts = self.program.instructions
        two_qubit_gates = 0
        for inst in insts:
            if isinstance(inst, Gate) and len(inst.qubits) > 1:
                two_qubit_gates += 1
        return HardwareConstrainedProgramInfo(
            num_insts=len(insts),
            num_2_qubit_gates=two_qubit_gates)
