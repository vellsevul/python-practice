from pathlib import Path
import shutil

# папка текущего файла
BASE_DIR = Path(__file__).parent

# путь к sample.txt
source = BASE_DIR.parent / "file_handling" / "sample.txt"

# папка назначения
destination_folder = BASE_DIR / "destination"
destination_folder.mkdir(exist_ok=True)

# конечный файл
destination = destination_folder / "sample.txt"

shutil.move(source, destination)

print("File moved successfully!")