# CPSC 3400-02 Languages & Computation
# Game 2
# Saxton Van Dalsen
# 2/26/2025

import random
import re
import sys

# 100MB of characters
NUM_BYTES = (1024 ** 2) * 100
HEIGHT = 8
WIDTH = 8
STRENGTH = 9
CELL_WIDTH = 11

ANSI_CYAN = "\033[96m"
ANSI_END = "\033[0m"
ANSI_GREEN = "\033[92m"
ANSI_RED = "\033[91m"

class Alien:
    def __init__(self, board, coords, strength):
        self.board = board
        self.coords = coords
        self.strength = strength
        self.board.addAlien(self)
        self.x = coords[0]
        self.y = coords[1]
        self.squished = False
        self.value = bytearray(NUM_BYTES)
        self.children = []

    def __str__(self):
        return ANSI_RED + str(self.strength) + ANSI_END

    def doDeath(self):
        self.squished = True
        self.board.clearCell(self.coords)

    def doPop(self, strength=1):
        self.strength -= strength
        if self.strength < 1:
            self.doDeath()

    def doGrow(self):
        chance = random.randint(0, 9)
        if self.strength < STRENGTH and chance > 7:
            self.strength += 1

    def doTimestep(self):
        self.doTravel()
        self.doSpawn()
        self.doGrow()

    def doTravel(self):
        distx = random.randint(-1, 1)
        disty = random.randint(-1, 1)
        newx = self.x + distx
        newy = self.y + disty
        if self.inRange((newx, newy)):
            self.board.moveAlien(self.coords, (newx, newy))
            self.coords = (newx, newy)
    
    def doSpawn(self):
        emptySpace = self.findEmptySpace()
        neighbor = self.getNeighbor()
        chance = random.randint(0, 9)
        if neighbor != None and emptySpace != None and chance > 6:
            child = Alien(self.board, emptySpace, max(1, self.strength - 1))
            self.children.append(child)

    def findEmptySpace(self):
        adjacent = [(self.x + 1, self.y + 1), (self.x + 1, self.y), (self.x + 1, self.y - 1),
                    (self.x, self.y + 1), (self.x, self.y - 1), (self.x - 1, self.y - 1),
                    (self.x - 1, self.y), (self.x - 1, self.y + 1)]
        random.shuffle(adjacent)
        for coords in adjacent:
            if self.inRange(coords) and self.board.isEmpty(coords):
               return coords
        return None

    def getNeighbor(self):
        adjacent = [(self.x + 1, self.y + 1), (self.x + 1, self.y), (self.x + 1, self.y - 1),
                    (self.x, self.y + 1), (self.x, self.y - 1), (self.x - 1, self.y - 1),
                    (self.x - 1, self.y), (self.x - 1, self.y + 1)]
        neighbors = []
        for coords in adjacent:
            if self.inRange(coords):
                neighbor = self.board.getAlien(coords)
                if neighbor != None:
                    neighbors.append(neighbor)
        if len(neighbors) == 0:
            return None
        neighbor = neighbors[random.randint(0, len(neighbors) - 1)]
        return neighbor

    def inRange(self, coords):
        if coords[0] > 0 and coords[0] < self.board.width and coords[1] > 0 and coords[1] < self.board.height:
            return True
        return False

