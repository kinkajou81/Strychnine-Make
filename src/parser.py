from typing import List
import string_editing as se
import sys

# all instances of list_strings are expected to have leading and trailing whitespace stripped

def get_modes(list_strings: List[str]) -> List[str]:
    out: List[str] = []
    line: int = 0
    while(list_strings[line][:2] != "??"):
        out.append(list_strings[line])
        line += 1
    if(out == []):
        print("ERROR: Malformed mode header\n", file=sys.stderr)
        exit(-1)

    return out

def find_mode_bounds(mode: str, list_strings: List[str]) -> List[int]:
    out: List[int] = [0,0]
    target: str = "??>" + mode

    line: int = 0 # two loops with shared index to ensure proper ordering
    while(line < len(list_strings)):
        if(se.remove_whitespace(list_strings[line]) == target):
            out[0] = line
            break
        line += 1
    while(line < len(list_strings)):
        if(se.remove_whitespace(list_strings[line]) == "??."):
            out[1] = line
            break
        line += 1
    if(out[1] == 0):
        print("ERROR: Malformed mode: " + mode + "\n", file=sys.stderr)
        exit(-1)

    return out

def parse_compiler_relations(s: str):
    list_s = s.split(" ")
    out = []

    for segment in list_s:
        if((segment.find("??'") != -1) and (segment.find("??\"") != -1)):
            out.append(segment[:segment.find("??'")])
            out.append(segment[(segment.find("??'") + 3):segment.find("??\"")])
            out.append(segment[(segment.find("??\"") + 3):])
        else:
            print("ERROR: Malformed compiler relation\n", file=sys.stderr)
            exit(-1)
    return out

def parse_build_variables(s: str):
    list_s = s.split(" ")
    out = []

    for segment in list_s:
        if(segment.find("??=") != -1):
            out.append(segment[:segment.find("??=")])
            out.append(segment[(segment.find("??=") + 3):])
        else:
            print("ERROR: Malformed build variables", file=sys.stderr)
            exit(-1)
    return out

