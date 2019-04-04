The following is the result of investigating Quil and related technology.
Some of this may be general to other langauges/frameworks.

# Names of Things #
- Quil: target assembly language
- PyQuil: Python library for generating, simulating, and evaluating Quil
- QVM: backend for classical simulation of Quil (fake quantum)
- QPU: Rigetti physical Quil evaluator (real quantum)

# Quil #
The only instructions that are natively supported by Rigetti are:
- `RX`
- `RY`
- `RZ`
- `MEASURE`

# PyQuil #
PyQuil offers an expanded range of value quantum instructions, as well some nice functions for working with classical gates

See https://pyquil.readthedocs.io/en/stable/ for more info / reference

## Quantum Instructions ##
- Identity
- `X`, `Y`, `Z`
- `H`
- `S`, `T`
- `RX`, `RY`, `RZ`
- `PHASE`
- `CZ`
- `CNOT`, `CCNOT`
- `CPHASE00`, `CPHASE01`, `CPHASE10`, `CPHASE`
- `SWAP`, `CSWAP`, `ISWAP`, `PSWAP`

## Classical Instructions ##
- `WAIT`, `RESET`, `NOP`, `HALT`
- `MEASURE`
- `NEG`
- `NOT`, `AND`, `OR`
- `LOAD`, `STORE`
- ...

## Other Nice Language Features ##
- Can add gates to a program with addition: `prog += H(0)`
- can create "cyborg" programs with quantum programs nested in classical programs:
  - `prog.while_do(classical_reg, q_prog)`
  - `prog.if_then(...)`
