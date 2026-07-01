import os
from threading import Thread
import subprocess
from concurrent.futures import ThreadPoolExecutor

def index_str(ls, i):
    if i in range (0, len(ls)):
        return ls[i]
    else:  
        print("WARNING: Index Out Of Bounds")
        return ""

def index_str_nowarn(ls, i):
    if i in range (0, len(ls)):
        return ls[i]
    else:  
        return ""

def ls_r_x(directory, exclusions): # list files recursively with exclusions
    directory = os.path.abspath(directory)
    for d,dirs in enumerate(exclusions):
        exclusions[d] = os.path.abspath(exclusions[d])
        
    all_files = []
    path = None
    clear = True
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            clear = True
            for ex in exclusions:
                if ex in path:
                    clear = False
                    break
            if (clear == True):
                all_files.append(path)
    return all_files

def ls_dir_r(directory): # list directories recursively
    directory = os.path.abspath(directory)
    all_dirs = []
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            all_dirs.append(os.path.join(root, d))
    return all_dirs

def async_bash(command):
    out = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    print(out)
    

def main():
    print("--------------------------------------------------------------------------------------------------------------")
    mode = input("please type base compilation mode, or type h for help: ")
    if (mode.lower() == "h"):
        # enter help page
        chelp = input("Please Type v for Verbose Mode Details or Type s for Settings Syntax: ")
        if chelp.lower() == "v":
            print("Verbose mode is for debug\nType \"v\" During Confirmation to Enter Verbose Mode\n\n    Part 0 == Initial Setup and Confirmation\n    Part 1 == Argument Gathering\n    Part 2 == Data Processing\n\n")
    elif not mode.isdigit():
        print("The Mode Must Be a Number or \"h\"")
        return 0
    
    # get directory of script
    script_dir = os.getcwd()
    
    # confirm if directory is correct
    c = input("Continue @" + str(script_dir) + " [Y/n/v]: ")
    if (c.lower() == "y" or c.lower() == "v"):
        print("Continuing...")
    else:
        return 0

    # get settings from MAKE-SETTINGS.TXT
    settingsf = open(script_dir+os.sep+"MAKE-SETTINGS.TXT", "r")
    settings = (settingsf.read()).replace("\t", "")
    settingsf.close()
    settings = settings.strip()
    list_settings = settings.split("\n")

    # check if mode is valid
    if (int(mode) > len(list_settings)):
        print("ERR: Mode Out Of Bounds")
        return -1
    elif (0 >= int(mode)):
        print("ERR: Mode Cannot Be Zero")
        return -1
    
    # get directories
    directories = [name for name in os.listdir('.') if os.path.isdir(name)]
    
    # get language versions
    lang_ver = list_settings[0]

    # prepare lists
    list_stated_dirs = []
    list_order = []
    list_flags = []
    list_rm_flags = []
    list_so_dlls = []
    start = -1
    end = -1
    base_flags = ""
    target = ""
    app_name = ""
    cancel_parse = False


    # "jump" to mode region and get/set base flags
    for line_num, line in enumerate(list_settings):
        if list_settings[int(mode)] in line and line_num != int(mode) and "??>" in line:
            start = line_num+1
            if "??" not in list_settings[start]:
                base_flags = list_settings[start]
            else:
                base_flags = "O0"
                cancel_parse = True
            if "??" not in list_settings[start+1] and cancel_parse == False:
                target = list_settings[start+1]
            else:
                target = "native"
                cancel_parse = True
            if "??" not in list_settings[start+2] and cancel_parse == False:
                app_name = list_settings[start+2]
            else:
                app_name = "My App"
            cancel_parse = False
            del list_settings[0:start]
            break
    for line_num, line in enumerate(list_settings):
        if "??." in line:
            end = line_num-1
            del list_settings[(end+1):len(list_settings)]
            break

    # validate start and end found (only prints success in verbose mode)
    if start != -1:
        if (c.lower() == "v"):
            print("----------------------<part 0>----------------------")
            print("start found at: " + str(start))
    else:
        print("ERR: start not found for mode")
        return -1
    if end != -1:
        if (c.lower() == "v"):
            print("end found at: " + str(end))
    else:
        print("ERR: end not found")
        return -1

    # if in verbose mode
    if (c.lower() == "v"):
        print("list_settings: " + str(list_settings))

    cdir = None
    cancel_parse = False
    for line_num, line in enumerate(list_settings):
        if "??:" in line:
            # get current focused directory
            cdir = line[3:len(line)]
            if (c.lower() == "v"):
                print("cdir = " + str(cdir))
            # check if this is a valid directory
            if cdir in directories:
                list_stated_dirs.append(cdir)
                
                if "??," not in index_str(list_settings,line_num+1):
                    list_order.append(index_str(list_settings,line_num+1))
                else:
                    cancel_parse = True
                    list_order.append("")
                    if (c.lower() == "v"):
                        print("parse canceled on arg: 1")
                    
                if "??," not in index_str(list_settings,line_num+2) and cancel_parse == False:
                    list_flags.append(index_str(list_settings,line_num+2))
                else:
                    cancel_parse = True
                    list_flags.append("")
                    if (c.lower() == "v"):
                        print("parse canceled on arg: 2")
                    
                if "??," not in index_str(list_settings,line_num+3) and cancel_parse == False:
                    list_rm_flags.append(index_str(list_settings,line_num+3))
                else:
                    cancel_parse = True
                    list_rm_flags.append("")
                    if (c.lower() == "v"):
                        print("parse canceled on arg: 3")
                    
                if "??," not in index_str(list_settings,line_num+4) and cancel_parse == False:
                    list_so_dlls.append(index_str(list_settings,line_num+4))
                else:
                    list_so_dlls.append("")
                    if (c.lower() == "v"):
                        print("parse canceled on arg: 4")
                    
            # clear state
            cdir = None
            cancel_parse = False
            
    if (c.lower() == "v"):
        print("----------------------<part 1>----------------------")
    print("Language Version(s): " + lang_ver)
    print("Base Flags: " + base_flags)
    print("Target: " + target)
    if (c.lower() == "v"):
        print("list_stated_dirs: " + str(list_stated_dirs))
        print("list_order: " + str(list_order))
        print("list_flags: " + str(list_flags))
        print("list_rm_flags: " + str(list_rm_flags))
        print("list_so_dlls: " + str(list_so_dlls))

    list_list_flags = [[] for _ in range(len(list_flags))]
    list_list_rm_flags = [[] for _ in range(len(list_rm_flags))]
    list_list_so_dlls = [[] for _ in range(len(list_so_dlls))]
    # tokenise flags
    for i,flags in enumerate(list_flags):
        list_list_flags[i] = flags.split(" ")
    for i,flags in enumerate(list_rm_flags):
        list_list_rm_flags[i] = flags.split(" ")
    for i,flags in enumerate(list_so_dlls):
        list_list_so_dlls[i] = flags.split(" ")
    list_base_flags = base_flags.split(" ")
        
    if (c.lower() == "v"):
        print("----------------------<part 2>----------------------")
        print("list base flags: " + str(list_base_flags))
        print("list_list_flags: " + str(list_list_flags))
        print("list_list_rm_flags: " + str(list_list_rm_flags))
        print("list_list_so_dlls: " + str(list_list_so_dlls))

    # add base flags
    for g,group in enumerate(list_flags):
        for flag in list_base_flags:
            list_list_flags[g].append(flag)

    # remove duplicates
    duplicate_check_list_list_flags = []
    for g1,grouplv1 in enumerate(list_list_flags):
        for g2,grouplv2 in enumerate(list_list_flags[g1]):
            if grouplv2 in duplicate_check_list_list_flags:
                del list_list_flags[g1][g2]
            duplicate_check_list_list_flags.append(grouplv2)
        duplicate_check_list_list_flags = []

    if (c.lower() == "v"):
        print("list_list_flags: " + str(list_list_flags))

    list_commands_gcc = []

    list_stated_dir_files = []
    for d,directory in enumerate(list_stated_dirs):
        list_stated_dir_files.append([])
        list_stated_dir_files[d] = ls_r_x()

    if (c.lower() == "v"):
        print(d)

    # prepare target
    list_target = target.split(" ")
    
    for d,directory in enumerate(list_stated_dirs):
        march = index_str_nowarn(list_target,0)
        m = index_str_nowarn(list_target,1)
        mcpu = index_str_nowarn(list_target,2)
        list_commands_gcc.append("gcc")
        for flag in list_list_flags[d]:
            list_commands_gcc[d] = list_commands_gcc[d] + " -" + flag
        for t,targ in enumerate(list_target):
            if "??," not in march and "" != march:
                list_commands_gcc[d] = list_commands_gcc[d] + " -march=" + march
            if "??," not in m and "" != m:
                list_commands_gcc[d] = list_commands_gcc[d] + " -m" + m
            if "??," not in mcpu and "" != mcpu:
                list_commands_gcc[d] = list_commands_gcc[d] + " -mcpu=" + mcpu
    print(list_commands_gcc)

    max_workers = max(min(len(list_commands_gcc), os.cpu_count() * 2, 80), 24)

    for command_gcc, com_i in enumerate(list_commands_gcc):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(async_bash, list_commands_gcc)
        print("Running: " + command_gcc)
        
    return 0

errcode = main()
if errcode == -1:
    print("Exiting With Failure...")
else:
    print("Exiting...")
