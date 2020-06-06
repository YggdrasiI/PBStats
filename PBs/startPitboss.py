#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Installation/Setup:
#   Edit the following variables directly in this script or
#   copy 'startPitbossEnv.py.example' into 'startPitbossEnv.py' and
#   edit the values it the environment file.
#
# 1. CIV4BTS_PATH : Your Civ4:BTS installation directory
#    i.e "$HOME/Civ4/Beyond the Sword"
# 2. ALTROOT_BASEDIR: As default the absolute path on this folder.
#    Edit this if you place your games at an other position, i.e.
#    $HOME/PBs.
# 3. GAMES: Hold list of games. Expand it, if you host multiple games.
#    Every entry maps to a subfolder of ALTROOT_BASEDIR.
#
# Notes:
# • Attention, backup/move your "My Games"-Folder before
#   you start the Pitboss Server with an empty ALTROOT-Folder.
#   Due a bug in the Pitboss executable your current
#   "BTS-My Games-Folder" will be moved, not copied, to the new position!
#
# • Configure the Pitboss servers over the file 'pbSettings.json' in the
#   ALTROOT-Directory of each game.
#
# • This script assumes that the wine drive 'Z:'
#   is mapped to '/' (default wine setting).
#

import sys
import os.path
import re
import glob
import json
import struct
import fileinput
import time

# Begin of configuration

# Path to Civ4:BTS folder (without executable name)
# CIV4BTS_PATH = "$HOME/Civ4/Beyond the Sword"
CIV4BTS_PATH = r"C:\Program Files (x86)\2K Games\Firaxis Games\\"\
    r"Sid Meiers Civilization 4 Complete\Beyond the Sword"

# Folder which will be used as container for all ALTROOT directories.
# It should contains the configuration seed folder (seed)
# Set this to the subfolder '[...]/PBStats/PBs' !
# ALTROOT_BASEDIR = "$HOME/PBStats/PBs"
ALTROOT_BASEDIR = os.path.abspath(".")

# Default mod name. Can be overwritten in GAMES-dict.
# Moreover, the mod name will be changed automatically
# if the save to load contains an other mod name.
MOD = "PB Mod_v9"

# Allow restart if PB server quits
RESTART = True
# Timeout to wait a few seconds before the pitboss server restarts.
RESTART_TIMEOUT = 3

# Start command templates
START_WINDOWS = '{CIV4BTS_EXE} mod= "{MOD}"\\" /ALTROOT={ALTROOT}"'
START_LINUX = 'wine "{CIV4BTS_EXE}" mod= "{MOD}"\\\" /ALTROOT="{ALTROOT_W}"'

# Update command (For mods with ModUpdater.py)
UPDATE_WINDOWS = 'python {SCRIPT} {ARGS}'
UPDATE_LINUX = 'python {SCRIPT} {ARGS}'
UPDATE_SCRIPT = 'ModUpdater.py'

# Variant with cleaned output
UNBUFFER = False
START_LINUX_UNBUFFER = r'unbuffer wine "{CIV4BTS_EXE}" mod= "{MOD}"\\\" '\
    r'/ALTROOT="{ALTROOT_W}" | grep -v "^FTranslator::AddText\|fixme:\|err:"'

# Automatic generation of symbolic links for BTS_Wrapper
# The wrapper needs a http server which serves [ALTROOT]/Saves/pitboss/auto
BTS_WRAPPER_WWW_DIR = None

# (Linux only)Path for xvfb-run framebuffer.
# Screenshot available via 'xwud --id $XVFB_DIR'
XVFB = False
XVFB_DIR = "/run/shm/{GAMEID}"
XVFB_MCOOKIE = "/tmp/{GAMEID}"
XVFB_CMD = 'xvfb-run -a -e /dev/shm/xvfb.{GAMEID}.err --auth-file={COOKIE} '\
    '-s "-fbdir {DIR} -screen 0 640x480x24"'\
    'wine "{CIV4BTS_EXE}" mod= "{MOD}"\\\" /ALTROOT="{ALTROOT_WIN}" &'
XVFB_PRE_CMD = '$(sleep 3; xauth merge {COOKIE}) &'  # ; fg'

# Seed directory
# ALTROOT_SEED = os.path.join(ALTROOT_BASEDIR, "seed")

INI = "CivilizationIV.ini"
INI_OPT = "PitbossSMTPLogin"

EXTENSION = ".CivBeyondSwordSave"
# End of configuration

