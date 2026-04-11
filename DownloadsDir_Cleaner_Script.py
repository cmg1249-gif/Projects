import shutil
import os
import time
# This script will delete files in the specified directory that are older than one day (24 hours).
one_day_in_seconds = 86400
path = os.path.join(os.path.expanduser("~"), "Downloads")
now = time.time()
files_deleted = 0
 
 
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    last_modified = os.path.getmtime(file_path)
    age_in_seconds = now - last_modified
   
   
    if age_in_seconds >= one_day_in_seconds:
        if os.path.isfile(file_path):
            os.remove(file_path)
            files_deleted += 1
            print(f"Deleted: {file_path}")
        else:
            shutil.rmtree(file_path)
            files_deleted += 1
            print(f"Deleted directory: {file_path}")


print(f"Total files & directories deleted: {files_deleted}")
