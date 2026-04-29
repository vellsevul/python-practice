for i in range(1, 11):
    if i % 3 == 0:
        continue
    print(i)
##1
words = ["hi", "", "python", "", "ok"]
for w in words:
    if not w:
        continue
    print(w.upper())
##2
arr = [2, 3, 4, 5, 6]
for x in arr:
    if x % 2 != 0:
        continue
    print("even:", x)
##3
s = "a1b2c3"
for ch in s:
    if ch.isdigit():
        continue
    print("letter:", ch)
##4
nums = [10, -5, 7, -2, 0]
pos_sum = 0
for x in nums:
    if x <= 0:
        continue
    pos_sum += x
print(pos_sum)
##5