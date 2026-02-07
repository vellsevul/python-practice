a, b, c = True, False, True
print(a or b and c)  
###1
x = 12
print(not (x % 2 == 0 and x % 3 == 0)) 
###2
s = "kazakhstan"
print(("a" in s) and ("z" in s) and ("x" not in s))
###3
x = 5
print((x > 0) ^ (x < 0))  
###4
p, q = False, False
print(not (p or q) == ((not p) and (not q)))  
###5