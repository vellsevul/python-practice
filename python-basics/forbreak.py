arr = [8, 12, 15, 22]
for x in arr:
    if x % 5 == 0:
        print("first multiple of 5:", x)
        break
##1
text = "a0b0C0"
for ch in text:
    if ch.isupper():
        print("first upper:", ch)
        break
##2
for n in range(2, 100):
    if all(n % d != 0 for d in range(2, int(n**0.5) + 1)):
        print("first prime:", n)
        break
##3
arr = [1, 2, 3, 4, 5]
target = 4
for i, x in enumerate(arr):
    if x == target:
        print("index:", i)
        break
##4
for x in range(1, 1000):
    if x * x > 500:
        print(x, x*x)
        break
#5