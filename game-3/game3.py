# CPSC 3400-02 Languages & Computation
# Game 3
# Saxton Van Dalsen
# 3/9/2025

# It's WWII and you're on some old ship and you need to find where the leaking pipe is
# (or something like that). Start out with an introduction dialogue to let the player know
# the situation and what to do. Assess them in the starting/current room there in, maybe
# have it where you get woken up by a shipmate and they tell you that you need to fix it
# but you usually have your toolbag in your room but it's not there. So you need to gather
# explore to find tools and your way around the ship to find the leak.
# - Text based adventure game, basically like in the form of a "text-based dungeon crawl"
# - where the player starts with a given setting and environment, provided instructions, and how
# - to play the game.
# - Include instructions for playing the game and print out available verbs for you're game
# - Minimum 5 rooms, looking to make 6 then with three interactive objects in each
# - When players input text, it should be handled by parsing the input, stripping the stop words
#   then passed through a regular expression matcher to determine verbs and objects/direction
#   by player's input.
# - The dungeon 

# You'll need to get the key from Machinery Technician to get into the engine room to fix the pipe

# After reading through and thinking about how to go about creating my own text-based dungeon crawl
# style game I decided that an object oriented approach would make the most sense.

import sys
import json

# Player class
class Player:
    def __init__(self, direction, start_location):
        self.inventory = []
        self.location = start_location
        self.direction = direction

    # To get and display the current location of the player in case they forgot
    def checkLocation():
        print("You're current location is: {location}")

    def checkDirection():
        print("You are currently facing: " {direction})

    # To access and check objects within your current inventory
    def checkInventory():

    # To access and use an item from your inventory
    def useItem():



# To define items throughout the game    
class Item:
    def __init__(self, name, description, interactions):
        self.name = name
        self.description = description
        self.interactions = interactions # For the verb actions on items


# To handle navigating through through rooms in the ship
class Ship:
    def __init__(self, file_path=None):
        self.rooms = {} # To store rooms from json layout
        
        # Useful for the player to know how to run the game with a provided
        # json "dungeon" style map
        if not file_path:
            print("Error: No dungeon map provided.\n Run: python3 game3.py <dungeon.json>")
            sys.exit(1)
        
        self.load_map(file_path) # Loading the provided map on command line
    
    # To load in a given map (dungeon)
    def load_map(self, file_path):
        # To load in json file from command line in read mode
        try:
            with open(file_path, "r") as file:
                self.rooms = json.load(file)
        # Used to troubleshoot command line loading json file
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)


# Define each room, the objects in that room, and how you can interact within each
class Room:
    def __init__(self, name, description, directions, items):
        self.name = name
        self.description = description
        self.directions = directions
        self.items = items

# Handle the game flow and logic
class Game:
    def __init__(self,):


if __name__ == "__main__":
    