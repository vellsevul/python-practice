import os

os.makedirs("test_folder/subfolder", exist_ok=True)

print("Current directory:", os.getcwd())
print("Files:", os.listdir())