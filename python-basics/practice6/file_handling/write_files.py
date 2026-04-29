from pathlib import Path

file_path = Path(__file__).parent / "sample.txt"

with open(file_path, "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.write("This is Practice 6\n")