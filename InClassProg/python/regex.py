# Given code from CPSC-3400-02 for learning, practicing, & testing regular expressions in Python

import re

def checkPatterns(lines):
    pattern = re.compile(r"^([a-zA-Z]+) ([a-zA-Z]+) ([a-zA-Z]+)[\.\!\?]")
    phone = re.compile(r"\(?(\d\d\d)\)? ?(\d\d\d)-(\d\d\d\d)|(\d{3})\-(\d{3})\-(\d{4})")
    email = re.compile(r"(\S+)@(\S+)\.(gov|edu|com|org)$")
    for line in lines:
        sentence = re.search(pattern, line)
        number = re.search(phone, line)
        address = re.search(email, line)
        for check in [sentence, number, address]:
            if check != None:
                print(check)
                print('-')
                print(check.groups())
                print(check.group(1))
                print(check.group(2))
                print(check.group(3))

if __name__ == "__main__":
    infile = "patterns.txt"
    infile = open(infile)
    lines = infile.readlines()
    checkPatterns(lines)
    infile.close()
