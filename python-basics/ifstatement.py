x = -5
if abs(x) == 5:
    print("distance from 0 is 5")
###1
s = "  Anel  "
if s.strip():
    print("clean:", s.strip())
###2
n = 121
if int(str(n)[::-1]) == n:
    print("palindrome")
###3
arr = [2, 4, 6, 8]
if all(x % 2 == 0 for x in arr):
    print("all even")
###4
password = "Abc123!"
if any(ch.isupper() for ch in password) and any(ch.isdigit() for ch in password):
    print("looks strong")
###5