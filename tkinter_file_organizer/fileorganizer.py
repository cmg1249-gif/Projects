import os
from pathlib import Path
import shutil
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Media": [".mp3", ".mp4", ".mkv", ".wav", ".flv", ".mov"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Installers": [".exe", ".msi", ".dmg"],
}
EXT_DICT = {}
# Building a dictionary that has its keys and values reversed so its easier to work with
for key, value in FILE_CATEGORIES.items():
	for x in value:
		EXT_DICT[x] = key

class FileOrganizer:

	def organize_by_extensions(self, dir_path):
		# Converting the string into a Path Object
		target_dir = Path(dir_path)
		if not target_dir.is_dir():
			return
		for file in target_dir.iterdir():
			if not file.is_file():
				print("File does not exist")
				continue
			else:
				file_ext = file.suffix
				if file_ext not in EXT_DICT:
					print("File extension does not exist")
					return
				folder_path = target_dir / EXT_DICT[file_ext]
				if not folder_path.is_dir() or not folder_path.is_file():
					folder_path.mkdir(parents=True, exist_ok=True)
					shutil.move(str(file), str(folder_path))





