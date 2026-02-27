import re

# 1) 'a' followed by zero or more 'b'
def task1(s: str) -> bool:
    return bool(re.fullmatch(r"ab*", s))

# 2) 'a' followed by 2 to 3 'b'
def task2(s: str) -> bool:
    return bool(re.fullmatch(r"ab{2,3}", s))

# 3) lowercase letters joined with underscore
def task3(s: str):
    return re.findall(r"[a-z]+_[a-z]+", s)

# 4) one uppercase letter followed by lowercase letters
def task4(s: str):
    return re.findall(r"[A-Z][a-z]+", s)

# 5) 'a' followed by anything, ending in 'b'
def task5(s: str) -> bool:
    return bool(re.fullmatch(r"a.*b", s))

# 6) replace space/comma/dot with colon
def task6(s: str) -> str:
    return re.sub(r"[ ,\.]", ":", s)

# 7) snake_case -> camelCase
def task7(s: str) -> str:
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s)

# 8) split at uppercase letters
def task8(s: str):
    return [x for x in re.split(r"(?=[A-Z])", s) if x]

# 9) insert spaces before capitals (not at start)
def task9(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", s)

# 10) camelCase -> snake_case
def task10(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def main():
    print("=== Task 1 ===")
    print(task1("a"), task1("ab"), task1("abbb"), task1("ac"))  # True True True False

    print("\n=== Task 2 ===")
    print(task2("abb"), task2("abbb"), task2("ab"), task2("abbbb"))  # True True False False

    print("\n=== Task 3 ===")
    print(task3("hello_world test_case Not_valid EXAMPLE_test"))  # ['hello_world', 'test_case']

    print("\n=== Task 4 ===")
    print(task4("Hello world MyName Test ABC"))  # ['Hello', 'My', 'Name', 'Test']

    print("\n=== Task 5 ===")
    print(task5("ab"), task5("a123b"), task5("axxb"), task5("ba"))  # True True True False

    print("\n=== Task 6 ===")
    print(task6("Hello, world. Python is cool"))  # Hello::world::Python:is:cool

    print("\n=== Task 7 ===")
    print(task7("hello_world_test"))  # helloWorldTest

    print("\n=== Task 8 ===")
    print(task8("HelloWorldTest"))  # ['Hello', 'World', 'Test']

    print("\n=== Task 9 ===")
    print(task9("HelloWorldTest"))  # Hello World Test

    print("\n=== Task 10 ===")
    print(task10("helloWorldTest"))  # hello_world_test


if __name__ == "__main__":
    main()