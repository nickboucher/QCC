import qiskit

class IBMQ(object):
    def __init__(self):
        qiskit.IBMQ.load_accounts()

        self.backends = filter(self.filter_backend, self.load_backends())
        self.backend_names = [b.name() for b in self.backends]

    @staticmethod
    def filter_backend(backends):
        return 'qasm' not in backends.name()

    def init_ibmq_accounts():
        qiskit.IBMQ.load_accounts()

    def load_backends(self):
        return qiskit.IBMQ.backends()

