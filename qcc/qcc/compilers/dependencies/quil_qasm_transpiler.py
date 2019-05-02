#!/usr/bin/env python3
import numpy
from pyquil import Program, get_qc
from pyquil.quilbase import Declare, Gate, Halt, Measurement, Pragma, \
    Reset, ResetQubit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit

# TODO: A lot of testing.


class Quil_QASM_Transpiler:
    """ Transpiler from Quil to QASM. """

    def transpile(self, program):
        """ Transpile Quil to QASM, taking a Quil program as input. """

        instructions = program.instructions

        # TODO: Expand from ProtoQuil programs to anything IBM can handle.
        if not program.is_protoquil():
            raise ValueError("The Quil program is not a ProtoQuil program.")

        defined_gate_map = self._construct_defined_gate_map(
            program.defined_gates
        )

        instructions = self._remove_pragmas(instructions)

        classical_register_map = self._construct_classical_register_map(
            instructions
        )
        quantum_register_map = self._construct_quantum_register_map(
            instructions
        )

        crs, qrs, circuit = self._instantiate_qiskit(
            len(classical_register_map),
            len(quantum_register_map)
        )

        self._transpile_instructions(
            crs,
            qrs,
            circuit,
            instructions,
            classical_register_map,
            quantum_register_map,
            defined_gate_map
        )

        return circuit

    @staticmethod
    def _construct_defined_gate_map(defined_gates):
        """ Construct a map from names to defined gate objects. """

        defined_gate_map = {}
        for gate in defined_gates:
            defined_gate_map[gate.name] = gate
        return defined_gate_map

    @staticmethod
    # TODO: Determine whether there is a corresponding PRAGMA for BARRIER.
    def _remove_pragmas(instructions):
        """ Remove PRAGMAs from the instructions. """

        return [
            instr for instr in instructions if not isinstance(instr, Pragma)
        ]

    @staticmethod
    def _construct_classical_register_map(instructions):
        """
        Create a map from classical register instances in the Quil code
        to indices in the classical register object that we create for
        the Qiskit circuit.
        """

        classical_register_map = {}

        # The next classical register to assign
        qiskit_index = 0

        declarations = [
            instr for instr in instructions
            if isinstance(instr, Declare) and instr.memory_type == "BIT"
        ]

        declaration_map = {}
        for instr in declarations:
            if instr.name in declaration_map.keys():
                raise ValueError(
                    "There is a duplicate declaration of %s." % instr.name
                )
            declaration_map[instr.name] = instr

        # Classical registers are MemoryReference objects.
        def parse_classical(register):
            return register.name, int(register.offset)

        def classical_key(name, offset):
            return "%s[%s]" % (name, offset)

        for instr in instructions:
            if isinstance(instr, Measurement):
                if instr.classical_reg:
                    name, off = parse_classical(instr.classical_reg)
                    if (name not in declaration_map.keys()) or \
                       off >= declaration_map[name].memory_size:
                        raise ValueError(
                            "%s[%s] is an invalid memory address" % (name, off)
                        )
                    key = classical_key(name, off)
                    if key not in classical_register_map.keys():
                        classical_register_map[key] = qiskit_index
                        qiskit_index += 1
                else:
                    classical_register_map[str(instr.qubit)] = qiskit_index
                    qiskit_index += 1

        return classical_register_map

    @staticmethod
    def _construct_quantum_register_map(instructions):
        """
        Create a map from quantum register instances in the Quil code to
        indices in the quantum register object that we create for the
        Qiskit circuit.
        """

        quantum_register_map = {}

        # The next quantum register to assign
        qiskit_index = 0

        for instr in instructions:
            if isinstance(instr, Measurement):
                if str(instr.qubit) not in quantum_register_map.keys():
                    quantum_register_map[str(instr.qubit)] = qiskit_index
                    qiskit_index += 1
            elif isinstance(instr, ResetQubit):
                if str(instr.qubit) not in quantum_register_map.keys():
                    quantum_register_map[str(instr.qubit)] = qiskit_index
                    qiskit_index += 1
            elif isinstance(instr, Gate):
                for qubit in instr.qubits:
                    if str(qubit) not in quantum_register_map.keys():
                        quantum_register_map[str(qubit)] = qiskit_index
                        qiskit_index += 1

        return quantum_register_map

    @staticmethod
    def _instantiate_qiskit(cr_count, qr_count):
        """
        Instantiate the appropriate Qiskit objects for the creation of
        a Qiskit circuit.
        """

        crs = ClassicalRegister(cr_count)
        qrs = QuantumRegister(qr_count)
        circuit = QuantumCircuit(qrs, crs)
        return (crs, qrs, circuit)

    def _transpile_instructions(self, crs, qrs, circ, insts,
                                cr_map, qr_map, dg_map):
        """
        Transpile instructions from Quil to QASM using the classical register
        map, quantum register map, and defined gate map.
        """

        for instr in insts:
            if isinstance(instr, Reset):
                circ.reset(qrs)
            elif isinstance(instr, ResetQubit):
                q_key = str(instr.qubit)
                circ.reset(qrs[qr_map[q_key]])
            elif isinstance(instr, Halt):
                break
            elif isinstance(instr, Measurement):
                q_key = str(instr.qubit)

                cr = instr.classical_reg
                if cr:
                    c_key = "%s[%s]" % (cr.name, cr.offset)
                else:
                    c_key = q_key

                circ.measure(qrs[qr_map[q_key]], crs[cr_map[c_key]])
            elif isinstance(instr, (Declare, Pragma)):
                continue
            elif isinstance(instr, Gate):
                if len(instr.modifiers) >= 1:
                    raise ValueError("TODO: Incorporate gate modifiers.")

                if instr.name in dg_map.keys():
                    self._transpile_defined_gate(
                        crs, qrs, circ, instr, cr_map, qr_map, dg_map
                    )
                else:
                    self._transpile_standard_gate(qrs, circ, instr, qr_map)
            else:
                raise ValueError("The program is not a ProtoQuil program.")

    # TODO: Is this the best way to decompose a user-defined gate?
    def _transpile_defined_gate(self, crs, qrs, circ, instr,
                                cr_map, qr_map, dg_map):
        """
        Transpile a defined gate using the decomposer built into the Quil
        compiler.
        """

        definition = dg_map[instr.name]

        # Create a small program with the single instruction
        p = Program()
        p += definition
        p += instr

        max_qubit = max([qubit.index for qubit in instr.qubits])
        qc = get_qc("%sq-qvm" % (max_qubit + 1))
        decomposition = qc.compiler.quil_to_native_quil(p)

        decomp_insts = decomposition.instructions
        self._transpile_instructions(
            crs, qrs, circ, decomp_insts, cr_map, qr_map, dg_map
        )

    @staticmethod
    def _transpile_standard_gate(qrs, circ, instr, qr_map):
        """ Add a single standard gate to the Qiskit circuit. """

        params = instr.params
        q_keys = [str(qubit) for qubit in instr.qubits]
        qiskit_qs = [qrs[qr_map[key]] for key in q_keys]
        if instr.name == "I":
            circ.iden(qiskit_qs[0])
        elif instr.name == "X":
            circ.x(qiskit_qs[0])
        elif instr.name == "Y":
            circ.y(qiskit_qs[0])
        elif instr.name == "Z":
            circ.z(qiskit_qs[0])
        elif instr.name == "H":
            circ.h(qiskit_qs[0])
        elif instr.name == "S":
            circ.s(qiskit_qs[0])
        elif instr.name == "T":
            circ.t(qiskit_qs[0])
        elif instr.name == "RX":
            circ.rx(params[0], qiskit_qs[0])
        elif instr.name == "RY":
            circ.ry(params[0], qiskit_qs[0])
        elif instr.name == "RZ":
            circ.rz(params[0], qiskit_qs[0])
        elif instr.name == "PHASE":
            circ.rz(params[0], qiskit_qs[0])
        elif instr.name == "CZ":
            circ.cz(qiskit_qs[0], qiskit_qs[1])
        elif instr.name == "CNOT":
            circ.cx(qiskit_qs[0], qiskit_qs[1])
        elif instr.name == "CCNOT":
            circ.ccx(qiskit_qs[0], qiskit_qs[1], qiskit_qs[2])
        elif instr.name == "CPHASE00":
            circ.x(qiskit_qs[0])
            circ.x(qiskit_qs[1])
            circ.cu1(params[0], qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[1])
            circ.x(qiskit_qs[0])
        elif instr.name == "CPHASE01":
            circ.x(qiskit_qs[0])
            circ.cu1(params[0], qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[0])
        elif instr.name == "CPHASE10":
            circ.x(qiskit_qs[1])
            circ.cu1(params[0], qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[1])
        elif instr.name == "CPHASE":
            circ.cu1(params[0], qiskit_qs[0], qiskit_qs[1])
        elif instr.name == "SWAP":
            circ.swap(qiskit_qs[0], qiskit_qs[1])
        elif instr.name == "CSWAP":
            circ.cswap(qiskit_qs[0], qiskit_qs[1], qiskit_qs[2])
        elif instr.name == "ISWAP":
            circ.swap(qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[0])
            circ.cu1(numpy.pi / 2, qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[0])
            circ.x(qiskit_qs[1])
            circ.cu1(numpy.pi / 2, qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[1])
        elif instr.name == "PSWAP":
            circ.swap(qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[0])
            circ.cu1(params[0], qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[0])
            circ.x(qiskit_qs[1])
            circ.cu1(params[0], qiskit_qs[0], qiskit_qs[1])
            circ.x(qiskit_qs[1])
        else:
            raise ValueError("The gate %s is unknown." % instr.name)
