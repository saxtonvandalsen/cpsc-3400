# CPSC 3400-02 Game 1 - 20 Questions
# Saxton Van Dalsen
# 2/11/2025

import os

# Since we need to pass in a dialogue binary tree for the computer to
# follow while playing, I need to construct a class representing nodes
# in a linked list to handle the logic of the game and being to move down
# the tree
class Node:
    # Constructor used to create a node in the tree based on the given
    # format of the identifying nodes in the .tree file
    def __init__(self, node_id, node_type, data):
        self.node_id = node_id # Identify tree node id
        self.node_type = node_type # Identify either question or answer
        self.data = data # data based on that text
        self.left = None # Using left for a yes answer
        self.right = None # Using right for a no answer

# Defining class to keep all my game logic organized.
# Easier to manage, update, and organize while testing
class TwentyQuestionsGame:
    # Setting up game structure with constructor. Either load file on command 
    # line or start empty. To build upon either way.
    def __init__(self, tree_file=None):
        
        # Initializing root node of tree to empty
        self.root_node = None

        # Checking for a file provided and if it exists based on the name
        if tree_file != None and os.path.exists(tree_file):
            # Load the tree from the file if it exists
            self.root_node = self.load_tree_file(tree_file)
        else:
            # Start with initial question then if the file was
            # not passed in command line
            self.root_node = Node(0, 'question', "Is this a test?")

    # Load the .tree file and pass it on to create the questions binary tree
    # Needed to make sure each question and answer in the tree is mapping accordingly
    # even if the nodes within the given file are out of out of order
    def load_tree_file(self, tree_file):
        # Opening the file in read mode by r
        file = open(tree_file, 'r')

        # Using dictionary to map node IDs as keys to their specific node values
        # Efficient so I can link parent and child nodes for different orders 
        # based on tree file input like out-of-order structure
        nodes = {}

        # Reading all nodes and storing them in dictionary nodes
        for line in file:
            # Using strip throughout code for removing spaces and handling new lines from data
            # then splitting into sections based on lines of nodes descriptions formatting
            line = line.strip()
            sections = line.split(":")

            # Mapping each line of the .tree file in correct structured format
            node_id = int(sections[0])
            node_type = sections[1]
            data = sections[2]

            # Ternary conditional checks to see if empty or not
            # then assigns accordingly for parent, left, and right
            parent_id = int(sections[3]) if sections[3] else None
            left_id = int(sections[4]) if sections[4] else None
            right_id = int(sections[5]) if sections[5] else None

            # Creating the node object and storing node IDs for
            # linking later
            nodes[node_id] = Node(node_id, node_type, data)
            nodes[node_id].parent_id = parent_id
            nodes[node_id].left_id = left_id
            nodes[node_id].right_id = right_id
        
        # Closing the file here after being loaded and reading all lines
        file.close()

        # Linking child nodes based on their node IDs
        for node in nodes.values():
            if node.left_id != None:
                node.left = nodes[node.left_id]
            if node.right_id != None:
                node.right = nodes[node.right_id]

        # Iterating to search for and return the root node
        for node in nodes.values():
            if node.parent_id is None:
                return node

    # Needed this handle asking questions and traversing through the tree.
    # It's needed for triggering learning to add new nodes of questions and answers
    # Also part of handling the question coutner limit
    def handle_question(self, node, question_counter=0):

        # Handling the 20 questions limit by ending the questioning if
        # 20 questions have been reached then prompting user to play again
        if question_counter >= 20:
            print("The maximum number of 20 questions has been reached.")
            self.prompt_play_again()
            return

        # Checking if we are at an answer node or not
        if node.node_type == 'answer':
            # Asking if the guess was correct
            response = input(f"Is it {node.data}? (y/n): ").strip().lower()
            # If correct print the winning message and if not
            # we need to trigger to learn and update the tree for this point
            if response == 'y':
                print("I win! Better luck next time.")
            else:
                self.update_knowledge(node)
            # Prompt to ask if they want to play again
            self.prompt_play_again()
        else:
            # Asking current question
            response = input(f"{node.data} (y/n): ").strip().lower()
            # Check if answer is yes
            if response == 'y':
                # Program would fail after adding first question when running
                # command line with no tree. So I added aditional handling to check
                # if left node is empty, if so it moves to learning/updating knowledge
                if node.left != None:
                    self.handle_question(node.left)
                else:
                    # Update knowledge and prompt play to play again
                    self.update_knowledge(node)
                    self.prompt_play_again()
            else:
                # Same with this part added this check for the right node as well
                # if the tree or left or right nodes are emmpty.
                if node.right != None:
                    self.handle_question(node.right)
                else:
                    # Update knowledge and prompt play to play again for either case
                    self.update_knowledge(node)
                    self.prompt_play_again()
            
    # Helping the aspect of the game to learn and build upon the tree when 
    # it makes a wrong final guess. It will prompt and ask user for a similar style 
    # question while adding an answer and relation to it. This helps expansion of the tree
    def update_knowledge(self, node):
        print("You've stumped me! Help me learn how to beat you next time.")
        print(f"I really thought it was going to be a(n) {node.data}.")

        # Asking for a new question to help learn for an new answer based on the
        # incorrect guess
        new_question = input(f"Provide me a new yes/no question to help me learn: ")

        # Getting the correct answer for what the player was thinking
        correct_answer = input("What were you actually thinking of?: ").strip()

        # Based on previous guess, asking if it would be yes or no for the new question
        response = input(f"Would a(n) {node.data} be associate with a yes or no answer to your new question ? (y/n)").strip().lower()

        # Based on response from user, this adds together the new answer with old guess
        # in the tree based on whether answer as yes or no
        if response == 'y':
            # Handling for the old wrong guess to be yes now
            # and correct answer to be set to no
            node.left = Node(node.node_id + 1, 'answer', node.data)
            node.right = Node(node.node_id + 2, 'answer', correct_answer)
        else:
            # Handling for the other situation for the wrong guess to be now
            # set to no and correct one to be a yes now
            node.right = Node(node.node_id + 1, 'answer', node.data)
            node.left = Node(node.node_id + 2, 'answer', correct_answer)

        # Updating node to be the new question instead of answer
        node.data = new_question
        node.node_type = 'question'

    # Sets up and starts the game for the user based on if no .tree file was
    # given in command line and it will check for this to determine how the game
    # plays from there
    def play_game(self):
        print("Starting the 20 Questions game!")

        # If a .tree file was given in command line and loaded correctly then
        # it will move out and start with root node question
        if self.root_node and self.root_node.data != "Is this a test?":
            print("Thanks for passing me my database!")
        # If not then start by prompting the user for the first question
        else:
            first_question = input("Provide first question: ").strip()
            self.root_node = Node(0, 'question', first_question)

        # To initialize the question counter when starting the game
        self.handle_question(self.root_node, question_counter=0)

    # The game kept playing on a loop as I forgot to add a function or
    # condition to check and ask if the user would like to play again or
    # not. Created to keep it organized for calling it elsewhere
    def prompt_play_again(self):
        play_again = input("Play again? (y/n): ").strip().lower()
        
        # If user wants to play again then it will start back at the root
        # of tree, if not then it exits the program
        if play_again == 'y':
            self.handle_question(self.root_node)
        else:
            print("Well I had fun! Lets play again sometime.")
            exit()

# Game starts here and utilizing sys to check if a .tree file
# was passed in command line or not. If it was we load quesitons,
# if not we start with a starting question
if __name__ == "__main__":
    import sys

    # Checking if the .tree file was passed into command line
    # to determine pre built tree or an empty one
    if len(sys.argv) > 1:
        tree_file = sys.argv[1]
    else:
        tree_file = None

    # Starting the game based with passed in tree based on if it
    # added in command line or left empty
    game = TwentyQuestionsGame(tree_file)
    game.play_game()