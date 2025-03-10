# CPSC 3400-02 Languages & Computation
# Game 3
# Saxton Van Dalsen
# 3/9/2025

import sys
import json
import re

# Player class to track and update the state of the player through their location,
# direction, and inventory
class Player:
    # Constructor to hold and maintain players inventory, current location, and
    # the player's facing direction
    def __init__(self, direction, startLocation):
        self.inventory = []
        self.currentLocation = startLocation
        self.direction = direction
    
    # Movement of the player in the specified direction they choose, if able
    def move(self, direction, ship):
        currentRoom = ship.getRoom(self.currentLocation)
        if currentRoom:
            nextRoom = currentRoom.getNextRoom(direction)
        else:
            nextRoom = None

        if nextRoom:
            self.currentLocation = nextRoom
            print(f"You moved {direction} to {nextRoom}.")
        else:
            print("You can't go that way.")

    # Check and display current location of the player in case they forgot
    def checkLocation(self):
        print(f"You're current location is: {self.currentLocation}.")

    # Get current direction
    def checkDirection(self):
        print(f"You are currently facing: {self.direction}.")

    # Getting list of objects within current inventory
    def checkInventory(self):
        if self.inventory:
            print(f"Inventory: {', '.join(self.inventory)}")
        else:
            print("Your inventory is empty.")

    # Use action on an item from inventory, potentially interacting with another object
    def useItem(self, itemName, target, ship):
        if itemName in self.inventory:
            if target:
                print(f"You used {itemName} on {target}.")
            else:
                print(f"You used {itemName}.")
        else:
            print(f"You don't have {itemName} in your inventory.")

    # For taking an item from a room and add it to players inventory
    def takeItem(self, itemName, ship):
        currentRoom = ship.getRoom(self.currentLocation)

        # Check if an item exists in current room, then add to inventory and 
        # remove it from that room once taken
        if itemName in currentRoom.items:
            self.inventory.append(itemName)
            del currentRoom.items[itemName]
            print(f"You picked up: {itemName}.")
        else:
            print(f"There is no {itemName} here to take.")

    # Provide the user with information from where they're looking and/or see
    # items in the room
    def look(self, target, ship):
        currentRoom = ship.getRoom(self.currentLocation)
    
        # Displaying the details about specific items/objects in the room and
        # provide the room description and available ways to move
        if target:
            if target in currentRoom.items:
                print(f"{target}: {currentRoom.items[target]['description']}")
            else:
                print(f"There's no {target} to look at.")
        else:
            print(f"{currentRoom.description}")
            print(f"Exits: {', '.join(currentRoom.directions.keys())}")

# For defining all interactive objects within rooms in the game, their descriptions,
# and interaction abilities
class Item:
    def __init__(self, name, description, interactions, isKey=False, unlocks=None):
        self.name = name
        self.description = description
        self.interactions = interactions
        self.isKey = isKey
        self.unlocks = unlocks

    # Checking if the itme can be used at all
    def canInteract(self, action):
        return action in self.interactions
    
    # To use the item, checking if it unlocks anything
    def use(self, player, ship, target=None):
        # Checking if an item is a key to use to unlock a room, then it'll unlock that room
        # if not then it'll just handle the use case for the leaking pipe at the end 
        if self.isKey and self.unlocks:
            if self.unlocks in ship.rooms and ship.rooms[self.unlocks].isLocked():
                ship.rooms[self.unlocks].unlock()
                print(f"You used {self.name} to unlock {self.unlocks}.")
                return True
            else:
                print(f"{self.name} doesn't seem to unlock anything useful.")
                return False
        elif target:
            print(f"You used {self.name} on {target}.")
        else:
            print(f"You used {self.name}.")
        return True