class Board:
    def __init__(self, height, width):
        self.board = [[None for j in range(width)] for i in range(height)]
        self.height = height
        self.width = width

    def __str__(self):
        string = ""
        for i in range(self.width):
            cells1 = []
            cells2 = []
            for j in range(self.height):
                alien = self.getAlien((i, j))
                cell1 = "|    -     ".format(alien)
                if alien != None and alien.squished == False:
                    cell1 = "|    {0}     ".format(alien)
                cell2 = "| ({0:02d},{1:02d})  ".format(i, j)
                if j == (self.height - 1):
                    cell1 += '|'
                    cell2 += '|'
                cells1.append(cell1)
                cells2.append(cell2)
            string += '-' * ((len(cells1) * CELL_WIDTH) + 1)
            string += '\n'
            for cell in cells1:
                string += cell
            string += '\n'
            for cell in cells2:
                string += cell
            string += '\n'
            if i == (self.width - 1):
                string += '-' * ((len(cells1) * CELL_WIDTH) + 1)
                string += '\n'
        return string

    def addAlien(self, alien):
        coords = alien.coords
        self.board[coords[0]][coords[1]] = alien

    def clearCell(self, coords):
        self.board[coords[0]][coords[1]] = None

    def doTimestep(self):
        for i in range(self.width):
            for j in range(self.height):
                alien = self.getAlien((i, j))
                if alien != None and alien.squished == False:
                    alien.doTimestep()

    def getAlien(self, coords):
        return self.board[coords[0]][coords[1]]

    def isEmpty(self, coords=None):
        if coords == None:
            flag = 0
            for i in range(self.width):
                for j in range(self.height):
                    if self.getAlien((i, j)) != None:
                        flag = 1
                        return False
            return True
        if self.getAlien(coords) != None:
            return False
        return True

    def moveAlien(self, oldCoords, newCoords):
        if not self.isEmpty(oldCoords) and self.isEmpty(newCoords):
            alien = self.getAlien(oldCoords)
            self.clearCell(oldCoords)
            self.board[newCoords[0]][newCoords[1]] = alien

    def squish(self, coords, strength=1):
        if coords[0] < 0 or coords[0] >= self.width:
            print("Invalid coordinates. Lose your turn.")
            return -1
        elif coords[1] < 0 or coords[1] >= self.height:
            print("Invalid coordinates. Lose your turn.")
            return -1
        elif self.isEmpty(coords):
            print("Cell is empty. Lose your turn.")
            return -1
        else:
            alien = self.getAlien(coords)
            if alien != None:
                score = strength if alien.strength > strength else alien.strength
                alien.doPop(strength)
                return score
        return -1

# Realized after playing the game and reading through the source code that the
# troops and bombs parameters are never initialized or used. Incorporating features for them
class Player:
    def __init__(self, board, troops, bombs):
        self.board = board
        self.score = 0
        self.strength = 1
        self.turn = 0
        # Need to track troops and bombs
        self.troops = troops
        self.bombs = bombs

    def __str__(self):
        width = self.board.width
        size = (width * CELL_WIDTH) + 1
        # Added in the display of current troops and bombs below the grid cells
        # and adjusted formatting to make simpler
        string = "TURN: {0}\tSTRENGTH: {1}\tSCORE: {2}\tTROOPS: {3}\tBOMBS: {4}".format(
            self.turn, self.strength, self.score, self.troops, self.bombs)
        return "{0:^{1}}".format(string, size)
        
    def doTimestep(self):
        self.turn += 1

    def printTree(alien, depth=0):
        tree = "{0}({1}):".format(str(alien), depth)
        if len(alien.children) == 0:
            return tree
        else:
            for child in alien.children:
                tree += printTree(child, depth + 1)
        return tree

    def printTrees(aliens):
        for alien in aliens:
            tree = printTree(alien)
            print(tree)

    # I was thinking to help balance out the game I would incorporate a feature to use
    # troops where you can attack multiple times within a turn if you have multiple troops available
    def useTroops(self):
        if self.troops > 0:
            print(f"You have {self.troops} troops. You're given the option to attack multiple coordinate.")
            attacks = []

            # Providing the player option to pick different coordinates for multiple attacks
            for count in range(self.troops + 1):
                userin = input("Enter coordinate (x,y) or press Enter to skip: ")

                # Still providing option if they would like to exit or quit at any time
                if userin == "QUIT" or userin == "EXIT":
                    exit(0)

                # Using user input for coordinates attack
                search = re.search(r"\(?(-?\d+)[, ]+(-?\d+)\)?", userin)
                if search:
                    userx, usery = map(int, search.groups())
                    attacks.append((userx, usery))

            self.troops -= 1
            return attacks
        
        return []

    # Adding a bombing feature as well to help stregthen attacks on aliens (to make the game a bit more fair)
    # as it seems in the starter code the aliens have the advantage based on only being able to attack once
    # each turn for the player. Player earns 1 bomb each turn.
    # If player has atleast 2 bombs in inventory then they'll be asked if they'd like to bomb on the turn,
    # where a bomb deals twice the damage of their current strength
    def useBomb(self, coords):
        if self.bombs >= 2:
            self.bombs -= 1
            print(f"A bomb has been dropped on {coords}!")
            # Return a bomb attack that will deal double the damage of strength
            return self.board.squish(coords, self.strength * 2)
        # Return a normal attack if no bomb was used
        return self.board.squish(coords, self.strength)


