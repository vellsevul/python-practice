import re

def show(title: str):
    print("\n" + "=" * 10, title, "=" * 10)

def main():
    # RegEx Introduction
    show("RegEx Introduction")
    text = "I love Python. python is cool!"
    print("text:", text)
    print("search 'Python':", bool(re.search(r"Python", text)))

    # RegEx Syntax and Metacharacters (., *, +, ?, ^, $, [], |, (), \)
    show("Metacharacters: . * + ? ^ $ [] | () \\")
    s = "ab aab abb abbb acb"
    print("s:", s)
    print("ab.:", re.findall(r"ab.", s))          # '.' any char
    print("ab*:", re.findall(r"ab*", s))          # '*' 0+ b
    print("ab+:", re.findall(r"ab+", s))          # '+' 1+ b
    print("ab?:", re.findall(r"ab?", s))          # '?' 0/1 b
    print("^ab (match begin):", bool(re.search(r"^ab", "abxx")))  # '^' start
    print("b$ (end):", bool(re.search(r"b$", "xxb")))             # '$' end
    print("[abc]x:", re.findall(r"[abc]b", s))   # [] set
    print("cat|dog:", re.findall(r"cat|dog", "cat bird dog"))     # |
    m = re.search(r"(ab)+", "abababxx")
    print("(ab)+ group:", m.group(0) if m else None)              # ()
    print(r"\. matches dot:", re.findall(r"\.", "a.b.c"))          # \ escape

    # Special Sequences (\d, \w, \s, \D, \W, \S, \A, \Z)
    show("Special Sequences: \\d \\w \\s \\D \\W \\S \\A \\Z")
    t = "User_01 has 2 cats.\nOK"
    print("t:", repr(t))
    print(r"\d:", re.findall(r"\d", t))          # digits
    print(r"\w+:", re.findall(r"\w+", t))        # words
    print(r"\s:", re.findall(r"\s", t))          # spaces/newlines
    print(r"\D+:", re.findall(r"\D+", "123ABC!!"))  # non-digits
    print(r"\W+:", re.findall(r"\W+", "ABC_12!!"))  # non-word
    print(r"\S+:", re.findall(r"\S+", t))        # non-space tokens
    print(r"\AUser:", bool(re.search(r"\AUser", t)))  # start of whole string
    print(r"OK\Z:", bool(re.search(r"OK\Z", t)))      # end of whole string

    # Sets and Character Classes
    show("Sets and Character Classes")
    x = "az AZ 09 _-."
    print("x:", x)
    print("[a-z]:", re.findall(r"[a-z]", x))
    print("[A-Z]:", re.findall(r"[A-Z]", x))
    print("[0-9]:", re.findall(r"[0-9]", x))
    print("[^a-z ] (not lowercase or space):", re.findall(r"[^a-z ]", x))

    # Quantifiers ({n}, {n,}, {n,m})
    show("Quantifiers: {n} {n,} {n,m}")
    y = "ab abb abbb abbbb"
    print("y:", y)
    print("ab{2}:", re.findall(r"ab{2}", y))         # exactly 2 b
    print("ab{2,}:", re.findall(r"ab{2,}", y))       # 2+ b
    print("ab{2,3}:", re.findall(r"ab{2,3}", y))     # 2 to 3 b

    # re.search() - Find first match
    show("re.search() - first match")
    text = "Price: 1200 KZT, old price: 1500 KZT"
    m = re.search(r"\d+", text)
    print("first number:", m.group(0) if m else None)

    # re.findall() - Find all matches
    show("re.findall() - all matches")
    nums = re.findall(r"\d+", text)
    print("all numbers:", nums)

    # re.split() - Split strings
    show("re.split()")
    line = "one,two  three.four"
    parts = re.split(r"[ ,\.]+", line)
    print("split:", parts)

    # re.sub() - Replace patterns
    show("re.sub()")
    cleaned = re.sub(r"[ ,\.]+", ":", line)
    print("replace with ':' :", cleaned)

    # re.match() - Match at beginning
    show("re.match() - match at beginning")
    print("match 'Price' at start:", bool(re.match(r"Price", "Price: 1200")))
    print("match 'Price' at start:", bool(re.match(r"Price", "X Price: 1200")))

    # Flags (IGNORECASE, MULTILINE, DOTALL)
    show("Flags: IGNORECASE / MULTILINE / DOTALL")
    multi = "Line1\nTOTAL: 18009\nLine3"
    print("IGNORECASE search 'python':", bool(re.search(r"python", "PYTHON", flags=re.IGNORECASE)))

    totals = re.findall(r"^TOTAL:.*$", multi, flags=re.MULTILINE)
    print("MULTILINE ^TOTAL:", totals)

    dot = re.search(r"Line1.*Line3", multi, flags=re.DOTALL)
    print("DOTALL Line1.*Line3:", dot.group(0) if dot else None)

if __name__ == "__main__":
    main()