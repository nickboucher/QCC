#!/usr/bin/env python3
import numpy
from pyquil import get_qc
from pyquil.quilbase import Declare, Gate, Halt, Measurement, Pragma, \
    Reset, ResetQubit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit

import qcc.assembly
from qcc.compilers.direct_compilers import QASM_IBM_Compiler
from qcc.hardware import IBM, Rigetti
from qcc.interfaces import Compiler

# TODO: A lot of testing.


class Intermediary_IBM_Compiler(Compiler):
    """ Compiles Intermediary Language to IBM """

    def compile(self, source, target_lang):
        """ Compile from the intermediary language to QASM. """

        # TODO: Move any functionality out that depends on the specific
        #   implementation of the intermediary language.
        program = source.quil.program
        instructions = program.instructions

        # TODO: Expand from ProtoQuil programs to anything IBM can handle.
        if not program.is_protoquil():
            raise ValueError("The Quil program is not a ProtoQuil program.")

        # TODO: Deal with DEFGATEs.
        # TODO: Deal with gate modifiers (DAGGER and CONTROLLED).
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

        compiled_circuit = self._compile_circuit(circuit, target_lang)
        return IBM(compiled_circuit)

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
                if instr.name in dg_map.keys():
                    raise ValueError("TODO: Implement defined gates.")

                if len(instr.modifiers) >= 1:
                    raise ValueError("TODO: Incorporate gate modifiers.")

                self._transpile_standard_gate(qrs, circ, instr, qr_map)
            else:
                raise ValueError("The program is not a ProtoQuil program.")

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

    # TODO: Verify that the code works once IBM comes back up.
    @staticmethod
    def _compile_circuit(circuit, target_lang):
        """ Compile the circuit for the specific target language. """

        # Not ideal, since we go to QASM then back to the circuit.
        qasm = qcc.assembly.QASM(circuit.qasm())
        compiler = QASM_IBM_Compiler()
        return compiler.compile(qasm, target_lang)


class Intermediary_Rigetti_Compiler(Compiler):
    """ Compiles Intermediary Language to Rigetti """

    # TODO: Test once we set up the Rigetti account.
    @staticmethod
    def compile(source, target_lang):
        """ Compile from the intermediary language to a Quil program. """

        program = source.quil.program
        qc = get_qc(target_lang)
        compiled_program = qc.compiler.quil_to_native_quil(program)
        return Rigetti(compiled_program)
