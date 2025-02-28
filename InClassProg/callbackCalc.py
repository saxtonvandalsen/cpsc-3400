# Callback calculator
# 2/26/2025

memory = 0

# set y to default value for unary operations case 
def calc(op, x, y=None):
    global memory # not recreating, referring to global memory variable
    result = 0
    if x == None and y != None:
        x = memory

    if y != None:
        result = op(x, y)
    else:
        result = op(x) # unary operation handling
    memory = result
    return result

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def multi(x, y):
    return x * y

def div(x, y):
    if y == 0:
        print("Cannot divide by zero")
        return 0
    return x / y

def printResult(result, op, x, y=None):
    if result == "ERROR":
        return
    elif y != None:
        # curly brace placeholders for variables
        print("{0} {1} {2} = {3}".format(x, op, y, result))
    else:
        # f for formatted string
        print(f"{x} {op} {y} = {result}")


if __name__ == "__main__":
    # Example user input: + 1 2
    userin = input("Provide expression: ").upper()
    while(userin != "STOP" and userin != "EXIT" and userin != "QUIT"):
        expression = userin.split() # list of strings
        numInputs = len(expression)
        if numInputs == 0:
            print("Invalid number of terms.")
            userin = input("Provide expression: ").upper()
            continue
        op = expression[0]
        x = None
        y = None
        if numInputs == 1:
            x = memory
        elif numInputs == 2:
            x = memory # referencing memory
            y = float(expression[1]) # translated to float
        elif numInputs == 3:
            x = float(expression[1])
            y = float(expression[2])
        
        if op == '+':
            result = calc(add, x, y)
        elif op == '-':
            result = calc(sub, x, y)
        elif op == '*':
            result = calc(multi, x, y)
        elif op == '/':
            result = calc(div, x, y)
        else:
            result = ("ERROR")
            print("Invalid operation.")
        printResult(result, op, x, y)
        userin = input("Provide expression: ").upper()
