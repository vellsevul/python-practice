cmd = "sum"
a, b = 4, 9
match cmd:
    case "sum": print(a + b)
    case "mul": print(a * b)
    case _:     print("unknown")
###1
op = "*"
a, b = 3, 5
actions = {"+": a + b, "-": a - b, "*": a * b}
print(actions.get(op, "bad op"))
##2
def add(a,b): return a+b
def mul(a,b): return a*b

op = "mul"
func = {"add": add, "mul": mul}.get(op)
print(func(2, 7) if func else "unknown")
###3
status = 404
match status:
    case 200 | 201: print("ok")
    case 400:       print("bad request")
    case 404:       print("not found")
    case _:         print("other")
##4
token = ("move", 10, 20)
match token:
    case ("move", x, y) if x >= 0 and y >= 0:
        print("move to", x, y)
    case ("move", _, _):
        print("negative coords")
    case _:
        print("invalid")
###5