# Put your overrides of aboves values into following file
if os.path.exists("startPitbossEnv.py"):
    print("Load local environment")
    sys.path.append(".")
    if int(sys.version[0]) < 3:
        execfile(os.path.join('startPitbossEnv.py'))
    else:
        exec(open(os.path.join('startPitbossEnv.py')).read())

####################
# List of games. Insert the names of your games here or define
# an own dict in startPitbossEnv.py
if "GAMES" not in globals():
    GAMES = {
        "1": {"name": "Pitboss 1", "mod": MOD,
              "altroot": os.path.join(ALTROOT_BASEDIR, "PB1")},
        "2": {"name": "Pitboss 2", "mod": MOD,
              "altroot": os.path.join(ALTROOT_BASEDIR, "PB2")},
        "seed": {"name": "Example", "mod": MOD,
                 "altroot": os.path.join(ALTROOT_BASEDIR, "seed")},
    }
###################


def my_input(t=""):
    # Branch for Python2/3
    if int(sys.version[0]) < 3:
        return raw_input(t)
    else:
        return input(t)


def init():
    # Expand environment variables
    globals()["ALTROOT_BASEDIR"] = os.path.expandvars(ALTROOT_BASEDIR).strip()
    globals()["CIV4BTS_PATH"] = os.path.expandvars(CIV4BTS_PATH).strip()
    globals()["MOD"] = os.path.expandvars(MOD).strip()
    # globals()["ALTROOT_SEED"] = os.path.expandvars(ALTROOT_SEED).strip()
    if XVFB:
        globals()["XVFB_DIR"] = os.path.expandvars(XVFB_DIR).strip()

    for g in GAMES:
        game = GAMES[g]
        for k in game:
            game[k] = os.path.expandvars(game[k]).strip()


def checkIniFile(gameid):
    """ The PitbossSMTPLogin variable had to contain the altroot path."""
    altroot = GAMES[gameid]["altroot"]
    altroot_w = getAltrootWin(altroot)
    altroot_ini = ""
    iniFn = os.path.join(altroot, INI)
    opt = INI_OPT+"="
    if os.path.isfile(iniFn):
        fp = open(iniFn, mode="r")
        ini = fp.readlines()
        fp.close()
    else:
        # print("{} not found.".format(iniFn[iniFn.rfind(os.path.sep)+1:]))
        print("{} not found.".format(iniFn))
        return None

    for line in ini:
        if line.startswith(opt):
            altroot_ini = line[line.find("=")+1:].strip()

    return altroot_ini == altroot_w


def fixIniFile(gameid):
    """ Set PitbossSMTPLogin variable on altroot path."""

    if checkIniFile(gameid):
        # Nothing to do
        return True

    altroot = GAMES[gameid]["altroot"]
    altroot_w = getAltrootWin(altroot)
    iniFn = os.path.join(altroot, INI)
    opt = INI_OPT+"="
    if os.path.isfile(iniFn):
        for line in fileinput.input(iniFn, inplace=True, backup=".pybak"):
            if line.startswith(opt):
                print("{}{}".format(opt, altroot_w))
            else:
                print(line.strip())

    else:
        print("{} not found.".format(iniFn[iniFn.rfind(os.path.sep)+1:]))
        return False

    return True


def loadSettings(gameid):
    altroot = GAMES[gameid]["altroot"]
    pbFn = os.path.join(altroot, "pbSettings.json")
    if os.path.isfile(pbFn):
        fp = open(pbFn, mode="r")
        pbSettings = json.load(fp)
        fp.close()
    else:
        return None

    return pbSettings


def saveSettings(gameid, pbSettings):
    altroot = GAMES[gameid]["altroot"]
    pbFn = os.path.join(altroot, "pbSettings.json")
    try:
        fp = open(pbFn, mode="w")
        # Note that it's necessary to use the old syntax (integer value)
        # for indent argument!
        json.dump(pbSettings, fp, indent=1)
    except Exception:
        print("Write of json file fails!")


def printSelectionMenu():
    print("""\
==== Select Game/Altroot ====
ID - Description
          """)
    for g in sorted(GAMES.keys()):
        print("  {:10.10} - {}".format(g, GAMES[g]["name"]))

    print("  {:10.10} {} - {}".format("list", "[id] [save pattern]",
                                      "Print out names of 20 youngest saves."))
    print("  {:10.10} - {}".format("help",
                                   "Print help and exit"))


