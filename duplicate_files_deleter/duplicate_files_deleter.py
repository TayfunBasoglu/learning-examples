import os
import sys

#Path
path = r'Test'

os.chdir(path)

#All filenames and sizes
all_files = list()
for i in os.listdir():
    all_files.append(os.stat(i).st_size)

# Keep Files
keep_files = list(set(all_files))

# Delete Files
delete_files = all_files.copy()
for i in keep_files:
    if i in delete_files:
        delete_files.remove(i)

# Control
if len(delete_files) < 1:
    sys.exit("The duplicate file was not found.")

sure = input(str(len(delete_files))+" files will be deleted, are you sure? (y/n)\n->  ")

if sure in ["Y","y"]: 
    #Delete
    for i in os.listdir():
        file_name = i
        file_size = os.stat(i).st_size
        if file_size in delete_files:
            os.remove(file_name)
            delete_files.remove(file_size)
else:
    print("Exit")