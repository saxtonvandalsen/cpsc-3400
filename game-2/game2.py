# CPSC 3400-02 Languages & Computation
# Game 2
# Saxton Van Dalsen
# 2//2025

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

class Player:
    def __init__(self, board, troops, bombs):
        self.board = board
        self.score = 0
        self.strength = 1
        self.turn = 0

    def __str__(self):
        width = self.board.width
        size = (width * CELL_WIDTH) + 1
        string = "TURN: {0}\tSTRENGTH: {1}\tSCORE: ".format(self.turn, self.strength)
        if self.score > 0:
            string += ANSI_GREEN + str(self.score) + ANSI_END
        elif self.score == 0:
            string += str(self.score)
        else:
            string += ANSI_RED + str(self.score) + ANSI_END
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

if __name__ == "__main__":
    seed = 0
    if len(sys.argv) > 1:
        seed = sum([ord(c) for c in sys.argv[1]])
    random.seed(seed)
    aliens = []
    board = Board(HEIGHT, WIDTH)
    player = Player(board, 3, 3)
    userin = ""
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
        userin = input("Choose a coordinate to attack (x,y): ")
        search = re.search(r"\(?(-?\d+)[, ]+(-?\d+)\)?", userin)
        (userx, usery) = search.groups() if search != None else (None, None)
        if userx == None or usery == None:
            if userin.upper() == "QUIT" or userin.upper() == "EXIT":
                continue
            elif userin.upper() == "TREES":
                printTrees(aliens)
                continue
            print("Invalid coordinates. Lose your turn.")
        else:
            userx = int(userx)
            usery = int(usery)
            score = board.squish((userx, usery), player.strength)
            if score > 0:
                player.strength += 1 if player.strength < STRENGTH else 0
            elif score <= 0:
                player.strength -= 1 if player.strength > 1 else 0
            player.score += score
        board.doTimestep()
        player.doTimestep()
        if board.isEmpty():
            print("You win!")
            exit(0)
