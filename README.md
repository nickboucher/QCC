# QCC
Quantum Compiler Collection
*Nicholas Boucher, Nathanael Cho, Juan Esteller, Brian Sapozhnikov*

QCC is a python package supporting cross-compilation between different quantum assembly languages. The goal of QCC is to remove barriers for quantum developers by allowing applications to target arbitrary hardware without rewriting source code. Additionally, QCC aims to help developers identify the *best* hardware on which to run their code. Due to engineering differences, different quantum hardware excel in different areas; QCC can help developer to figure out and use the hardware that will give them the best results.

At this time, QCC's supported quantum assembly languages are `QASM` and `Quil`.

QCC is the final project for Harvard course ES170.

## Installation

Installation of QCC requires two steps: installing the Python components and installing the Rigetti components.

### Installing Python Components

In order to use any of the Python code in this repository, the package must be installed (preferably using `pip` instead of `easy_install`). After cloning the repository and `cd`ing to the root of the repo, an example installation is:
```bash
pip install qcc/
```

If you are actively developing this package, be sure to install the package with the `-e` editable flag. For example, from the root directory of this repository:
```bash
pip install -e qcc/
```

Note that the code for QCC is written in Python 3 and requires at Python 3.5 or newer.

### Installing Rigetti Components

QCC depends on a compilation tool built by Rigetti. As such, in order to use most of the functionality of QCC you must have the [Rigetti Forest SDK](https://www.rigetti.com/forest) installed.

## Usage

QCC is typically invoked as a command line tool. After following the above installation instructions, the command `qcc` will automatically be added to the current user's `$PATH`. After this `qcc` can be invoked system-wide from the command line. Note that if qcc was installed in a `virtualenv`, that environment must be active on order for the `qcc` command to work.

For example, running the following line from the command line will display help information:
```bash
qcc --help
```

The arguments to `qcc` are as follows:
```
usage: qcc [-h] [--target TARGET] [--auto-target] [-m METRIC] [--profiles]
           [--stats] [-v {1,2}] [-o OUTPUT_FILE]
           source-file
```
These arguments are defined as follows:

- Required Arguments:
  - `source-file`: The source file containing a program in a supported quantum assembly language.
  - Exactly one of:
    - `target`: the specific hardware to target -- must be an option output from `list`
    - `auto-target`: automatically select the optimal hardware for the source program
    - `profiles`: like auto-target, but only prints statistics for each potential target instead of printing the cross-compiled code
    - `list`: lists all hardwares available for `target`
- Optional Arguments:
  - `metric`: allows the user to specify the metric chosen by auto-target. Possible options are: `num_2_qubit_gates` and `num_insts`
  - `stats`: in addition to printing the output for `target`, will also print the statistics for that target hardware
  - `verbose`: specifies the level of verbosity in output -- possible values are `1` and `2`, where 1 is the default and 2 prints out more verbose output
  - `o`: optionally specifies an output file instead of printing to STDOUT
  - `help`: prints the help instructions


  Additionally, the `list` verb can be invoked to list all of the target hardwares supported by QCC.

## Testing

To run the test suite, simply run `python test/run_tests.py`

To add tests simply add the appropriate files, using the existing tests as examples.
Make sure to add `__init__.py` files where appropriate to ensure correct discovery of test scripts.
All test script files should start match the form `test*.py`.
All `unittest` methods should start with `test` and use assertions and other useful features of the `unittest` package.

### Type Checking

You can perform type checking for this codebase using `mypy` with the following commands from the root repo directory:

```
pip install mypy
export MYPYPATH="./stubs"
mypy qcc/
```
