def ex1():
    # map: квадраты
    nums = list(map(int, input("numbers: ").split()))
    print(list(map(lambda x: x * x, nums)))

def ex2():
    # filter: оставить только положительные
    nums = list(map(int, input("numbers: ").split()))
    print(list(filter(lambda x: x > 0, nums)))

def ex3():
    # sorted: сортировка по модулю
    nums = list(map(int, input("numbers: ").split()))
    print(sorted(nums, key=lambda x: abs(x)))

def ex4():
    # sorted: пары name score, сорт по score desc, потом name asc
    n = int(input("n: "))
    arr = []
    for _ in range(n):
        name, score = input("name score: ").split()
        arr.append((name, int(score)))
    print(sorted(arr, key=lambda p: (-p[1], p[0])))

def ex5():
    # filter + map: оставить emails похожие на валидные и сделать lower
    emails = input("emails: ").split()
    valid = list(filter(lambda e: ("@" in e and "." in e), emails))
    print(list(map(lambda e: e.lower(), valid)))

# ---- runner ----
choice = int(input("Choose example (1-5): "))
if choice == 1: ex1()
elif choice == 2: ex2()
elif choice == 3: ex3()
elif choice == 4: ex4()
elif choice == 5: ex5()
else: print("Wrong choice")