def printHelp():
    print("""Syntax: python [-u] {0} gameid [savegame] [password]
    or  python [-u] {0} gameid list [pattern]

 gameid: Selects the game. Edit the GAMES-variable to define more games.
         Use the 'seed' director as template and define a different
         'altroot' directory for each game.
 savegame: If the server automatically load a save, it takes the filename
          defined in pbSettings.json.
          Use this argument to override the filename. It's not required
          to write out the full filename. The script selects the youngest file
          which match the (regular) expression.
          This is useful to load the latest save of a player.
 password: Overrides the stored password. Be careful, a wrong password traps
          the PB server in an infinite loop. The server had to be killed
          manually...
     list: Show latest saves matching a given pattern
       -u: Force unbuffered output. I.e. Required in Mingw32 bash shell

Without args: Show list of games and wait for further user input.
          """.format(sys.argv[0]))


def _add_auto_subfolders(folders):
    # Add 'PATH/auto' for each PATH
    # and convert path separators...
    folders_with_auto = []
    for s in folders:
        if os.path.sep == "/":
            s = s.replace("\\\\", "/").replace("\\", "/")
        folders_with_auto.append(s)
        folders_with_auto.append(os.path.join(s, "auto"))

    return folders_with_auto


def _made_case_insensitive(folders):
    # Made pattern case insensitive
    # (prevents 'saves/multi' vs. 'Saves/multi' struggle)

    def insensitive(text):
        a = ["[{}{}]".format(c.lower(), c.upper()) if
             c.lower() != c.upper() else c for c in text]
        return ''.join(a)

    folders = [insensitive(f) for f in folders]
    return folders


def _remove_duplicates(filenames):
    # Remove duplicates, but do not change order

    filenames_no_dup = []
    for s in filenames:
        if s not in filenames_no_dup:
            filenames_no_dup.append(s)

    return filenames_no_dup


def findSaves(gameid, pbSettings, reg_pattern=None, pattern="*"):
    """ Return list of tuples (path, creation_date) of given pattern. """
    altroot = GAMES[gameid]["altroot"]

    subfolders = [pbSettings.get("save", {}).get(
        "writefolder", os.path.join("Saves", "multi"))]
    subfolders.extend(pbSettings.get("save", {}).get("readfolders", []))
    subfolders.append(os.path.join("Saves", "pitboss"))

    subfolders = _add_auto_subfolders(subfolders)
    subfolders = _made_case_insensitive(subfolders)

    if not pattern.lower().endswith(EXTENSION.lower()):
        pattern += EXTENSION

    saves = []
    for x in subfolders:
        ss1 = os.path.join(altroot, x, pattern)
        saves.extend(glob.glob(ss1))
        ss2 = os.path.join(CIV4BTS_PATH, x, pattern)
        saves.extend(glob.glob(ss2))
        # print("{}, {}".format(ss1, ss2))

    if reg_pattern:
        reg = re.compile(reg_pattern)
        saves = [x for x in saves if reg.search(x)]

    saves = _remove_duplicates(saves)

    savesWithTimestamps = [(x, os.path.getctime(x)) for x in saves]
    # Sort by timestamp
    savesWithTimestamps.sort(key=lambda xx: xx[1])
    # Remove oldest
    while len(savesWithTimestamps) >= 20:
        savesWithTimestamps.pop(0)

    # Shift current selected save of pbSettings.json on top, but
    # warn if save was not found.
    currenty_selected = pbSettings.get("save", {}).get("filename", "undefined")
    bMissing = True
    for st in savesWithTimestamps:
        if currenty_selected == os.path.basename(st[0]):
            bMissing = False
            savesWithTimestamps.remove(st)
            savesWithTimestamps.append(st)
            break

    if bMissing and reg_pattern is None:
        print("\nWarning: Currently selected save '{0}' "
              "can not be found!\n".format(currenty_selected))

    savesWithTimestamps.reverse()
    return savesWithTimestamps


def isAutostart(pbSettings):
    # Return 1 if autostart is 'true' or '1'
    bGui = (int(pbSettings.get("gui", 1)) != 0)
    bGui = (int(pbSettings.get("noGui", not bGui)) == 0)  # Old key name
    bAutostart = (int(pbSettings.get("autostart", 0)) != 0)
    bShell = (int(pbSettings.get("shell", {}).get("enable", 0)) != 0)

    if not bAutostart:
        bAutostart = isForcedAutostart(pbSettings)

    if not bAutostart and not bGui and not bShell:
        print("Warning: Autostart flag is disabled, but gui and shell "
              "flag also.\nThe PB server handles this case like 'gui=1'")
        bAutostart = True

    return bAutostart


