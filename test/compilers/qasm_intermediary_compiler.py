from qcc.compilers import QASM_Intermediary_Compiler
from qcc.assembly import QASM

qasm_str = """OPENQASM 2.0;
include "qelib1.inc";
qreg qr[4];
creg cr[4];
h qr[0];
x qr[1];
y qr[2];
z qr[3];
cx qr[0],qr[3];
barrier qr[0],qr[1],qr[2],qr[3];
u1(0.300000000000000) qr[0];
u2(0.300000000000000,0.200000000000000) qr[1];
u3(0.300000000000000,0.200000000000000,0.100000000000000) qr[2];
u1(1.570796326794897) qr[0];
u1(0.785398163397448) qr[1];
id qr[1];
if(cr==1) z qr[2];
measure qr[0] -> cr[0];"""

qasm_program = QASM(qasm_str)

compiler = QASM_Intermediary_Compiler()

interm = compiler.compile(qasm_program)

print(interm.quil)
