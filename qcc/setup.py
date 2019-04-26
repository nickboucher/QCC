import setuptools

setuptools.setup(
    name="qcc",
    version="0.0.1",
    author="Nicholas Boucher, Nathanael Cho, Juan Esteller, Brian Sapozhnikov",
    description="Quantum Code Compiler",
    long_description="Cross-compiles quantum assembly codes",
    url="https://github.com/nickboucher/QCC",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['qcc=qcc.command_line:main'],
    },
    install_requires = [
        'qiskit',
        'configparser',
        'pyquil',
        'pyduktape'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
