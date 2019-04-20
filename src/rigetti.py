import pyquil

backend_names = []

def init():
    global backend_names
    backend_names = pyquil.list_quantum_computers()
