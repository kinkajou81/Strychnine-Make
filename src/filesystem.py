import os
import sys
from pathlib import Path

def list_subdirectories(path: str):
    if(not os.path.isdir(path)):
        print("ERROR: Invalid directory: " + path + "\n")
        sys.exit(1)

    with os.scandir(path) as it:
        return [
            entry.path
            for entry in it
            if entry.is_dir() and not entry.name.startswith(".")
        ]
        

def list_subdirectories_ex(path: str, recursive: bool):
    if(not recursive):
        return list_subdirectories(path)

    if(not os.path.isdir(path)):
        print("ERROR: Invalid directory: " + path + "\n")
        sys.exit(1)

    out = []
    for root, directories, _ in os.walk(path, followlinks=True):
        directories[:] = [d for d in directories if not d.startswith(".")]
        out.extend(os.path.join(root, d) for d in directories)
    return out

def make_build_directory(path: str):
    old_path = os.getcwd()

    os.chdir(path)
    os.mkdir(".strychnine_make")
    os.chdir(".strychnine_make")
    Path("data.txt").touch()

    os.chdir(old_path)

def make_build_directories(paths):
    