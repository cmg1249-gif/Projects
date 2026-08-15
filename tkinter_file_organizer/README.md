# File Organizer

A small desktop app that sorts a messy folder into category subfolders by file extension.

Pick a directory, hit **Organize**, and every recognized file is moved into
`Images/`, `Documents/`, `Media/`, `Archives/` or `Installers/` inside that same
directory. A scrolling log shows each move as it happens.

Built with Python's standard library only — `tkinter`, `pathlib`, and `shutil`.
No dependencies to install.

## Running it

```bash
python main.py
```

Requires Python 3.6+ (uses f-strings and `pathlib`). `tkinter` ships with the
standard CPython installer on Windows and macOS; on most Linux distros it is a
separate package (`python3-tk` on Debian/Ubuntu).

## Categories

| Folder | Extensions |
|---|---|
| Images | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.svg` |
| Documents | `.pdf` `.docx` `.doc` `.txt` `.xlsx` `.pptx` `.csv` |
| Media | `.mp3` `.mp4` `.mkv` `.wav` `.flv` `.mov` |
| Archives | `.zip` `.rar` `.tar` `.gz` `.7z` |
| Installers | `.exe` `.msi` `.dmg` |

Files with an extension not in the table are left where they are.

To add a category or an extension, edit the `FILE_CATEGORIES` dict at the top of
`main.py`. The flat lookup table used at runtime is generated from it
automatically.

## How it works

The category map is authored in the readable, category-first shape:

```python
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ...],
    ...
}
```

That's convenient to maintain but slow to query — answering "what category is
`.jpg`?" would mean scanning every list. So at import time it gets inverted once
into a flat `extension -> category` dict, turning each lookup into a single
dict access:

```python
EXT_DICT = {".jpg": "Images", ".pdf": "Documents", ...}
```

Same data, two shapes: one for humans editing it, one for the program reading it.

## Caveats

File moves are **not reversible** from within the app. Try it on a scratch
folder before pointing it at anything you care about.

If a file of the same name already exists in the destination folder, `shutil.move`
behavior depends on the platform — it may overwrite.

## Possible additions

- Preview the planned moves and confirm before executing
- Handle destination filename collisions (skip / rename / prompt)
- An "Other" bucket for unrecognized extensions
- Undo the most recent run
