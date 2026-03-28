# json.py

import json

# 1️⃣ JSON string → Python
print("---- Example 1: loads ----")
json_string = '{"name": "Anel", "age": 16}'
data = json.loads(json_string)
print(data)
print(data["name"])

# 2️⃣ Python → JSON string
print("\n---- Example 2: dumps ----")
new_json = json.dumps(data, indent=4)
print(new_json)

# 3️⃣ Write JSON file
print("\n---- Example 3: Write File ----")
with open("output.json", "w") as f:
    json.dump(data, f, indent=4)

# 4️⃣ Read JSON file
print("\n---- Example 4: Read File ----")
with open("output.json", "r") as f:
    loaded = json.load(f)
print(loaded)

# 5️⃣ Working with sample-data.json
print("\n---- Example 5: sample-data.json ----")
try:
    with open("sample-data.json", "r") as f:
        sample = json.load(f)
    print("Sample loaded successfully")
    print(type(sample))
except FileNotFoundError:
    print("sample-data.json not found")