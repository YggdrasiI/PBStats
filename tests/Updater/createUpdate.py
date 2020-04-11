#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Helper script to generate Update as difference of two git
    branches.
    Requires Linux/Mac.
"""

import os
import sys

def debug(s):
    print(s)

# ===========================================================
# Note: Overwrite environment values in a file named
#       createUpdateEnv.py, but not directly here!
#
# Begin of environment setup

MOD_NAME="Updater"
TARGET_PATH= os.path.join(".", "server", MOD_NAME)
MOD_PATH_IN_REPO="tests/Updater/Mods/Updater/"  # without leading './'!

if True:
    # More complex example where the mod folder is just a subdirectory of
    # a git repo. Here, we just want respect changes of this subdirectory.
    #
    # Path is relative to root of git project.

    RELATIVE_MOD_PATH=os.path.join(
        os.popen("git rev-parse --show-cdup").read(-1).replace("\n", "").strip(),
        MOD_PATH_IN_REPO)
    GIT_LIST = r'git diff --name-only {{base_branch}} "{rel_mod_path}"'.format(
        rel_mod_path=RELATIVE_MOD_PATH)
    GIT_TO_REMOVE = r'git diff {{base_branch}} "{rel_mod_path}" ' \
        r'| grep -B 1 "^+++ /dev/null" ' \
        r'| sed -n "s/--- a\/\(.*\)/\1/p"'.format(rel_mod_path=RELATIVE_MOD_PATH)

    # Es wird ins Mod-Verzeichnis gewechselt und die  Dateiliste wird um
    # das passende Prefix gekürzt. Außerdem muss der Ausgabepfad des Zips
    # and das neue Arbeitsverzeichnis angepasst werden. Das geht am einfachsten
    # indem TARGET_PATH zu einem absoulten Pfad gemacht wird.
    TARGET_PATH = os.path.expanduser(TARGET_PATH)
    TARGET_PATH = os.path.abspath(TARGET_PATH)

    ZIP = r"cd '{rmp}' && echo '{{files}}' | sed -n 's#{mpir}[\/]*##p' " \
        "| zip -r \"{{update_zip}}\" -@".format(rmp=RELATIVE_MOD_PATH,
                                            mpir=MOD_PATH_IN_REPO)

    # A variant for Windows with 7z instead of zip.
    '''
    ZIP = r"cd '{rmp}' && echo '{{files}}' | sed -n 's#{mpir}[\/]*##p' " \
        "> ziplist.txt && 7z.exe a -r \"{{update_zip}}\" @ziplist.txt " \
        "&& rm ziplist.txt".format(rmp=RELATIVE_MOD_PATH,
                mpir=MOD_PATH_IN_REPO)
    '''

else:
    # Simple example where this script is directly placed in the folder
    # of the mod
    MOD_PATH_IN_REPO = "./"
    RELATIVE_MOD_PATH = "./"
    GIT_LIST = r"git diff --name-only {base_branch}"
    GIT_TO_REMOVE = r'git diff {base_branch} ' \
        '| grep -B 1 "^+++ /dev/null" ' \
        '| sed -n "s/--- a\/\(.*\)/\1/p"'
    ZIP = "echo '{files}' | zip -r \"{update_zip}\" -@"

UPDATES_HTML_TEMPLATE = '''\
<html>
  <head><title>List of updates</title></head>
  <body>
    <!--
      One line for each update. Insert new updates at the bottom of the list.
      The client will search for it's latest update file \
(identified by it's name) and 
      download all files after this entry. 

      Entries in one-line html-comments will be ignored.
    -->
    <!--<a href="https://raw.githubusercontent.com/YggdrasiI/PBStats/\
master/tests/Updater/server/example_update001.zip" \
checksum="9609a90227d4d10509f2dd68ed513837">Update 1.zip</a><br />-->
  </body>
</html>
'''

# End of environment setup
# ===========================================================

# Important if createUpdateEnv.py is symlink…
sys.path.insert(0, ".")

# Load further variables from Env file
if os.path.isfile("createUpdateEnv.py"):
    from createUpdateEnv import *


UPDATE_INFO = "update_info.json"
CONFIG=r'''{{
  "name": "{update_name}",
  "desc": "{update_desc}",
  "mod_files_to_remove": [{to_remove}]
}}'''
HTML_LINE = r'<a href="{update_name}" checksum="{checksum}">{update_name}</a><br />'
# -----------------------------------------------------------

TARGET_PATH = os.path.expanduser(TARGET_PATH)
TARGET_PATH = os.path.expandvars(TARGET_PATH)
EXTRA_LIST = [os.path.join(MOD_PATH_IN_REPO, UPDATE_INFO)]


def create_update_info(update_name, update_desc="", to_remove=[]):

    # Wrap to_remove paths with "'s
    to_remove = ['"'+t.strip()+'"' for t in to_remove if len(t.strip())>0]

    config = CONFIG.format(update_name=update_name,
                           update_desc=update_desc,
                           to_remove=",\n    ".join(to_remove))

    update_path = os.path.join(RELATIVE_MOD_PATH, UPDATE_INFO)  # Mod folder
    with open(update_path, "w") as f:
        f.write(config)


# TODO: Some redundance between UPDATES_HTML_TEMPLATE 
# and updates.template.html..
def update_html__init_folder(target_path):
    if not os.path.exists(target_path):
        try:
            os.mkdir(target_path)
        except:
            raise

    updates_html = os.path.join(target_path, "updates.html")
    if not os.path.exists(updates_html):
        with open(updates_html, "w") as f:
            f.write(UPDATES_HTML_TEMPLATE)


def update_html(update_name, zip_file):
    html_file = os.path.join(TARGET_PATH, "updates.html")
    html_file_fallback = os.path.join(TARGET_PATH,
            "..", "updates.template.html")

    # Read content of updates.html, but remove
    # line for current update if it already exists.
    if not os.path.isfile(html_file):
        print("Can not add new entry. File '{0}' not found.".format(html_file))
        if os.path.isfile(html_file_fallback):
            print("Fall back on template file '{0}'.".format(html_file_fallback))
            without_old_line =  os.open(html_file_fallback).read(-1)
        else:
            return False
    else:
        without_old_line =  os.popen("cat '{0}' | grep -v {1}".format(
                    html_file, update_name)).read(-1)

    # Gen checksum for new update zip
    md5sum = os.popen("md5sum '{0}'".format(zip_file)).read(-1)
    md5sum = md5sum[:md5sum.find(" ")]

    append_last = without_old_line.replace(
            "</body>",
            "  "+HTML_LINE.format(update_name=update_name, checksum=md5sum)+ "\n  </body>")

    print(append_last)

    # Backup previous version of html file
    if (os.path.isfile(html_file + ".old")
            and os.path.isfile(html_file)):
        # To omit WindowsError (Error 183)
        os.unlink(html_file + ".old")

    os.rename(html_file, html_file + ".old")

    # Finally, write new file
    with open(html_file, "w") as f:
        f.write(append_last)


def gen_update_name():
    # Get number of zips in target path and increment it by +1
    zips = os.popen("ls {target_path}/*.zip".format(
        target_path=TARGET_PATH)).read(-1).strip("\n")
    #print(zips)
    numZips = len(zips.split("\n")) if len(zips) > 0 else 0

    return "Update{num:03}.zip".format(num=numZips+1)


def normalize_update_name(update_name):
    update_name = update_name.replace(" ", "_")
    if not update_name.endswith(".zip"):
        update_name = update_name + ".zip"

    return update_name


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python %s {previous version branch} {Update Name} [Update description]\n" \
                "\n" \
                "Create two git branches, one for the current mod version and one for the next version." % (sys.argv[0],))

    else:
        base_branch = sys.argv[1]

        if len(sys.argv) > 2:
            update_name = normalize_update_name(sys.argv[2])
        else:
            update_name = gen_update_name()

        if len(sys.argv) > 3:
            update_desc = sys.argv[3]
        else:
            update_desc = ""

        # Gen. list of affected files
        _git_list_cmd = GIT_LIST.format(base_branch=base_branch)
        debug(_git_list_cmd)
        git_list = os.popen(_git_list_cmd).read(-1)
        full_list = git_list + " ".join(EXTRA_LIST)

        # Gen list of removed files
        _git_to_remove_cmd = GIT_TO_REMOVE.format(base_branch=base_branch)
        debug(_git_to_remove_cmd)
        git_to_remove = os.popen(_git_to_remove_cmd).read(-1)
        git_to_remove = git_to_remove.split("\n")

        print(">>>>>>> " + update_name + " <<<<<<")
        print("======= Files =========")
        print(full_list)
        print("------- Removed -------")
        if len(git_to_remove) > 0: print("\n".join(git_to_remove))
        else: print("None")
        print("=======================")

        update_html__init_folder(TARGET_PATH)

        create_update_info(update_name, update_desc, git_to_remove)
        update_zip = os.path.join(TARGET_PATH, update_name)

        bContinue = True

        print("" \
                "Press [Enter] to continue update creation " \
                "and [Ctrl+C] to abort.")
        try:
            user_in = sys.stdin.readline()
        except:
            bContinue = False

        if bContinue:
            if (os.path.isfile(update_zip + ".old")
                    and os.path.isfile(update_zip)):
                # To omit WindowsError (Error 183)
                os.unlink(update_zip + ".old")

            if os.path.isfile(update_zip):
                print("Warning, Zip file already exists. Add .old to previous file...")
                os.rename(update_zip, update_zip + ".old")

            _zip_cmd = ZIP.format(files=full_list, update_zip=update_zip)
            debug(_zip_cmd)
            ret = os.popen(_zip_cmd).read(-1)
            print(ret)

            print("" \
                    "Press [Enter] publish update (== edit update.hmtl) " \
                    "and [Ctrl+C] to abort.")
            try:
                user_in = sys.stdin.readline()
            except:
                bContinue = False

        if bContinue:
            update_html(update_name, update_zip)
