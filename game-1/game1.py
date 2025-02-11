# CPSC 3400-02 Game 1 - 20 Questions
# Saxton Van Dalsen

import os

# Welcome to my take on the 20 questions game
print("Starting the 20 Questions game!")

# Since we need to pass in a dialogue binary tree for the computer to
# follow while playing, I need to construct a class representing nodes
# in a linked list to handle the logic of the game and being to move down
# the tree
class Node:
    
    # Constructor used to create a node, store the data based on input,
    # and left represents a yes answer while right represents a no answer
    # Setting each to None to allow creation of a Node
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

# Defining class to keep all my game logic organized.
# Easier to manage, update, and organize while testing
class TwentyQuestionsGame:
    
    # Setting up game structure with constructor. Either load file on CLI or 
    # start empty. To build upon either way.
    def __init__(self, tree_file=None):
        self.root_node = None # Initializing root node of tree to empty

        # Checking for a file provided and if it exists based on the name
        if tree_file != None and os.path.exists(tree_file):
            # Load the tree from the file if it exists
            self.root_node = self.load_tree(tree_file)
        else:
            # Start with initial question then if the file was not in CLI
            self.root_node = Node("Is this a test?")

    #

        

# Game starts here and utilizing sys to check if a .tree file
# was passed in command line or not. If it was we load quesitons,
# if not we start with a starting question
if __name__ == "__main__":
    import sys

    # Checking if the .tree file was passed into CLI
    if len(sys.argv) > 1:
        tree_file = sys.argv[1]
    else:

        # If no file in CLI then start empty
        tree_file = None
    game = TwentyQuestionsGame(tree_file)