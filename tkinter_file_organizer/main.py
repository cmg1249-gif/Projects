"""Tkinter front end for the file organizer."""

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog as fd

from fileorganizer import organize_by_extensions


def write_log(message):
	"""Append a line to the read-only log widget and scroll to it."""
	log.configure(state="normal")
	log.insert("end", message + "\n")
	log.configure(state="disabled")
	log.see("end")


def organize_wrapper():
	# askdirectory() returns "" when the dialog is cancelled, and Path("")
	# quietly becomes the current directory, so guard before doing anything.
	chosen = fd.askdirectory(title="Select folder to organize")
	if not chosen:
		return

	moved = organize_by_extensions(chosen)
	write_log(f"--- {chosen} ---")
	for file_name, category in moved:
		write_log(f"{file_name}  ->  {category}")
	write_log(f"{len(moved)} file(s) moved.\n")


root_window = tk.Tk()
root_window.title("File Organizer")
root_window.minsize(300, 200)
root_window.config(background="white", padx=20, pady=20)

organize_button = tk.Button(root_window, text="Organize", command=organize_wrapper)
organize_button.grid(row=0, column=1)

log = scrolledtext.ScrolledText(root_window, width=60, height=20, state="disabled")
log.grid(row=2, column=1)

root_window.mainloop()
