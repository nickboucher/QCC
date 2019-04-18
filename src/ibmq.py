import qiskit

class IBMQ(object):
    def __init__(self):
        qiskit.IBMQ.load_accounts()

        backends = filter(self.filter_backend, self.load_backends())
        self.backend_names = [b.name() for b in backends]

        # convert to dictionary
        self.backends = {}

        for b in backends:
            self.backends[b.name()] = b

    @staticmethod
    def filter_backend(backends):
        return 'qasm' not in backends.name()

    def init_ibmq_accounts():
        qiskit.IBMQ.load_accounts()

    def load_backends(self):
        return qiskit.IBMQ.backends()

