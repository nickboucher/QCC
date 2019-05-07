cat test/resources/quil/src_01.quil
qcc -v 2 test/resources/quil/src_01.quil --target ibmq_qasm_simulator
cat test/resources/qasm/src_01.qasm
qcc -v 2 test/resources/qasm/src_01.qasm --target 9q-square-qvm --stats -o /tmp/output
cat /tmp/output
qcc -v 2 test/resources/qasm/src_01.qasm --auto-target -o /tmp/output
cat /tmp/output
