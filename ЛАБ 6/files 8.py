import os

def delete_file(path):
    if os.path.exists(path):
        if os.access(path, os.W_OK):
            os.remove(path)
            print("File deleted.")
        else:
            print("No write access to delete the file.")
    else:
        print("File does not exist.")

delete_file("test.txt")