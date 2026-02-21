def ex1():
    # Point distance
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def dist(self, other):
            dx = self.x - other.x
            dy = self.y - other.y
            return (dx*dx + dy*dy) ** 0.5

    x1, y1 = map(float, input("x1 y1: ").split())
    x2, y2 = map(float, input("x2 y2: ").split())
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    print(round(p1.dist(p2), 4))


def ex2():
    # BankAccount with operations
    class BankAccount:
        def __init__(self, owner, balance=0.0):
            self.owner = owner
            self.balance = balance

        def deposit(self, amount):
            self.balance += amount

        def withdraw(self, amount):
            if amount > self.balance:
                return False
            self.balance -= amount
            return True

    owner = input("owner: ")
    acc = BankAccount(owner)
    n = int(input("ops: "))
    for _ in range(n):
        op, val = input("D/W value: ").split()
        val = float(val)
        if op == "D":
            acc.deposit(val)
        else:
            print(acc.withdraw(val))
    print("balance:", acc.balance)


def ex3():
    # TodoItem with __str__
    class TodoItem:
        def __init__(self, title):
            self.title = title
            self.done = False

        def mark_done(self):
            self.done = True

        def __str__(self):
            return f"[{'x' if self.done else ' '}] {self.title}"

    t = TodoItem(input("task: "))
    cmd = input("cmd (done/skip): ").strip()
    if cmd == "done":
        t.mark_done()
    print(str(t))


def ex4():
    # Character battle
    class Character:
        def __init__(self, name, hp, damage):
            self.name=name
            self.hp=hp
            self.damage=damage

        def attack(self, other):
            other.hp-=self.damage

    player=Character("Hero", 100, 10)
    enemy=Character("Orc", 80, 15)
    player.attack(enemy)
    print(enemy.hp)


def ex5():
    # Simple inventory (list of objects)
    class Product:
        def __init__(self, title, price):
            self.title = title
            self.price = price

    n = int(input("n: "))
    items = []
    for _ in range(n):
        title = input("title: ")
        price = float(input("price: "))
        items.append(Product(title, price))

    # найти самый дорогой
    best = items[0]
    for it in items[1:]:
        if it.price > best.price:
            best = it
    print("most expensive:", best.title, best.price)


# ---- runner ----
choice = int(input("Choose example (1-5): "))
if choice == 1:
    ex1()
elif choice == 2:
    ex2()
elif choice == 3:
    ex3()
elif choice == 4:
    ex4()
elif choice == 5:
    ex5()
else:
    print("Wrong choice")