from typing import List
import editing
import sys

# all instances of list_strings are expected to have leading and trailing whitespace stripped

def get_modes(list_strings: List[str]) -> List[str]:
    out: List[str] = []
    line: int = 0
    while((list_strings[line][:2] != "??") and (line < len(list_strings))):
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
        if(editing.remove_whitespace(list_strings[line]) == target):
            out[0] = line
            break
        line += 1
    while(line < len(list_strings)):
        if(editing.remove_whitespace(list_strings[line]) == "??."):
            out[1] = line
            break
        line += 1
    if(out[1] == 0):
        print("ERROR: Malformed mode: " + mode + "\n", file=sys.stderr)
        exit(-1)

    return out

def remove_comments(s: str):
    out: str = ""

    is_comment: List[bool] = [False]*len(s)
    inside_comment: bool = False

    comment_opener: str = "??/"
    comment_closer: str = "\n"

    character_position: int = 0
    while(character_position < len(s)):
        if(inside_comment):
            is_comment[character_position] = True

        if(character_position + len(comment_opener) <= len(s)):
            if(s[character_position:(character_position + len(comment_closer))] == comment_closer and inside_comment):
                is_comment[character_position] = False
                inside_comment = False
            elif(s[character_position:(character_position + len(comment_opener))] == comment_opener and not inside_comment):
                inside_comment = True
                is_comment[character_position] = True
        character_position += 1

    character_position = 0
    while(character_position < len(s)):
        if(not is_comment[character_position]):
            out += (s[character_position])
        character_position += 1

    return out

def parse_compiler_relations(s: str):
    if("??," in s):
        return "??,"

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

def parse_flags(s: str):
    if("??," in s):
        return "??,"

    list_s = s.split(" ")
    out = []

    for segment in list_s:
        if((segment.find("??'") != -1) and (segment.find("??\"") != -1)):
            out.append(segment[:segment.find("??'")])
            out.append(segment[(segment.find("??'") + 3):])
        else:
            print("ERROR: Malformed flags\n", file=sys.stderr)
            exit(-1)

    return out

def parse_build_variables(s: str):
    if("??," in s):
        return "??,"

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

def parse_directory_section(list_strings: List[str], offset: int):
    out: dict = {}
    line_number = offset

    try:
        while(line_number <= (offset + 6)):
            if "??," in list_strings[line_number]:
                line_number += 1
                continue

            if(line_number == offset):
                out["directory"] = list_strings[line_number][3:]
            elif(line_number == (offset + 1)):
                out["order"] = list_strings[line_number]
            elif(line_number == (offset + 2)):
                out["compiler_relation"] = parse_compiler_relations(list_strings[line_number])
            elif(line_number == (offset + 3)):
                out["arguments"] = list_strings[line_number].split(" ")
            elif(line_number == (offset + 4)):
                out["removed arguments"] = list_strings[line_number].split(" ")
            elif(line_number == (offset + 5)):
                out["dynamic link objects"] = list_strings[line_number].split(" ")
            elif(line_number == (offset + 6)):
                out["is executable"] = list_strings[line_number]
            line_number += 1
    except:
        print("ERROR: Settings for directory " + out["directory"] + " are too short")

    return out

