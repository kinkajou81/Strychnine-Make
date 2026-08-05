from typing import List

def get_modes(list_strings: List[str]) -> List[str]:
    out: List[str] = []
    line: int = 0
    while(list_strings[line][:1] != "??"):
        out.append(list_strings[line])
        line += 1