def isForcedAutostart(pbSettings):
    # Forced autostart flag, i.e. set by webinterface during restart
    bForcedAutostart = (int(pbSettings.get("save", {}).get(
        "oneOffAutostart", 0)) != 0)
    return bForcedAutostart


def isRestartDisabled(gameid, pbSettings):
    noRestart = bool(pbSettings.get("tmpNoRestart", False))
    if noRestart:
        # Reset trigger
        # pbSettings["tmpNoRestart"] = False
        saveSettings(gameid, pbSettings)

    return noRestart


def isUpdateFlag(pbSettings):
    bUpdate = bool(pbSettings.get("startUpdate", False))
    return bUpdate


def removeUpdateFlag(gameid, pbSettings):
    pbSettings.pop("startUpdate", None)
    # Set flag to call CyGame().setAdminPassword() after startup.
    # This restores the password protection.
    pbSettings["restorePassword"] = 1
    saveSettings(gameid, pbSettings)


def getAutostartSave(pbSettings):
    # Read current save name from pbSettings.json
    return pbSettings.get("save", {}).get("filename", None)


def replaceSave(gameid, pbSettings, save, adminpw=None):
    # Shorten path
    save = os.path.basename(save)
    # Replace filename and optionally the password in pbSettings.json
    pbSettings.setdefault("save", {})["filename"] = save
    if adminpw:
        pbSettings["save"]["adminpw"] = adminpw

    saveSettings(gameid, pbSettings)


def listSaves(gameid, reg_pattern=None):
    """ Print newest saves. """
    pbSettings = loadSettings(gameid)
    print("Youngest saves for pattern '{0}':".format(reg_pattern))
    lSaves = findSaves(gameid, pbSettings, reg_pattern)
    i = 0
    print("Nb %24.24s %-15s %s" % ("Timestamp", "Mod name",
                                   "Path (without extension)"))
    for tS in lSaves:
        i += 1
        ts = time.ctime(tS[1])
        path = tS[0]
        # name = os.path.basename(path)

        # Shrink path for trivial paths, but show non-trivial paths
        # Useful if saves with equal names but different paths exists.
        name = path

        normal_prefix = os.path.join(GAMES[gameid]["altroot"], "Saves", "")
        if name[:len(normal_prefix)] == normal_prefix:
            name = name[len(normal_prefix):]

        mod_name = parseModName(tS[0])
        if name[-len(EXTENSION):].lower() == EXTENSION.lower():
            name_without_ext = name[:-len(EXTENSION)]
        else:
            name_without_ext = name

        print("%2i %24.24s %-15s %s" % (i, ts, mod_name, name_without_ext))


def parseModName(filename):
    """ Return mod name for savegame. (Derived from FindHash.py) """

    def get_int(f):
        sx = f.read(4)
        ix = struct.unpack('<' + 'B'*len(sx), sx)
        ret = ix[0] + (ix[1] << 8) + (ix[2] << 16) + (ix[3] << 24)
        return ret

    f = open(filename, mode="rb")
    try:
        _ = f.read(4)
        mod_nameLen = get_int(f)
        b_mod_name = f.read(mod_nameLen)  # type is bytes
        mod_name = b_mod_name.decode('ascii')

        prefix = "Mods\\"
        if mod_name[:len(prefix)] == prefix:
            mod_name = mod_name[len(prefix):]

        if len(mod_name) > 0 and mod_name[-1] == "\\":
            mod_name = mod_name[:-1]

        return mod_name

    except MemoryError:
        print("Error while reading {0}").format(filename)
    finally:
        f.close()

    return ""


def getAltrootWin(altroot):
    """ Convert path with slashes into usable form as wine argument. """
    if os.path.sep == "/":
        return "Z:{}".format(altroot.replace("/", "\\\\"))
    else:
        return altroot


