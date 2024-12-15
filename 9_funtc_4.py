from functools import reduce

# Sum up all the numbers in a list
result = reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
print(result)  # Output: 15
