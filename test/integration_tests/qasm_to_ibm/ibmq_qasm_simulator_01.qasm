Request: compile qasm to ibmq_qasm_simulator
Direct compilation path found: compiling directly
Result below:
OPENQASM 2.0;
include "qelib1.inc";
qreg qr[4];
creg cr[4];
z qr[3];
y qr[2];
x qr[1];
h qr[0];
cx qr[0],qr[3];
barrier qr[0],qr[1],qr[2],qr[3];
u3(0.300000000000000,0.200000000000000,0.100000000000000) qr[2];
if(cr==1) z qr[2];
u2(0.300000000000000,0.200000000000000) qr[1];
u1(0.785398163397448) qr[1];
id qr[1];
u1(0.300000000000000) qr[0];
u1(1.570796326794897) qr[0];
measure qr[0] -> cr[0];