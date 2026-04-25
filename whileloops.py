n = 12345
s = 0
while n > 0:
    s += n % 10
    n //= 10
print(s)
##1
n = 72
k = 0
while n % 2 == 0:
    n //= 2
    k += 1
print("power of 2 =", k)
##2
x = 1
i = 0
while x < 1000:
    x *= 3
    i += 1
print(i, x)
##3
a, b = 0, 1
count = 10
while count > 0:
    print(a, end=" ")
    a, b = b, a + b
    count -= 1
##4
n = 100
while n > 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
print(n)
##5