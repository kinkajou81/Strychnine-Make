import os
from threading import Thread
import subprocess
from concurrent.futures import ThreadPoolExecutor
import sys

def main():
    flags = [x for x in sys.argv[1:] if (x[0] == "-")]
    args = [x for x in sys.argv[1:] if (x[0] != "-")]

    settings_file = open("strymake.conf", "r")
    settings_source: str = settings_file.read()
    settings_file.close()

    return 0

errcode = main()
if(errcode != 0):
    print("Exiting With Failure...")
else:
    print("Exiting...")