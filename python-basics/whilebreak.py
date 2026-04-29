n = 2
while True:
    if all(n % d != 0 for d in range(2, int(n**0.5) + 1)):
        print("first prime >=2 is", n)
        break
    n += 1
##1
arr = [4, 8, 10, 15, 22]
i = 0
while i < len(arr):
    if arr[i] % 3 == 0:
        print("found multiple of 3:", arr[i])
        break
    i += 1
##2
x = 1
while True:
    x *= 2
    if x > 200:
        break
print(x)
##3
text = "abcXYZ"
i = 0
while i < len(text):
    if text[i].isupper():
        print("first upper:", text[i])
        break
    i += 1
##4
attempts = 0
while attempts < 5:
    attempts += 1
    if attempts == 3:
        print("locked")
        break
##5