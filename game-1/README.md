# Game Lab 1 - Twenty Questions

## Overview
This assignment implements a simple Twenty Questions game using Python. The game follows the structure of a **binary tree** to simulate a computerized version of the classic parlor game where a player attempts to guess what another person is thinking by asking yes or no questions. The goal is to progressively narrow down the answer through a series of questions until a correct guess is made or the question limit is reached.

## Objective
The program must:
- Use a binary tree data structure to represent a dialogue tree for questions and answers.
- Support both interactive gameplay and learning by updating the tree with new knowledge when the player successfully stumps the computer.
- Allow loading of a pre-defined tree from a file passed as a command-line argument.
- Write updated trees back to files for future use.

## Requirements
- When a player wins, the agent asks what the correct answer was and prompts the user to provide a question that differentiates the new answer from the previous leaf node.
- When a player loses, the agent gloats and asks if the player wants to play again.
- The agent must ask questions from the tree until the question limit (20 questions) is reached or until the correct answer is guessed.
- The game must include sufficient comments to explain the core logic and functions used.