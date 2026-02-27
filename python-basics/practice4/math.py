# math.py

import math
import random

# 1️⃣ Built-in functions
print("---- Built-in Functions ----")
print(min(3, 7, 2))
print(max(3, 7, 2))
print(abs(-10))
print(round(3.6))
print(pow(2, 3))

# 2️⃣ math module basics
print("\n---- math module ----")
print(math.sqrt(16))
print(math.ceil(3.2))
print(math.floor(3.8))

# 3️⃣ Trigonometry
print("\n---- Trigonometry ----")
print(math.sin(1))
print(math.cos(1))
print(math.pi)
print(math.e)

# 4️⃣ random numbers
print("\n---- random module ----")
print(random.random())
print(random.randint(1, 10))

# 5️⃣ random list operations
print("\n---- random list ----")
arr = [1, 2, 3, 4, 5]
print(random.choice(arr))
random.shuffle(arr)
print(arr)