x = -8
sign = "pos" if x > 0 else ("neg" if x < 0 else "zero")
print(sign)
##1
s = "  hi "
clean = s.strip() if s and s.strip() else "EMPTY"
print(clean)
#2
a, b = 10, 7
print(a if a > b else b)
##3
n = 9
print("odd" if n % 2 else "even")
##4
arr = []
print(arr[0] if arr else "no first element")
##5
