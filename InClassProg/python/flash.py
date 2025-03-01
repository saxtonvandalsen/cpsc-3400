import random

# Class definition of a linked list representing flashcards
class Node:
    def __init__(self, answer, definition, nextNode):
        self.answer = answer
        self.definition = definition
        self.next = nextNode

    def __str__(self):
        return "{0}: {1}".format(self.definition, self.answer)


if __name__ == "__main__":
    file = open("flashcards.txt")
    flashcards = file.readlines()
    numTests = len(flashcards)
    cardList = []
    print("Old Order")

    # Loop flashcards, created Node objects with answers and definitions then add to list
    for i in range(numTests):
        card = flashcards[i].split(':')
        answer = card[0]
        definition = card[-1].strip()
        card = Node(answer, definition, None)
        print(card)
        cardList.append(card)

    # Shuffle the list of flashcards in random order to achieve unique output each time
    random.shuffle(cardList)

    # Link each Node in the list to the next node
    for i in range(len(cardList)):
        node = cardList[i]
        if i < len(cardList) - 1:
            node.next = cardList[i + 1]

    # Going through the flashcard list and testing based on randomness
    print("New Order")
    head = cardList[0]
    curr = head
    while curr != None:
        print(curr.definition)
        userin = input("Answer: ").lower()
        if userin == curr.answer.lower():
            print("Correct! Getting next card.")
        else:
            print("Incorrect. Consider dropping out.")
        curr = curr.next

        if curr is None:
            print("You answered all flashcards correctly!")
            break
        else:
            print("Getting next card.")