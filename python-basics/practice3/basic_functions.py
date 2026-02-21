def ex1():
    # Нормализация имени
    s = input("Full name: ")
    parts = s.strip().split()
    parts = [p.capitalize() for p in parts]
    print(" ".join(parts))

def ex2():
    # N-е простое число
    n = int(input("n: "))

    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        d = 2
        while d * d <= x:
            if x % d == 0:
                return False
            d += 1
        return True

    count = 0
    x = 1
    while count < n:
        x += 1
        if is_prime(x):
            count += 1
    print(x)

def ex3():
    # safe_div: вернуть (ok, value)
    a = float(input("a: "))
    b = float(input("b: "))

    def safe_div(a, b):
        if b == 0:
            return False, None
        return True, a / b

    ok, val = safe_div(a, b)
    print(ok, val)

def ex4():
    # *args: сумма чисел
    arr = list(map(int, input("numbers: ").split()))

    def sum_all(*nums):
        s = 0
        for x in nums:
            s += x
        return s

    print(sum_all(*arr))

def ex5():
    # **kwargs: форматированный логгер
    msg = input("message: ")
    prefix = input("prefix (empty for default): ").strip()
    upper = input("upper? (yes/no): ").strip().lower()

    def log(message: str, **kwargs):
        pref = kwargs.get("prefix", "[LOG]")
        up = kwargs.get("upper", False)
        out = f"{pref} {message}"
        if up:
            out = out.upper()
        print(out)

    if prefix == "":
        log(msg, upper=(upper == "yes"))
    else:
        log(msg, prefix=prefix, upper=(upper == "yes"))

# ---- runner ----
choice = int(input("Choose example (1-5): "))
if choice == 1: ex1()
elif choice == 2: ex2()
elif choice == 3: ex3()
elif choice == 4: ex4()
elif choice == 5: ex5()
else: print("Wrong choice")