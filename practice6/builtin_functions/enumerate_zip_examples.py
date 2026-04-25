names = ["Ali", "Dana", "Sara"]
scores = [90, 85, 95]

# enumerate
for i, name in enumerate(names):
    print(i, name)

# zip
for name, score in zip(names, scores):
    print(name, score)

# built-ins
print(len(names))
print(sum(scores))
print(min(scores))
print(max(scores))
print(sorted(scores))