"""File sorting logic, with no GUI attached.

Keeping this separate from main.py means the organizing can be run and tested
from a plain script or a REPL without opening a window.
"""

from pathlib import Path
import shutil

FILE_CATEGORIES = {
	"Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
	"Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
	"Media": [".mp3", ".mp4", ".mkv", ".wav", ".flv", ".mov"],
	"Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
	"Installers": [".exe", ".msi", ".dmg"],
}

# The map above is grouped so it is easy to read and edit, but answering
# "what category is .jpg?" would mean scanning every list. Invert it once here
# so each lookup at run time is a single dict access.
EXT_DICT = {}
for category, extensions in FILE_CATEGORIES.items():
	for extension in extensions:
		EXT_DICT[extension] = category


def organize_by_extensions(dir_path):
	"""Move every recognized file in dir_path into a category subfolder.

	Returns a list of (filename, category) pairs describing what was moved, so
	the caller can display or log the results. Files whose extension is not in
	EXT_DICT are left alone.
	"""
	target_dir = Path(dir_path)
	if not target_dir.is_dir():
		return []

	moved = []
	# Snapshot the listing first: the loop creates folders and moves files
	# inside target_dir, and iterdir() reads the directory lazily.
	for file in list(target_dir.iterdir()):
		if not file.is_file():
			continue

		category = EXT_DICT.get(file.suffix.lower())
		if category is None:
			continue

		folder_path = target_dir / category
		folder_path.mkdir(parents=True, exist_ok=True)
		shutil.move(file, folder_path)
		moved.append((file.name, category))

	return moved
