# CPSC 3400 - Little Programs (LP1 - LP4)

## Overview
This subfolder contains all four "Little Programs" (LP1 to LP4) for my CPSC 3400 Languages and Computation class during Winter Quarter 2025.
Each program was designed to address or solve a specific task related to different aspects of computation and programming concepts.
Below I provide a brief description of each program's objectives and requirements.

### 1. Little Program 1 (LP1)
**Objective:** Write a Scheme program (using the GNU Guile dialect) to find the sum of all integers divisible by 3 or by 5 from the set N = {i | 0 < i < 30,000}. The program must only use the basic, out-of-the-box GNU Guile Scheme language, without external libraries. The output should display the sum of multiples of 3 or 5.

### 2. Little Program 2 (LP2)
**Objective:** Create a Scheme program (using the GNU Guile dialect) to find the sum of all even integers in the Fibonacci sequence whose values are less than 1 billion. The program should only use the basic GNU Guile Scheme language without external libraries. The output should display the sum of even Fibonacci numbers.

### 3. Little Program 3 (LP3)
**Objective:** Develop a Scheme program (using the GNU Guile dialect) to find the count of all games where the current player wins for all positive integers n <= 2^30 such that `nim-win(n, 2n, 3n) = 1`. This program simulates the Nim game with three heaps where the goal is to find all winnable configurations using a specified set of rules. The output should display the count of winning game configurations.

### 4. Little Program 4 (LP4)
**Objective:** Implement an automated Blackjack player using a Scheme program (GNU Guile dialect) that achieves a win rate of at least 40%. The program makes multiple simplifying assumptions to keep the implementation minimal, such as:
  - Aces always have a value of 1, face cards have a value of 10.
  - Only `hit` or `stay` are available actions.
  - No options for split, double down, or surrender.
  - Only one player and one dealer.
  - Infinite number of decks.

The program reads hands from a text file (`deck.scm`) and computes the win rate by analyzing the number of successful hands played. The output displays the number of wins over the total number of hands.