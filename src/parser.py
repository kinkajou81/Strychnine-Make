from typing import List
import string_editing as se

def get_modes(list_strings: List[str]) -> List[str]:
    out: List[str] = []
    line: int = 0
    while(list_strings[line][:1] != "??"):
        out.append(list_strings[line])
        line += 1
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
    return out