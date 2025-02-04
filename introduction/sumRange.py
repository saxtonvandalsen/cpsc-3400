def sumRange(nums):
    acc = 0
    for num in nums:
        acc += num
    return acc

def sumEvenRange(nums):
    acc = 0
    for num in nums:
        if num % 2 == 0:
            acc += num
        return acc

def sumOddRange(nums):
    acc = 0
    for num in nums:
        if num % 2 == 1:
            acc += num
        return acc


num = range(int(input("Provide ending number: ")) + 1)
print(sumRange(num))
print(sumEvenRange(num))
print(sumOddRange(num))