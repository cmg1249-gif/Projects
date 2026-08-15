import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog as fd
import fileorganizer as fo

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

root_window = tk.Tk()

def organize_wrapper():
	user_input = fd.askdirectory()
	organize_by_extensions(user_input)

root_window.title("File Organizer")
root_window.minsize(300,200)
root_window.config(background="white", padx=20, pady=20)

#Information window
log = scrolledtext.ScrolledText(root_window, width=60, height=20, state="disabled")
log.grid(row=2, column=1)
def organize_by_extensions(dir_path):
	# Converting the string into a Path Object
	target_dir = Path(dir_path)
	if not target_dir.is_dir():
		return
	for file in target_dir.iterdir():
		if not file.is_file():
			continue
		else:
			file_ext = file.suffix
			if file_ext not in EXT_DICT:
				return
			folder_path = target_dir / EXT_DICT[file_ext]
			if not folder_path.is_dir() or not folder_path.is_file():
				folder_path.mkdir(parents=True, exist_ok=True)
				shutil.move(str(file), str(folder_path))
				log.configure(state="normal")
				log.insert("end", f"{file.name} - > {EXT_DICT[file_ext]}\n")
				log.configure(state="disabled")
				log.see("end")

#Organize button
organize_button =tk.Button(root_window, text="Organize", command=organize_wrapper)
organize_button.grid(row=0, column=1)




root_window.mainloop()