# Ship class handles managing rooms, loading in the dungeon (json map), and 
# maintaining the room state
class Ship:
    def __init__(self, filePath=None):
        self.rooms = {} # To store rooms from json layout
        
        # Useful for the player to know how to run the game with a provided
        # json "dungeon" style map
        if not filePath:
            print("Error: No dungeon map provided.\n Run: python3 game3.py <dungeon.json>")
            sys.exit(1)
        
        # Loading the provided map on command line
        self.loadMap(filePath)
    
    # Loading the dungeon (map) from a json file and build Room objects based on it
    def loadMap(self, filePath):
        # Handling with try/catch this in case no json file passed in command line
        try:
            # Opening the json file in read mode
            with open(filePath, "r") as file:
                data = json.load(file)
                # 
                for roomName, roomData in data.items():

                    # Convert item list to a dictionary (key = objID)
                    itemDict = {item["objID"]: Item(item["objID"], item["description"], item["interactions"]) for item in roomData.get("objects", [])}
                    
                    self.rooms[roomName] = Room(
                        name=roomName,
                        description=roomData["description"],
                        directions=roomData.get("directions", {}),
                        items=itemDict,
                        locked=roomData.get("locked", False)
                    )
        except FileNotFoundError:
            print(f"Error: File '{filePath}' not found.")
            sys.exit(1)
        
    # Get and return a Room object
    def getRoom(self, roomName):
        room = self.rooms.get(roomName)
        if room is None:
            print(f"Error: Room '{roomName}' not found in ship.rooms.")
        return room
    
    # To unlock a room if Player has correct key/item in inventory to
    # access that room
    def unlockRoom(self, roomName):
        if roomName in self.rooms and self.rooms[roomName].locked:
            self.rooms[roomName].locked = False
            print(f"{roomName} is now unlocked.")
        else:
            print(f"{roomName} is already unlocked.")

    # Getting next room while facing given direction and making sure you can access it
    def getNextRoom(self, currentRoom, direction):
        if currentRoom in self.rooms:
            nextRoom = self.rooms[currentRoom].directions.get(direction, None)
            if nextRoom and nextRoom in self.rooms:
                return nextRoom
        return None

# Room class for defining each room properties, with all relevant information for
# smooth player interactions and understanding
class Room:
    def __init__(self, name, description, directions, items, locked=False):
        self.name = name
        self.description = description
        self.directions = directions
        self.items = items
        self.locked = locked

    # Getting the next connected rooms in a given direction
    def getNextRoom(self, direction):
        return self.directions.get(direction, None)

    # Checking if any items exist in the room
    def getItem(self, itemName):
        return self.items.get(itemName, None)

    # Updating room status of objects when player's takes a sitting item
    def removeItem(self, itemName):
        if itemName in self.items:
            del self.items[itemName]

    # Checking if room is unlocked to determine entrance or not
    def isLocked(self):
        return self.locked

    # Unlocking a room, setting to false
    def unlock(self):
        self.locked = False