if __name__ == "__main__":
    seed = 0
    if len(sys.argv) > 1:
        seed = sum([ord(c) for c in sys.argv[1]])
    random.seed(seed)
    aliens = [] # Where the root aliens are being held at
    board = Board(HEIGHT, WIDTH)
    player = Player(board, 3, 3)
    userin = ""

    # Initially I tried to implement mark and sweep garbage collection inside Board class
    # After testing and reviewing the handout, I realized that the root aliens are managed in main.
    # Because of this I instead move to troubleshooting within main to handle squished aliens being
    # properly removed while maintaining the references to their children
    def markAndSweep(aliens):
        # New list to hold children and non-squished aliens
        new_aliens = []
        
        for alien in aliens:
            if alien.squished:
                # Handling if alien is squished then move its children
                # to new aliens list
                for child in alien.children:
                    if not child.squished:
                        new_aliens.append(child)
            else:
                # Used to store non-squished alien children
                remaining_children = []
                # Checking for each child of each alien, if not squished
                # then adding it to the new list
                for child in alien.children:
                    if not child.squished:
                        remaining_children.append(child)
                # Then updating to remove squished children and maintaining
                # current aline since it wasn't squished
                alien.children = remaining_children
                new_aliens.append(alien)

        # Updating original aliens root list with updated one
        # Clearing elements from original list first then adding in
        # updated aliens back to that list
        aliens.clear()
        for alien in new_aliens:
            aliens.append(alien)
        
    while(userin.upper() != "QUIT" and userin.upper() != "EXIT"):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        s = random.randint(1, STRENGTH)
        if player.turn == 0:
            s = 5
        if board.isEmpty((x, y)):
            alien = Alien(board, (x, y), s)
            aliens.append(alien)
        print(board)
        print(player)

        # Handling and providing user option for multiple troop attacks
        attack_coords = player.useTroops()  # Get extra attack coordinates
        
        # If minimum troops aren't available, single attack
        if not attack_coords:
            userin = input("Choose a coordinate to attack (x,y): ")
            
            # Handle exit conditions and tree output option
            if userin.upper() == "QUIT" or userin.upper() == "EXIT":
                break
            elif userin.upper() == "TREES":
                printTrees(aliens)
                continue # Continue after trees of aliens are displayed

            # User input for coordinates attack
            search = re.search(r"\(?(-?\d+)[, ]+(-?\d+)\)?", userin)
            if search:
                userx, usery = map(int, search.groups())
                attack_coords.append((userx, usery))
            else:
                print("Invalid coordinates. Lose your turn.")

                # Updating player score if they skip/press enter or invalid coords
                # and maintaining minimum strength
                player.score -= 1
                player.strength = max(1, player.strength - 1)

                # Losing condition to check if player gets below or equal to -15 score
                if player.score <= -15:
                    print("You're score was too negative. You lose.")
                    exit(0)

                continue  # Skipping turn if invalid input

        # Asking the player if they want to use bombs if they have atleast 2
        if player.bombs >= 2:
            bomb_choice = input("Do you want to use a bomb on this turn? (yes/no): ").strip().lower()
        else:
            bomb_choice = "no"

        # Handling attack style, coordinates and strength based on players action
        for coords in attack_coords:
            if board.isEmpty(coords):
                print("Cell is empty. Lose your turn.")
                continue

            # Checking for bomb attack or regular attack
            if bomb_choice == "yes":
                score = player.useBomb(coords)
            else:
                score = board.squish(coords, player.strength)

            # Adjusting player strength based on attack results
            if score > 0:
                player.strength += 1 if player.strength < STRENGTH else 0
            elif score <= 0:
                player.strength -= 1 if player.strength > 1 else 0
            player.score += score
        

        board.doTimestep()

        # I'm calling my mark and sweep after board timestep function because I
        # need the changes to the game state to take affect before removing references
        # to squished aliens, to fix the aliens trees
        markAndSweep(aliens)

        # Adding losing state. First counting number of cells with aliens in them
        alien_count = 0
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if board.getAlien([i, j]) is not None:
                    alien_count += 1
        
        # Losing condition if the aliens take over 80% of the grid
        if alien_count > (WIDTH * HEIGHT * 0.8):
            print("Aliens win. You lose. Be better next time.")
            exit(0)

        player.bombs += 1 # Add 1 bomb on each turn
        player.troops += 1 # Add 1 troop on each turn
        player.doTimestep()
        if board.isEmpty():
            print("You win!")
            exit(0)
