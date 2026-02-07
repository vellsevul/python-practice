x = -3
if x > 0:
    print("positive")
elif x < 0:
    print("negative")
else:
    print("zero")
###1
score = 76
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("D")
###2
temp = 18
if temp < 0:
    print("ice")
elif temp < 15:
    print("cold")
elif temp < 25:
    print("normal")
else:
    print("hot")
###3
s = "3.14"
if s.isdigit():
    print("int")
elif s.count(".") == 1 and s.replace(".", "").isdigit():
    print("float-like")
else:
    print("other")
###4
n = 30
if n % 2 == 0 and n % 3 == 0:
    print("multiple of 6")
elif n % 2 == 0:
    print("even only")
elif n % 3 == 0:
    print("multiple of 3 only")
else:
    print("neither")
###5