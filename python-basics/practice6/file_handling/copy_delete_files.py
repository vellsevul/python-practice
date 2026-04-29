import shutil
import os

# append
with open("sample.txt", "a", encoding="utf-8") as f:
    f.write("New line added\n")

# copy
shutil.copy("sample.txt", "backup.txt")

# delete backup
if os.path.exists("backup.txt"):
    os.remove("backup.txt")