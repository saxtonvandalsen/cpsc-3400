# CPSC 3400-02 Languages & Computation
# Game 3
# Saxton Van Dalsen
# 3/11/2025

import sys
import json
import re

# Player class to track and update the state of the player through their location,
# directions, and inventory. I realized objects needed to be created, readable/actionable,
# and manipulation for dynamic state change throughout the program, I read from Part 2 
# and kept it noted throughout creating my object oriented approach to the game.
# I kept naming standard of snake_case style for json keys of rooms and object IDs naming to help 
# differentiate map data from Python variables and objects. Helped a lot with troubleshooting/
# debugging in game structure and in input/output statements
class Player:
    # Constructor to hold and maintain players inventory, current location, and
    # the player's facing direction
    def __init__(self, direction, startLocation):
        self.inventory = []
        self.currentLocation = startLocation
        self.direction = direction
    
    # Movement of the player in the specified direction they choose, if able
    # and handling different cases based on input
    def move(self, direction, ship):
        currentRoom = ship.getRoom(self.currentLocation)
        
        # Validation check when troubleshooting before proceeding, come back to
        if not currentRoom:
            print("Error on current location")
            return

        # Getting the next room based on players chosen direction to go/move
        nextRoomName = currentRoom.getNextRoom(direction)
        nextRoom = ship.getRoom(nextRoomName)

        # Checking if there is a room in that direction
        if not nextRoom:
            print(f"You can't go {direction} from here.")
            return

        # Checking first if a room is locked before allowing entry
        if nextRoom.isLocked():
            print(f"The door to {nextRoomName} is locked. You need a key to enter.")
            return

        # Moving the player to the next room
        self.currentLocation = nextRoomName
        print(f"You moved {direction} to {nextRoomName}.")


    # Check and display current location of the player in case they forgot
    # condensed location/direction helper funcitons into one for ease
    def checkLocation(self):
        print(f"You're currently in the {self.currentLocation} facing {self.direction}")

    # Getting list of objects within current inventory, so you can check while exploring around
    def checkInventory(self):
        if self.inventory:
            print("\nYou currently have in your inventory:")
            for item in self.inventory:
                print(f"- {item.name}")
        else:
            print("\nYour inventory is empty.")

    # Handling using an item from players inventory, unlockinga room with a key 
    # and interacting with a target if possible
    def useItem(self, itemName, target, ship):
        # Searching for the item player is trying to use in inventory
        # matching by name
        item = None
        for i in self.inventory:
            if i.name == itemName:
                item = i
                break

        if not item:
            print(f"You don't have {itemName} in your inventory.")
            return

        # Checking if its a key and will be able to unlock the engine room
        if item.isKey and item.unlocks == "engine_room":
            # Getting engine room and checking if locked then unlock with key
            engine_room = ship.getRoom("engine_room")
            if engine_room and engine_room.isLocked():
                engine_room.unlock()
                
                print(f"You used {item.name} to unlock the engine room.")
            else:
                print(f"The engine room is already unlocked.")
            return

        # If the item has an intended target, use it on that
        if target:
            print(f"You used {item.name} on {target}.")
        else:
            print(f"You used {item.name}.")


    # For taking an item from a room and add it to players inventory
    def takeItem(self, itemName, ship):
        currentRoom = ship.getRoom(self.currentLocation)

        # Check if an item exists in current room, then add item object to inventory and 
        # remove it from that room once taken
        if itemName in currentRoom.items:
            item = currentRoom.items[itemName]
            self.inventory.append(item)
            # Updating current rooms objects/items if player takes it
            del currentRoom.items[itemName]
            print(f"You picked up: {itemName}.")
        else:
            print(f"There is no {itemName} here to take.")

    # Provide the user with information from where they're looking and/or see
    # items in the room
    def look(self, target, ship):
        # Get room from where player currently is
        currentRoom = ship.getRoom(self.currentLocation)
    
        # Displaying the details about specific items/objects in the room and
        # provide the room description and available ways to move
        if target:
            if target in currentRoom.items:
                # Printing description
                print(f"{target}: {currentRoom.items[target]['description']}")
            else:
                print(f"There's no {target} to look at.")
        else:
            print(f"{currentRoom.description}")

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
    
    # To use the item and checking for specific key functionality, checking if it unlocks anything
    # for the player
    def use(self, player, ship, target=None):
        # Checking if an item is a key to use to unlock a room, then it'll unlock that room
        # if not then it'll just handle the use case for the leaking pipe at the end 
        if self.isKey and self.unlocks:
            # Checking room exists and is currently locked before unlocking it
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
# help work/interact with the rooms within the ship
class Ship:
    def __init__(self, filePath=None):
        self.rooms = {}
        # Useful error message for the player to know how to run the game
        # with a provided json "dungeon" style map
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
                # Processing the loaded json data through each room
                for roomName, roomData in data.items():
                    # A lot of troubleshooting to correctly filter and get the "directions" dictionary
                    # for each room loaded based on json data. They weren't loading in from
                    # json and I couldn't move or go through rooms.
                    directions = {}
                    for key, value in roomData.items():
                        if key not in ["description", "objects", "locked"]:
                            directions[key] = value

                    # Convert item list to a dictionary using objID as the key
                    itemDict = {}
                    # Iterating through the item list, getting data specifics then 
                    # storing them as Item objects
                    for item in roomData.get("objects", []):
                        objID = item["objID"]
                        description = item["description"]
                        interactions = item["interactions"]
                        # Storing data into item dictionary from construction of Item object
                        itemDict[objID] = Item(objID, description, interactions)
                    
                    # Creating Room object using the parsed data and storing it then
                    # in the ships room dictionary where room name is key
                    self.rooms[roomName] = Room(
                        name=roomName,
                        description=roomData["description"],
                        directions=directions,
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
            # Letting the player no you can't go that way
            print("Inaccessible shipmate.")
        return room
    
    # To unlock a room if Player has correct key/item in inventory to
    # access that room
    def unlockRoom(self, roomName):
        # If a specific room with the name is currently locked, then unlock it
        # this will be used in correlation with having a key in players inventory
        if roomName in self.rooms and self.rooms[roomName].locked:
            self.rooms[roomName].locked = False
            print(f"{roomName} is now unlocked.")
        else:
            print(f"{roomName} is already unlocked.")

    # Getting next room while facing given direction and making sure you can access it
    def getNextRoom(self, currentRoom, direction):
        if currentRoom in self.rooms:
            # Getting next room based on current direction if a room exists in ships
            # room dictionary. validation check
            nextRoom = self.rooms[currentRoom].directions.get(direction, None)
            if nextRoom and nextRoom in self.rooms:
                return nextRoom
        return None

# Room class for defining each room properties, with all relevant information for
# smooth player interactions in the rooms and understanding the setting for the player
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

    # Additionally open verb with object check will be handled as well in main
    # if the player wants to use this verb rather
    def open(self):
        if self.locked:
            print(f"{self.name} is locked. You need a key to open it.")
            return False
        print(f"You opened {self.name}. You can now enter.")
        return True

# Initially was trying and considered a Game class to separate and manage input handling and game flow
# but realized later it worked better to handle it within main. Helps for direct user input processing
if __name__ == "__main__":
    # Getting json file from command line
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
    else:
        filePath = None

    # Hash set of usual stop words
    stopWords = {"the", "a", "an", "to", "on", "at", "in", "with", "i", "will", "well", "then", "my"}

    # To sanitize the user's input first and remove the common stop words
    # to handle the actual verbs/actions. My approach to it based on assignment breakdown
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
    # verbs and relevant objects/directions to determine the player's intended action. This took
    # the most work/time to get some functioning user input to actionable gameplay
    def parseInput(userInput):
        # Must sanitize user input before parsing key words
        userInput = sanitizeInput(userInput)

        # Regex patterns for different possible commands, handling spaces within input line
        # and matches on sequences of input words or items. Trying to match as many with different user
        # inputs as possible
        movePattern = re.compile(r"^go\s+(north|south|east|west|n|s|e|w)$")
        takePattern = re.compile(r"^take\s+(.+)$")
        openPattern = re.compile(r"^open\s+(.+)$")
        usePattern = re.compile(r"^use\s+(.+?)(?:\s+on\s+(.+))?$")
        useKeyPattern = re.compile(r"^use\s+key$")
        lookPattern = re.compile(r"^look(?:\s+(.+))?$")

        # Added additional regex patterns, during testing, for checking or looking at tools
        # in toolbage (inventory) and to be able to interact and fix the leaking pipe at the end
        checkToolsPattern = re.compile(r"^(check|look at)\s+(inventory|objects|items|tools|toolbag)$")
        fixPipePattern    = re.compile(r"^(use|fix)\s+(tools|toolbag|leaking pipe|fix leaking pipe)$")

        # I was running into trouble trying to parse certain phrases for my game so I 
        # added some common phrases to be converted to actionable commands
        if userInput in ["where am I", "check my location", "current location", "current direction"]:
            return ("LOOK", "around", None)
        
        if userInput in ["look around", "look here"]:
            return ("LOOK", "around", None)

        # Iterative checking on regex patterns to search based on users command input on what
        # they're trying to do. Specific verbs are being checked in search and extracting
        # relevant actions
        moveMatch = movePattern.search(userInput)
        takeMatch = takePattern.search(userInput)
        openMatch = openPattern.search(userInput)
        useMatch = usePattern.search(userInput)
        useKeyMatch = useKeyPattern.search(userInput)
        checkToolsMatch = checkToolsPattern.search(userInput)
        fixPipeMatch = fixPipePattern.search(userInput)
        lookMatch = lookPattern.search(userInput)

        # Process parsed input against the regex matches and executing the actions for the player
        # Returning structured tuples based on required commands and additional ones added for some more
        # player flexibility from their input
        if moveMatch:
            return ("GO", moveMatch.group(1), None)
        if takeMatch:
            return ("TAKE", takeMatch.group(1), None)
        if openMatch:
            return ("OPEN", openMatch.group(1), None)
        if useMatch:
            # Checking if second object (obj2) was specified in user input
            # on use verb
            if useMatch.group(2):
                obj2 = useMatch.group(2)
            else:
                obj2 = None
            return ("USE", useMatch.group(1), obj2)
        if useKeyMatch:
            return ("USE_KEY", None, None)
        if checkToolsMatch:
            return ("CHECK_TOOLS", None, None)
        if fixPipeMatch:
            return ("FIX_PIPE", None, None)
        if lookMatch:
            # Checking if player provided an object with look verb
            if lookMatch.group(1):
                obj1 = lookMatch.group(1)
            else:
                obj1 = None
            return ("LOOK", obj1, None)

        # Handling different edge cases based on user's input prompt
        return (None, None, None)
    
    # Displaying the game introduction, an objective for the player, and some instructions for going about the game
    print("You've been woken up to a loud intercom noise requesting you to report to the engine room to a fix a pipe.")
    print("Your objective is to find and collect the necessary tools to fix a leaking pipe in the engine room on an old Navy ship.")
    print("Explore different rooms, take items, and use them where needed. Have fun shipmate!")
    print("Actionable commands: 'go, 'take', 'use', 'look', 'quit' or 'exit'.")
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
        # used for troubleshooting in correlation to parseInput function
        if currentRoom is None:
            print(f"Room '{player.currentLocation}' not found.")
            sys.exit(1)

        print(f"\nYou are in {currentRoom.name}.")
        print(f"{currentRoom.description}")
        print(f"You see a door: {', '.join(currentRoom.directions.keys())}")

        # Show and display descriptions of available objects/itmes in the room
        if currentRoom.items:
            print("You see some stuff in the room:")
            for itemName, item in currentRoom.items.items():
                print(f"- {itemName}: {item.description}")

        # Getting user input and parsing to lower case as well, matching verbs below in conditional checks
        userInput = input("\n> ").strip().lower()
        verb, obj1, obj2 = parseInput(userInput)

        # Help separation after user input for cleaner reading
        print("-------------------------------------------------------------------------------\n")

        # Return prompt if player decides to quit/exit game
        if userInput in ["quit", "exit"]:
            print("Exiting game. Thanks for playing!")
            break

        # Checking verb go for user input to move to another room and if there
        # is a door thats locked
        elif verb == "GO":
            if currentRoom.isLocked():
                print("The door is locked. You need a key to proceed.")
            else:
                player.move(obj1, ship)

        # Checking the available tools you have in your toolbag/inventory and displaying them
        elif verb == "CHECK_TOOLS":
            # Displaying items in your inventory
            if player.inventory:
                print("\nYou currently have in your inventory:")
                for item in player.inventory:
                    print(f"- {item.name}")
            else:
                print("\nYour inventory is empty.")

        # Check for taking an item within a room, then will let player take that item and store
        # in inventory
        elif verb == "TAKE":
            player.takeItem(obj1, ship)

        # Handling another case when player trys to look or check inventory, tools or toolbag
        # returns current players inventory list
        elif verb in ["CHECK", "LOOK"] and obj1 in ["inventory", "tools", "toolbag"]:
            player.checkInventory()

        # Handling the case where player attempts to use they key to the engine room after they pick it up
        elif verb == "USE" and obj1 == "key" or obj1 in["key"]:
            if player.currentLocation == "machinery_room":

                # Going through the inventory to check if player has the key stored
                key = None
                for item in player.inventory:
                    if item.name == "key":
                        key = item
                        break

                # Checking if the player has they key currently and will be able to unlock the engine 
                # room if its unlocked
                if key:
                    if "engine_room" in ship.rooms and ship.rooms["engine_room"].isLocked():
                        ship.rooms["engine_room"].unlock()
                        print("You used the key to unlock the door to the engine room.")
                    else:
                        print("The engine room is already unlocked.")
                else:
                    print("You don't have the key.")
            else:
                print("You can't use the key here.")


        # Handling the case if they player tries to fix the pipe in the engine room but only if
        # they have necessary tools to do so. Then seeing if they like to play again if they do complete
        # the task
        elif verb == "USE" or verb == "FIX_PIPE" and obj1 in ["tools", "toolbag", "fix leaking pipe"]:
            # Checking if the player is in the engine room and with required tools to fix the leak
            if player.currentLocation == "engine_room":
                has_wrench = False
                has_pipe_tape = False

                # Iterating through the players current inventory to check for required tools to fix the
                # leaking pipe
                for item in player.inventory:
                    if item.name == "wrench":
                        has_wrench = True
                    elif item.name == "pipe_tape":
                        has_pipe_tape = True

                # Ensure both required tools are available before proceeding
                if has_wrench and has_pipe_tape:
                    print("\nYou use your tools to fix the leaking pipe in the engine room!")
                    print("The Captain awards you for literally doing your job.")
                    print("Congratulations, you've beat the game!\n")

                    # Prompting the player the choice to play again or not
                    playAgain = input("Would you like to play again? (yes/no): ").strip().lower()
                    if playAgain == "yes":
                        ship = Ship(filePath)
                        player = Player("north", "crew_quarters")
                    else:
                        print("Thanks for playing!")
                        break
                else:
                    print("\nYou don't have all the necessary tools to fix the leak. Keep exploring the ship, you'll figure it out.")
            else:
                print("\nYou can't fix anything here.")


        # Handling the standard use case for use verb when player attempts to use item/object
        elif verb == "USE":
            # Checking for specified object within the users input
            if obj1:
                if obj2:
                    player.useItem(obj1, obj2, ship)
                else:
                    player.useItem(obj1, None, ship)
            else:
                print("Use what?")

        # Handle look command with examining your surroudings and providing description of
        # players location with if check on possible doors leading to other rooms in different directions
        elif verb == "LOOK":
            # Providing player to be able to look around and see where they are
            if obj1 in [None, "around"]:
                player.checkLocation()

                # Letting them know if they can enter another room or not in current direction
                nextRoomName = currentRoom.getNextRoom(player.direction)
                if nextRoomName:
                    print(f"You see a door leading somewhere.")
                else:
                    print(f"You see just another boring wall in the ship.")
                # Listing available door directions for the player by joining keys from
                # directions dictionary into a displayed string
                print(f"You see a door: {', '.join(currentRoom.directions.keys())}")
            else:
                player.look(obj1, ship)
        
        # Handling the open command to interact with doors in the game world
        elif verb == "OPEN":
            # If user input target object is a door and it's locked, notify them
            # of either locked or if its already been opened/unlocked
            if obj1 in ship.rooms:
                room = ship.rooms[obj1].locked

                # Letting the player know if a room is locked or not and providing some helpful info
                if room.isLocked():
                    print(f"The door to {obj1} is locked. You need a key to open it. Try using use key.")
                else:
                    print(f"You opened the door to {obj1}. You can now go there.")

            
            # Allowing the player to open (view) the inside of their inventory/toolbag
            # and will display all current items stored
            elif obj1 in player.inventory:
                if obj1 == "toolbag":
                    print(f"You open your {obj1} and check its contents:")
                    player.checkInventory()
                else:
                    print(f"You can't open this {obj1}.")
            
            else:
                print(f"There's nothing to open with that name.")

        # Invalid input prompt, to keep them aware if forgotten of verbs
        else:
            print("Invalid command. Try: 'go, 'take', 'use', 'look', 'quit' or 'exit'.")