def setupGame(gameid, save_pat=None, password=None):
    """ Check input and starts the game.

    If save_pat is given, the script search the youngest file with the
    regular pattern 'save_pat'.  The case will be ignored.

    If password is given, the saved one will be replaced.
    Nevertheless, the startup stops if neither the new password or
    one of the passwords in pbPasswords.json not matches with
    the save password. (TODO)
    """
    print("\n==== Start {} ====\n".format(GAMES[gameid]["name"]))

    pbSettings = loadSettings(gameid)
    if save_pat:
        lSaves = findSaves(gameid, pbSettings, save_pat)
        if len(lSaves) > 0:
            newest_save = lSaves[0][0]  # [0][1] is timestamp
            replaceSave(gameid, pbSettings, newest_save, password)
    else:
        save_pat = pbSettings.get("save", {}).get("filename", "")
        lSaves = findSaves(gameid, pbSettings, save_pat)

    bAutostart = isAutostart(pbSettings)
    if bAutostart:
        print("Autostart {0}".format(
            (pbSettings.get("save", {}).get("filename", "?"))))

    if bAutostart and len(lSaves) == 0:
        print("No save found for pattern '{}'.".format(save_pat))
        return -1

    if bAutostart:
        mod_name = parseModName(lSaves[0][0])
    else:
        mod_name = select_mod_manually(GAMES[gameid]["mod"])
        # mod_name = GAMES[gameid]["mod"]

    print("Mod name: {}".format(mod_name))

    civ4bts_exe = os.path.join(CIV4BTS_PATH,
                               "Civ4BeyondSword_PitBoss.exe")

    # Check if patched executable is available
    better_executables = ["Civ4BeyondSword_PitBoss_Zulan.exe",
                          "Civ4BeyondSword_PitBoss2014.exe"]
    for e in better_executables:
        if os.path.exists(os.path.join(CIV4BTS_PATH, e)):
            civ4bts_exe = os.path.join(CIV4BTS_PATH, e)
            break

    altroot = GAMES[gameid]["altroot"]
    altroot_w = getAltrootWin(altroot)

    if not os.path.exists(civ4bts_exe):
        print("Executeable not found. Is the path correctly?\n'{}'\n"
              "".format(civ4bts_exe))
        return

    if not os.path.exists(altroot):
        print("Altroot directory found. Is the path correctly?\n'{}'\n"
              "Copy 'seed' if you want create a new game.".format(altroot))
        return

    if BTS_WRAPPER_WWW_DIR:
        create_bts_wrapper_symlink(altroot, BTS_WRAPPER_WWW_DIR)

    if XVFB:
        xvfb_dir = XVFB_DIR.format(GAMEID=gameid)
        xvfb_mcookie = XVFB_MCOOKIE.format(GAMEID=gameid)
        xvfb_cmd = XVFB_CMD.format(GAMEID=gameid,
                                   COOKIE=xvfb_mcookie,
                                   DIR=xvfb_dir, MOD=mod_name,
                                   CIV4BTS_EXE=civ4bts_exe,
                                   ALTROOT_WIN=altroot_w)
        xvfb_pre_cmd = XVFB_PRE_CMD.format(COOKIE=xvfb_mcookie)
        if not os.path.exists(xvfb_dir):
            print("Create directory for XV framebuffer.")
            from os import mkdir
            mkdir(xvfb_dir)

    # Generate start command pipe
    pre_start_cmd = None
    if os.path.sep == "\\":  # Windows
        start_cmd = START_WINDOWS.format(
            CIV4BTS_EXE=os.path.basename(civ4bts_exe),
            MOD=mod_name,
            ALTROOT=altroot)
    else:
        if XVFB:
            pre_start_cmd = xvfb_pre_cmd
            start_cmd = xvfb_cmd
        elif UNBUFFER:
            start_cmd = START_LINUX_UNBUFFER.format(
                CIV4BTS_EXE=civ4bts_exe,
                MOD=mod_name,
                ALTROOT_W=altroot_w)
        else:
            start_cmd = START_LINUX.format(
                CIV4BTS_EXE=civ4bts_exe,
                MOD=mod_name,
                ALTROOT_W=altroot_w)

    print("Start Command:\n{}".format(start_cmd))

    # Start infinite loop for the selected game
    os.chdir(CIV4BTS_PATH)

    try:
        while True:
            if isUpdateFlag(pbSettings):
                prepare_update(gameid, pbSettings, mod_name)

            if pre_start_cmd:
                os.system(pre_start_cmd)

            os.system(start_cmd)

            if isRestartDisabled(gameid, pbSettings):
                break
            if not RESTART:
                break

            sys.stdout.write("\nRestart server in {} seconds.".format(
                RESTART_TIMEOUT))
            sys.stdout.flush()
            for _ in range(RESTART_TIMEOUT):
                time.sleep(1)
                sys.stdout.write(".")
                sys.stdout.flush()

            sys.stdout.write("\n")

            # Refresh settings
            pbSettings = loadSettings(gameid)

    except KeyboardInterrupt:
        print("\nQuit script")


