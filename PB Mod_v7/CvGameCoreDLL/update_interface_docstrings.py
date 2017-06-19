#!/usr/bin/env python

# The function declaration of Boost::Python objects are hardcoded
# as string. This Script should show changes/update this strings.
#
# (Example of such issue in Civ4:BTS is CyPlayer::initUnit.)
#

import os
import glob
import pdb 
# pdb.set_trace()

REWRITE_FILES = True
VERBOSE = 1
DEBUG_WRITE = False  # Write into /run/shm/[CvFoobar].tmp.cpp

file_cache = dict()

def get_function(line):
    if "python::init" in line:  # Constructor line is without name.
        return None

    b = line.find("&")
    if b == -1: raise Exception("No begin of function name found.")
    e = line.find(",", b)
    if e == -1: e = line.find(")", b)
    if e == -1: raise Exception("No end of function name found.")
    return (line[b+1:e], b+1, e)

def get_doc(line):
    # Restrict on substring after second ','
    c1 = line.find(",")
    c2 = line.find(",", c1+1)
    if c2 == -1: c2 = line.find(")", c1+1)

    b = line.rfind(", \"", c2)
    if b == -1: return (", (\"\"", c2+1, c2+1)
    e = line.find("\"", b+3)
    if e == -1: return (", (\"\"", c2+1, c2+1)
    return (line[b+2:e+1], b+2, e+1)

def get_cpp_filename(func_name):
    """ Return filename WITHOUT extension. """
    return func_name[:func_name.find(":")]

def get_sub_funcname(func_name):
    """ Return (right most) substring [b] of [a]::[b]. """
    return func_name[func_name.rfind("::")+2:]

def get_cpp_file(fname, explizit_fname=None):
    if fname in file_cache:
        return file_cache[fname]

    if VERBOSE: print("\tLoad %s..." % (fname))
    try:
        with open(fname+".cpp", "r") as f:
            file_cache[fname] = f.readlines()
    except IOError:
        if fname == "CvInfos":  # Prevent rekursion
            raise Exception("CvInfos.cpp missing")

        info = get_cpp_file("CvInfos")
        file_cache[fname] = info

    return file_cache[fname]

def clean_args(sArgs):
    """ Convert boost::python::list& into list, etc. """
    sArgs = sArgs.replace("&", "")
    colon_pos  = sArgs.find("::")
    while colon_pos > -1: 
        b = max([
            sArgs.rfind(" ", 0, colon_pos),
            sArgs.rfind("(", 0, colon_pos)])
        lArgs = [c for c in sArgs]
        # print("Remove %i %i %s" % (b+1, colon_pos+2, lArgs[b+1:colon_pos+2]))
        lArgs[b+1:colon_pos+2] = []
        sArgs = "".join(lArgs)

        colon_pos  = sArgs.find("::")

    sArgs = sArgs.replace(" /*", " (")
    sArgs = sArgs.replace("*/ ", ") ")
    return sArgs

def get_new_doc(func_name):
    cpp_file = get_cpp_file(get_cpp_filename(func_name))
    loc_func_name = get_sub_funcname(func_name)
    search_pat = "::%s" % (loc_func_name)
    if VERBOSE: print("Search %s" % (search_pat))
    for iLine in range(len(cpp_file)):
        line = cpp_file[iLine]
        if search_pat in line:
            # Check if declaration is in one line
            n = 1
            while n < 5 and len(line.split("(")) != len(line.split(")")):
                line[-1] = []  # Remove '\n'
                line += cpp_file[iLine+n]
                n += 1

            args = line[line.find("("):line.find(")")+1]
            # ret_arg = line[:line.find(" ")]
            ret_arg = line[:line.rfind(" ", 0, line.find("::"))]

            args = clean_args(args)
            ret_arg = clean_args(ret_arg)
            return "%s %s" % (ret_arg, args)

    # "Function not found" 
    return None

def save_comment_string(old_doc, new_doc):
    """ Transfer comment after ' - ' string in old doc string. """
    com = " - "
    if com in old_doc and com not in new_doc:
        new_doc = new_doc + old_doc[old_doc.find(com):old_doc.rfind("\"")]

    return new_doc

def update(line):
    if VERBOSE: print(line)
    tFunc = get_function(line)
    if tFunc is None:
        return line

    tDoc = get_doc(line)
    sOldDoc = tDoc[0]
    sNewDoc = get_new_doc(tFunc[0])
    if sNewDoc is None:
        if VERBOSE: print("\t Function not found: %s" %(tFunc[0]))
        return line

    sNewDoc = save_comment_string(sOldDoc, sNewDoc)

    # print("----- %s\n%s\n\"%s\"\n" % (tFunc[0], sOldDoc, sNewDoc))

    # Replace ')' with ', ' if line without doc string get new one.
    end = line[tDoc[1]-1]
    end2 = ""
    if end == ")":
        end = ", "
        end2 = ")"

    newLine = "%s%s\"%s\"%s%s\r\n" % (line[:tDoc[1]-1], end, sNewDoc,
                                      end2, line[tDoc[2]])
    return newLine

if __name__ == "__main__":

    interfaces = glob.glob("Cy*Interface*.cpp")
    # interfaces = ['CyAreaInterface.cpp']
    for interface in interfaces:
        print("Handle " + interface)
        with open(interface, "r") as f:
            txt = f.readlines()
            new_txt = []
            for line in txt:
                if ".def(" in line: 
                    line = update(line)

                new_txt.append(line) 

        if new_txt != txt:
            # print(new_txt)
            out = "".join(new_txt)
            out = out.replace('\r\r', '\r')  # Source unknown.
            
            if REWRITE_FILES:
                print("Detect change... and rewrite file " + interface)
                with open(interface, "w") as f:
                    f.write(out)

            if DEBUG_WRITE:
                dfile = "/run/shm/" + interface.replace(".", ".tmp.")
                print("Detect change... and write file " + dfile)
                with open(dfile, "w") as f:
                    f.write(out)
