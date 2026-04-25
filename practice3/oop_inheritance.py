def ex1():
    # Basic inheritance
    class Animal:
        def speak(self):
            return "..."

    class Dog(Animal):
        def speak(self):
            return "woof"

    print(Dog().speak())

def ex2():
    # super() call
    class Person:
        def __init__(self, name):
            self.name = name

    class Student(Person):
        def __init__(self, name, major):
            super().__init__(name)
            self.major = major

    name = input("name: ")
    major = input("major: ")
    st = Student(name, major)
    print(st.name, st.major)

def ex3():
    # overriding method + calling parent logic
    class Account:
        def __init__(self, balance=0):
            self.balance = balance

        def withdraw(self, amount):
            if amount > self.balance:
                return False
            self.balance -= amount
            return True

    class FeeAccount(Account):
        def __init__(self, balance=0, fee=1):
            super().__init__(balance)
            self.fee = fee

        def withdraw(self, amount):
            # снимаем комиссию
            return super().withdraw(amount + self.fee)

    bal = float(input("balance: "))
    fee = float(input("fee: "))
    amount = float(input("withdraw: "))
    acc = FeeAccount(bal, fee)
    print(acc.withdraw(amount))
    print("balance:", acc.balance)

def ex4():
    # multiple inheritance: Printer + Scanner => MFP
    class Printer:
        def print_doc(self, text):
            return f"Printed: {text}"

    class Scanner:
        def scan(self):
            return "Scanned document"

    class MFP(Printer, Scanner):
        pass

    device = MFP()
    text = input("text: ")
    print(device.print_doc(text))
    print(device.scan())

def ex5():
    # Polymorphism: разные фигуры -> площадь
    class Shape:
        def area(self):
            raise NotImplementedError

    class Rectangle(Shape):
        def __init__(self, w, h):
            self.w = w
            self.h = h
        def area(self):
            return self.w * self.h

    class Circle(Shape):
        def __init__(self, r):
            self.r = r
        def area(self):
            return 3.14159 * self.r * self.r

    t = input("type (rect/circle): ").strip()
    if t == "rect":
        w, h = map(float, input("w h: ").split())
        s = Rectangle(w, h)
    else:
        r = float(input("r: "))
        s = Circle(r)
    print(round(s.area(), 4))

# ---- runner ----
choice = int(input("Choose example (1-5): "))
if choice == 1: ex1()
elif choice == 2: ex2()
elif choice == 3: ex3()
elif choice == 4: ex4()
elif choice == 5: ex5()
else: print("Wrong choice")