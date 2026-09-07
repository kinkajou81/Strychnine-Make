import os
from threading import Thread
import subprocess
from concurrent.futures import ThreadPoolExecutor
import sys
import parser
import editing
from typing import List

def mode_selection(settings_source: str):
    modes: List[str] = settings_source.split("\n")[0].split(" ")
    
    print_formatted_modes: str = ""
    for mode in modes:
        print_formatted_modes += "      " + mode + "\n"

    print("\n\n" + print_formatted_modes)
    input("  Please select your desired mode:\n      ")

def main():
    flags = [x for x in sys.argv[1:] if (x[0] == "-")]
    args = [x for x in sys.argv[1:] if (x[0] != "-")]

    settings_file = open("strymake.conf", "r")
    settings_source: str = settings_file.read()
    settings_file.close()

    mode_selection(settings_source)

    return 0

errcode = main()
if(errcode != 0):
    print("Exiting With Failure...")