# Originaly had a "Game" class to handle the flow and input handling but realized
# I could scratch that and simply use main for that
if __name__ == "__main__":
    # Getting json file from command line
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
    else:
        filePath = None

    # Hash set of usual stop words
    stopWords = {"the", "a", "an", "to", "on", "at", "in", "with"}

    # To sanitize the user's input first and remove the common stop words
    # to handle the actual verbs/actions
    def sanitizeInput(userInput):
        # Converting user input to lowercase and splitting
        words = userInput.lower().split()

        # To filter out the stop words from user input and store the
        # cleaned up words in a list
        filteredWords = []
        for word in words:
            if word not in stopWords:
                filteredWords.append(word)
        
        # Returning filtered words
        return " ".join(filteredWords)

    # Processing user input by first sanitizing it, using regular expressions to extract
    # verbs and relevant objects/directions to determine the player's intended action
    def parseInput(userInput):
        # Need to sanitize user input before parsing key words
        userInput = sanitizeInput(userInput)

        # Regex patterns for different possible commands
        movePattern = re.compile(r"^go\s+(north|south|east|west|n|s|e|w)$")
        takePattern = re.compile(r"^take\s+(.+)$")
        openPattern = re.compile(r"^open\s+(.+)$")
        usePattern = re.compile(r"^use\s+(.+?)(?:\s+on\s+(.+))?$")
        lookPattern = re.compile(r"^look(?:\s+(.+))?$")

        # Then searching for these matches on given input
        moveMatch = movePattern.search(userInput)
        takeMatch = takePattern.search(userInput)
        openMatch = openPattern.search(userInput)
        useMatch = usePattern.search(userInput)
        lookMatch = lookPattern.search(userInput)

        # Process matches and handling different edge cases based on user's input prompt
        if moveMatch:
            return ("GO", moveMatch.group(1), None)
        if takeMatch:
            return ("TAKE", takeMatch.group(1), None)
        if openMatch:
            return ("OPEN", openMatch.group(1), None)
        if useMatch:
            return ("USE", useMatch.group(1), useMatch.group(2) if useMatch.group(2) else None)
        if lookMatch:
            return ("LOOK", lookMatch.group(1) if lookMatch.group(1) else None, None)
        
        # Handling different edge cases based on user's input prompt
        return (None, None, None)
    
    # Displaying the game introduction
    # Going to add a more fun narrative at the beginning
    print("Your goal: Find and collect the necessary tools to fix a leaking pipe in the engine room.")
    print("Explore different rooms, take items, and use them where needed.")
    print("Commands: 'go <direction>', 'take <item>', 'use <item>', 'look', 'quit'.")
    print("-------------------------------------------------------------------------------")
    
    # Loading in the json file into my ship class and starting the player at the beginning
    ship = Ship(filePath)
    player = Player("north", "crew_quarters")

    # Providing the player the option to play again or not once
    # beating the game. The game loop
    while True:
        # Show current location description and available directions
        currentRoom = ship.getRoom(player.currentLocation)

        # To verify that the player's current location exists in the ship's rooms 
        # before accessing its attributes, was running into None error on a few rooms
        # used for troubleshooting
        if currentRoom is None:
            print(f"Error: Room '{player.currentLocation}' not found in ship.rooms.")
            sys.exit(1)

        print(f"\nYou are in {currentRoom.name}.")
        print(f"{currentRoom.description}")
        print(f"Exits: {', '.join(currentRoom.directions.keys())}")

        # Show available objects in the room
        if currentRoom.items:
            print("You see:")
            for itemName, item in currentRoom.items.items():
                print(f"- {itemName}: {item.description}")

        # Getting user input and parsing that
        userInput = input("\n> ").strip().lower()
        verb, obj1, obj2 = parseInput(userInput)

        # Giving option to quit and handling that
        if userInput in ["quit", "exit"]:
            print("Exiting game. Thanks for playing!")
            break

        # Checking for user input to move to another room and if there
        # is a door thats locked
        elif verb == "GO":
            if currentRoom.isLocked():
                print("The door is locked. You need a key to proceed.")
            else:
                player.move(obj1, ship)

        # Check for taking an item
        elif verb == "TAKE":
            player.takeItem(obj1, ship)

        # Able to use an item in the ship
        elif verb == "USE":
            if obj2:
                player.useItem(obj1, obj2, ship)
            else:
                player.useItem(obj1, None, ship)

        # Handle looking at an object or around the room
        elif verb == "LOOK":
            player.look(obj1, ship)

        # Invalid input prompt, keep them aware
        else:
            print("Invalid command. Try 'go <direction>', 'take <item>', 'use <item>', 'look', or 'quit'.")

        # Check if the player has completed the game, as fixing the leak is the objective
        if player.currentLocation == "engine_room" and "wrench" in player.inventory and "pipe_tape" in player.inventory:
            print("\nYou use your tools to fix the leaking pipe in the engine room!")
            print("The Captain awards you a medal for your quick thinking and problem-solving skills.")
            print("Congratulations, you've beat the game!\n")

            # Asking if they'd like to play again
            playAgain = input("Would you like to play again? (yes/no): ").strip().lower()
            
            if playAgain == "yes":
                # Reset player and game state
                ship = Ship(filePath)
                player = Player("north", "crewQuarters")
                print("\nRestarting game...\n")
            else:
                print("Thanks for playing! Goodbye.")
                break