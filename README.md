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

In order to use any QUIL functionality, you must also have the [Rigetti Forest SDK](https://www.rigetti.com/forest) installed.

## Testing ##

To run the test suite, simply run `python test/run_tests.py`

To add tests simply add the appropriate files, using the existing tests as examples.
Make sure to add `__init__.py` files where appropriate to ensure correct discovery of test scripts.
All test script files should start match the form `test*.py`.
All `unittest` methods should start with `test` and use assertions and other useful features of the `unittest` package.

## MyPy for Development ##

You can perform type checking for this codebase using `mypy` with the following commands from the root repo directory:

```
pip install mypy
export MYPYPATH="./stubs"
mypy qcc/
```
