# ES170 Final Project Proposal
*Nicholas Boucher, Nathanael Cho, Juan Esteller, Brian Sapozhnikov*

April 1, 2019

## Overview

We aim to make quantum programming more attainable and accessible through designing and implementing a transpiler from a well-defined programming language of our own design to QisKit (or directly to `qasm`).

## Implementation

## Language Design

Specifically, we will design a programming language that enforces the following features through language design:

- Gates will be abstracted as functions and other syntactic elements (e.g. conditional statements)
- Functions can be non-recursively nested
- Measurement will occur only at the end of the program
- Measurement will be defined as a `return` statement at the end of the `main` function
- Abstraction of physical notion of superposition to computational/semantic notion will allow the programmer to leverage quantum computation without having to reason about physical systems

### Additional Language Features

We will also investigate the possibility/tractability of adding the following features:

- Recursive functions and mutually recursive functions
- A richer type system

## Approach

First, we will engage in a literature review to gain a deeper understanding of pre-existing work. We will then experiment with pre-existing quantum languages and gauge where we believe they fall short.

The final deliverable of this project will be a working transpiler from our new language to Python3/QisKit, which will enable us to target IBM's `qasm`.

### Schedule

Our time will be split up into three general periods:

1. Planning (1 week)
  - Literature review
  - Concrete language feature selection
  - Written in-depth language feature specifications
2. Implementation (2 weeks)
  - Implementation of basic language/compilation framework
  - Implementation of features
  - Rigorous testing of code
  - Iterative update of feature specifications as necessary
3. Loose Ends / Reach Goals / Presentation (1 week)
  - Implementation of additional language features/extensions (time-permitting)
  - Generation of example programs
  - Presentation material preparation

### Division of Work

The planning phase will be fairly divisible - we will work together to compile a starting list of literature, then each of us will be responsible for understanding a subset of that list (and other sources found from investigating those) and reporting back to the rest of the group. We will then work together to choose, and generate a specification for, particular language features to implement.

We plan to divide the implementation by feature, where (depending on the nature of the final list of features) either each of us will be responsible for implementing and testing some subset of the features or we will divide the features into two groups and work in pairs.

Time permitting, we will divide up the additional language features we would like to implement, doing so using the same division of work used for the implementation phase. We will then work together to generate some example programs that demonstrate these features well, possibly splitting up after developing a list of programs we would like to implement. We will jointly develop an outline for our presentation and use that to split up the preparation of the presentation material evenly.
