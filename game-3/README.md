# Game Lab 3 - Text-Based Adventure Game

## Overview
This assignment involves building a **text-based adventure game (dungeon crawl)** using Python. The game allows players to navigate through a maze of connected rooms, interacting with various objects and enemies using natural language commands. The project demonstrates concepts of **natural language processing (NLP)**, **state management**, and **JSON-based world descriptions**.

## Objective
The program must:
- Parse and interpret user inputs using predefined commands (`GO`, `TAKE`, `OPEN`, `USE`, `LOOK`) to interact with the game environment.
- Process directions, objects, and combat scenarios if implemented.
- Write and utilize a JSON file to describe the dungeon layout, including rooms, objects, and their interactions.
- Maintain state information to ensure progress is saved and appropriately handled throughout the game.

## Dungeon Description Schema
- The game world is described by a JSON file containing:
  - Rooms, each defined by ID and connections to other rooms.
  - Objects within rooms that can be interacted with.
  - Descriptions providing narrative context.
  - Verbs indicating possible interactions (`USE`, `TAKE`, `THROW`, `LOOK`, `OPEN`).
- The JSON file must be passed as a command-line argument when running the game.

## Requirements
- The game world must contain at least **five rooms** with a minimum of **three interactive objects per room**.
- Verbs must be processed and sanitized to account for natural language input variations.
- The player must be informed of valid commands at the beginning of the game.
- The game must include sufficient comments to explain the core logic and functions used.