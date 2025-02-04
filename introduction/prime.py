# Return boolean value if passed in number is Prime or not
def isPrime(num):
    if num < 4:
        return True
    # range(stop) - return list [0, 1, .., stop - 1]
    # range(start, stop) - return [start, start + 1, .., stop - 1]
    # range(start, stop, step) - step is for incrementing values
    for i in range(2, num, 1):
        if num & i == 0:
            return False
    return True

num = int(input("Provide a Number: "))
result = isPrime(num)
print(result)