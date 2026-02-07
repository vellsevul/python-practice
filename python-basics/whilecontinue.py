i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue
    print(i)
##1
s = "a1b2c3d4"
i = 0
while i < len(s):
    ch = s[i]
    i += 1
    if ch.isdigit():
        continue
    print(ch)
##2
arr = [3, -1, 0, 7, -5]
i = 0
while i < len(arr):
    if arr[i] < 0:
        i += 1
        continue
    print(arr[i])
    i += 1
##3
n = 30
d = 2
while d <= n:
    if n % d != 0:
        d += 1
        continue
    print("divisor:", d)
    d += 1
##4
i = 0
total = 0
while i < 8:
    i += 1
    if i in (3, 6):
        continue
    total += i
print(total)
###5