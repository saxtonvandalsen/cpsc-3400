import random

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
    for i in range(numTests):
        card = flashcards[i].split(':')
        answer = card[0]
        definition = card[-1].strip()
        card = Node(answer, definition, None)
        print(card)
        cardList.append(card)

    random.shuffle(cardList)
    for i in range(len(cardList)):
        node = cardList[i]
        if i < len(cardList) - 1:
            node.next = cardList[i + 1]

    print("New Order")
    head = cardList[0]
    curr = head
    while curr != None:
        print(curr.definition)
        userin = input("Answer: ")
        if userin == curr.answer:
            print("Correct! Getting next card.")
        else:
            print("Incorrect. Consider dropping out.")
        curr = curr.next