def select_mod_manually(default):
    """ Show list of directories of 'BTS/Mods' """

    def prompt(t):
        try:
            # user_in = default
            # if int(sys.version[0]) < 3:
            #     user_in = raw_input(t)
            # else:
            #     user_in = input(t)
            user_in = my_input(t)
        except EOFError:
            return default

        return user_in

    def get_list(folder):
        ret = {}
        ret[0] = "None"
        mod_names = [os.path.basename(x) for x in glob.glob(folder)
                     if os.path.isdir(x)]
        mod_names.sort()
        for x in mod_names:
            ret[len(ret)] = x

        return ret

    mod_list = get_list(os.path.join(CIV4BTS_PATH, "Mods", "*"))
    for m, name in sorted(mod_list.items()):
        print("  {id: 2}: {name}".format(id=m, name=name))

    user_in = prompt("Select mod ([Return] loads '{0}'): ".format(default))
    try:
        # Dict keys are integer. Convert input if possible
        user_in = int(user_in)
    except:
        pass

    if user_in in [0, mod_list[0]]:
        return None
    if user_in in mod_list:
        return mod_list[user_in]
    elif user_in in mod_list.values():
        return user_in
    elif user_in.strip() == "":
        return default
    else:
        print("Unknown mod '{user_in}'. Use default '{mod}'.". format(
            mod=default, user_in=user_in))
        return default


def prepare_update(gameid, pbSettings, mod_name):
    cur_folder = os.curdir
    mod_folder = os.path.join(CIV4BTS_PATH, "Mods", mod_name)
    script_rel_path = os.path.join("Assets", "Python", "Extras",
                                   UPDATE_SCRIPT)
    if os.path.sep == "\\":  # Windows
        update_cmd = UPDATE_WINDOWS.format(
            SCRIPT=script_rel_path,
            ARGS="--force" if isForcedAutostart(pbSettings) else "")
    else:
        update_cmd = UPDATE_LINUX.format(
            SCRIPT=script_rel_path,
            ARGS="--force" if isForcedAutostart(pbSettings) else "")

    if not os.path.isdir(mod_folder):
        print("(ModUpdater) Mod folder not found. Is the path correctly?\n"
              "'{}'\n".format(mod_folder))
        return -3
    elif not os.path.isfile(os.path.join(mod_folder, script_rel_path)):
        print("(ModUpdater) Update script not included. Does this mod"
              "supports this update mechanism?!\n")
        return -2
    else:
        print("Search and handle mod updates in\n{0}\n"
              "Cmd: {1}".format(mod_folder, update_cmd))
        os.chdir(mod_folder)
        exit_status = os.system(update_cmd)
        os.chdir(cur_folder)
        if exit_status == 0:
            removeUpdateFlag(gameid, pbSettings)
        else:
            print("Update process returns {0} != 0. Abort start"
                  "".format(exit_status))
            return -1

    return 0

def create_bts_wrapper_symlink(altroot, target_root):
    pb_name = os.path.split(altroot)[-1]
    game_path = os.path.join(target_root, pb_name)
    saves_path = os.path.join(target_root, pb_name, "Saves")
    symlink_path = os.path.join(target_root, pb_name, "Saves", "pitboss")
    for p in [game_path, saves_path]:
        if not os.path.exists(p):
            try:
                os.mkdir(p)
            except:
                print("create_bts_wrapper_symlink: Failed to create {}".format(p))
                return -2

    if not os.path.exists(symlink_path):
        try:
            os.symlink(os.path.join(altroot, "Saves", "pitboss"), symlink_path)
            print("Symlink for BTS_Wrapper created: '{}'".format(symlink_path))
        except:
            print("create_bts_wrapper_symlink: Failed to create {}".format(symlink_path))
            return -1

    return 0

if __name__ == "__main__":
    args = list(sys.argv[1:])

    init()
    if len(args) == 0:
        printSelectionMenu()
        # if int(sys.version[0]) < 3:
        #     args.extend(raw_input().split(" "))
        # else:
        #     args.extend(input().split(" "))
        args.extend(my_input().split(" "))

    # Add dummies for optional arguments
    args.append(None)
    args.append(None)
    args = args[0:3]

    if args[0] == "help":
        printHelp()
    elif args[0] == "list":
        listSaves(args[1], args[2])
    elif args[1] == "list":  # Avoid common mistake and check swaped order
        listSaves(args[0], args[2])
    else:
        if not fixIniFile(args[0]):
            print("Error: The option '{}' in '{}' contain not the altroot "
                  "path and the automated fix failed.".format(INI_OPT, INI))
        else:
            setupGame(*args)
