arr = [10, 20, 30]
for idx, val in enumerate(arr):
    print(idx, val)
##1
a = [1, 2, 3]
b = [10, 20, 30]
for x, y in zip(a, b):
    print(x + y)
##2
s = "Kazakhstan"
for ch in s:
    if ch.lower() in "aeiou":
        print("vowel:", ch)
##3
arr = [3, 5, 7, 9]
for i in range(len(arr) - 1):
    print(arr[i], "->", arr[i+1])
##4
n = 6
fact = 1
for i in range(2, n + 1):
    fact *= i
print(fact)
##5