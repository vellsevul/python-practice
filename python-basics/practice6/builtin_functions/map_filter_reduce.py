from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map
squares = list(map(lambda x: x*x, numbers))
print(squares)

# filter
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)

# reduce
total = reduce(lambda a, b: a + b, numbers)
print(total)