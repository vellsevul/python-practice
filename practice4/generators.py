# generators.py

# 1️⃣ iter() и next()
print("---- Example 1: iter() and next() ----")
arr = [10, 20, 30, 40]
it = iter(arr)
print(next(it))
print(next(it))
print(next(it))

# 2️⃣ Loop through iterator
print("\n---- Example 2: Loop through iterator ----")
for x in arr:
    print(x)

# 3️⃣ Custom Iterator Class
print("\n---- Example 3: Custom Iterator ----")

class MyNumbers:
    def __init__(self, max):
        self.max = max
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.max:
            self.current += 1
            return self.current
        else:
            raise StopIteration

myclass = MyNumbers(5)
for x in myclass:
    print(x)

# 4️⃣ Generator function with yield
print("\n---- Example 4: Generator function ----")

def square_generator(n):
    for i in range(n):
        yield i * i

for value in square_generator(5):
    print(value)

# 5️⃣ Generator Expression
print("\n---- Example 5: Generator Expression ----")

gen = (x * 2 for x in range(5))
for value in gen:
    print(value)