# CPSC 3400 - Languages and Computation

## Overview
This repository contains programming assignments, in-class programs, and presentation materials completed as part of the CPSC 3400 Languages and Computation course. The course focused on fundamental concepts related to programming languages, computation theories, and functional programming using Scheme, Python, and Rust. Topics covered include regular expressions, language classification, grammars, finite state automata, higher-order functions, and closures.

The repository is organized into several subfolders, each focusing on different aspects of the coursework:

---

### Game Assignments (game-1, game-2, game-3)
These folders contain various assignments related to game tree traversal and parsing, implemented in Python. Each game assignment involves designing programs to process input files (`svandalsen.tree` and `svandalsen.json`) and produce outputs based on the specifications of the problem.

- **game-1:** Python program for tree traversal and evaluation based on a provided `.tree` file.
- **game-2:** Python program building upon starter code given and focusing on Mark and Sweep implementation.
- **game-3:** Python program working with a JSON-based input file, focusing on parsing and data processing.

---

### In-Class Programs (InClassProg)
This folder includes introductory and demonstration programs developed during class sessions, showcasing concepts related to:
- Basic Python programming
- Scheme programming
- Understanding functional programming principles

---

### Introduction (introduction)
Contains basic introductory programs written in Python, including:
- `helloworld.py`: A simple 'Hello World' program.
- `prime.py`: A program for checking prime numbers.
- `sumRange.py`: A program calculating sums over a specified range.

---

### Little Programs (LittlePrograms)
This folder contains the four main programming assignments completed throughout the course, written in Scheme (GNU Guile dialect):

1. **LP1:** Sum of all integers divisible by 3 or 5 from a specified range using functional programming techniques.
2. **LP2:** Summing even Fibonacci numbers below 1 billion using recursive function definitions.
3. **LP3:** Implementation of the Nim game logic to count winning configurations for specified inputs.
4. **LP4:** Automated Blackjack player simulation achieving a win rate of at least 40% by evaluating various game scenarios using a predefined deck file.

The folder includes the associated `deck.scm` file required for LP4. Each program focuses on functional programming principles, recursion, and higher-order functions in Scheme.

---

### Presentation (Presentation)
Contains code written in Rust for demonstrating program implementation and syntax differences between Scheme and Rust. Files include:
- `helloworld.rs`: Simple 'Hello World' example in Rust.
- `lp1.rs`, `lp2.rs`: Rust implementations of LP1 and LP2 for comparative analysis.

---

### Course Outcomes & Description
The coursework focused on understanding the core principles of programming languages and computation, including:
- Writing Python programs using various data structures (lists, tuples, dictionaries, etc.) and regular expressions.
- Converting between DFAs, NFAs, and regular expressions.
- Context-free grammar generation and understanding language classification.
- Differentiating between interpretation, compilation, and translation.
- Understanding names, values, memory management, types, and variables.
- Implementing functional programming techniques and addressing garbage collection challenges with a focus on the Mark and Sweep technique.
- Understanding Turing Machines and the Halting Problem.

This repository provides a complete overview of the programming-related tasks for the course, showcasing comprehension of different programming paradigms and computation concepts.

---

## How to Run
Python and Scheme programs can be run using standard interpreters (e.g., Python 3 and GNU Guile). Rust programs can be compiled and executed using `rustc` or `cargo`.