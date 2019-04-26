# QCC
Quantum Code Compiler
*Nicholas Boucher, Nathanael Cho, Juan Esteller, Brian Sapozhnikov*

This is the final project for Harvard's ES170.

## Installation

### Install Pip Components

In order to use any of the Python code in this repository, the package must be installed (preferably using `pip` instead of `easy_install`).

If you are actively developing this package, be sure to install the package with the `-e` editable flag. For example, from the root directory of this repository:
```bash
pip install -e qcc/
```
### Install Rigetti Components

In order to use any QUIL functionality, you must also have the [Rigetti Forest SDK](https://www.rigetti.com/forest) installed. After that, you must run the following command in a separate terminal:
```bash
quilc -S
```

## MyPy for Development ##

You can perform type checking for this codebase using `mypy` with the following commands from the root repo directory:

```
pip install mypy
export MYPYPATH="./stubs"
mypy qcc/
```
