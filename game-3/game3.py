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

# After reading through and thinking about how to go about creating my own text-based dungeon crawl
# style game I decided that an object oriented approach would make the most sense.

# Player class
class Player:
    def __init__(self, inventory, location):
        self.inventory = inventory
        self.location = location
    

    def checkLocation():

# To define object and how to interact with them    
class Object:

# To handle navigating through through rooms in the ship
class Ship:

# Define each room, the objects in that room, and how you can interact within each
class Room:

# Handle the game flow and logic
class Game: