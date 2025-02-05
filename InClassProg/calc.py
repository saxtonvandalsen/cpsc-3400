memory = 0

def add(x, y):
    global memory
    result = x + y
    memory = result
    return result

def sub(x, y):
    global memory
    result = x - y
    memory = result
    return result

def mul(x, y):
    global memory
    result = x * y
    memory = result
    return result

def div(x, y):
    global memory
    result = x / y
    memory = result
    return result

def mod(x, y):
    global memory
    result = x % y
    memory = result
    return result

if __name__ == "__main__":
    userin = input("Provide Operation: ").upper()
    while(userin != "STOP" and userin != "QUIT" and userin != "EXIT"):
        expression = userin.split()
        operator = expression[0]
        numIns = len(expression)
        operand1 = float(expression[1])
        operand2 = float(expression[2])
        result = 0
        if operator == '+':
            result = add(operand1, operand2)
        elif operator == '-':
            result = sub(operand1, operand2)
        elif operator == '*':
            result = mul(operand1, operand2)
        elif operator == '/':
            result = div(operand1, operand2)
        elif operator == '%':
            result = mod(operand1, operand2)
        else:
            result = "ERROR"
            print("Invalid Operator")

        if result != "ERROR":
            print("{0} {1} {2} = {3}".format(operand1, operator, operand2, result))
        userin = input("Provide Operation: ").upper()

