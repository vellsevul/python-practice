s = "15"
if s.isdigit():
    print(int(s) * 2)
else:
    print("not a number")
###1
x = 3
y = 0
if y != 0:
    print(x / y)
else:
    print("division by zero")
###2
arr = [1, 2, 3]
if len(arr) >= 2:
    print(arr[-1] - arr[-2])
else:
    print("too short")
###3
email = "user@gmail.com"
if email.endswith("@gmail.com"):
    print("gmail")
else:
    print("not gmail")
###4
n = 29
if n > 1 and all(n % d != 0 for d in range(2, int(n**0.5) + 1)):
    print("prime")
else:
    print("not prime")
###5