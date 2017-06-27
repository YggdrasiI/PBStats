#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Shell to Civ4.
        See Readme for setup information.
"""

import cmd
import sys
import re
import os.path
import socket

if sys.platform[0:3] == "win32":
    import pyreadline as readline
else:
    import readline  # For history, do not remove

from socket import gethostname
from time import sleep

# For reply's
# from threading import Thread

# Constants
# from civ4_api import *

################################################
# Attention, the console is not password protected
# Non-local IPs open your whole system!
################################################

# Default values for connection
PYCONSOLE_PORT = 3333
# PYCONSOLE_HOSTNAME = "0.0.0.0" # Invalid on windows
PYCONSOLE_HOSTNAME = "127.0.0.1"

# MY_HOSTNAME = "0.0.0.0"  # Invalid on windows
MY_HOSTNAME = "127.0.0.1"  # or
# MY_HOSTNAME = gethostname()  # or
# MY_HOSTNAME = "192.168.X.X"

# Makes ANSI escape character sequences (for producing colored terminal
# text and cursor positioning) work under MS Windows.
# Note that colouring does not work in Git bash (Win), but Cmd.exe.
USE_COLORAMA = True

# Storage file for history
PYCONSOLE_HIST_FILE = ".pyconsole.history"

MY_PROMPT = ''
# MY_PROMPT = 'civ4> '
RESULT_LINE_PREFIX = '    '
RESULT_LINE_SPLIT = (160, '  ')

BUFFER_SIZE = 1024
EOF = '\x04'

################################################

if USE_COLORAMA:
    from colorama import init, Fore, Back, Style
    init()
    ColorOut = Fore.BLUE
    ColorWarn = Fore.RED
    ColorReset = Style.RESET_ALL
else:
    ColorOut = ""
    ColorWarn = ""
    ColorReset = ""

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self, tAddrPort):
        print("Connect to %s" % str(tAddrPort))
        self.s.connect(tAddrPort)

    def close(self):
        if not self.s is None:
            # warn("Close Client")
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            self.s = None

    def send(self, msg, bRecv=True):
        self.s.send(msg + EOF)
        ret = ""
        if bRecv:
            recv = self.s.recv(BUFFER_SIZE)
            while len(recv) == BUFFER_SIZE and recv[-1] != EOF:
                ret += recv
                recv = self.s.recv(BUFFER_SIZE)

            recv = recv.strip(EOF)
            # sys.stdout.write(recv)
            ret += recv
        return ret

def caster(v):
    """ Returns casting function for a few base types. """
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, unicode):
        return "unicode"
    print("To caster defined for %s" % (str(type(v))))
    return None

class Civ4Shell(cmd.Cmd):
    intro = """
    Welcome to the Civ4 shell. Type help or ? to list commands.
    Connect to local Civ4 server with 'connect port'.
    Exit shell with 'bye'.
    """

    remote_server_adr = (PYCONSOLE_HOSTNAME, PYCONSOLE_PORT)
    local_server_adr = (MY_HOSTNAME, PYCONSOLE_PORT + 1)

    prompt = ''

    def __init__(self, *args, **kwargs):
        cmd.Cmd.__init__(self, *args)
        self.client = None
        self.server = None
        self.bImport_doc = False
        self.latest_save_list = None

        # Overwrite address
        self.remote_server_adr = (
                        kwargs.get("host", self.remote_server_adr[0]),
                        kwargs.get("port", self.remote_server_adr[1]))
        print(kwargs)
        print(self.remote_server_adr)
        # Start client
        self.init()

    def init(self):
        # Client
        if(self.client is not None):
            self.client.close()
        self.client = Client()
        try:
            self.client.connect(self.remote_server_adr)
        except ValueError:
            warn("Connecting failed. Invalid port?")

        """
        # Server
            if self.server is not None:
                self.server.stop()
                self.server_thread.join()
            self.server = Server(self.local_server_adr)
            self.server_thread = Thread(target=self.server.start)
            self.server_thread.start()
        """

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    # ----- internal shell commands -----
    def do_connect(self, arg):
        """Connect to Civ4-Instance:                       connect [PORT] [HOSTNAME]

        Default PORT: %i
        Default HOSTNAME: %s
        """
        words = arg.split(' ')
        if len(words) > 1:
            self.remote_server_adr = (str(words[1]), int(words[0]))
        elif len(words) > 0:
            self.remote_server_adr = (self.remote_server_adr[0], int(words[0]))

        self.local_server_adr = (
            self.local_server_adr[0],
            self.remote_server_adr[1] + 1)
        self.init()

    do_connect.__doc__ %= (remote_server_adr[1], remote_server_adr[0])

    def do_bye(self, arg):
        """Close Civ4 shell and exit:          bye
        """
        warn('Quitting Civ4 shell.')
        # self.send("q:", True)  # Inform server that client quits.
        self.close()
        return True

    def do_test(self, arg):
        """Send test commands to backend."""
        print(" Change amount of gold (Player 0):")
        self.default("gc.getPlayer(0).setGold(100)")

        print(" Number of units (Player 0):")
        self.default("print('Num Units: %i' % gc.getPlayer(0).getNumUnits())")
        print(" Add unit (Player 0):")
        # Attention pydoc.doc(CyPlayer.initUnit)) returns wrong declaration!
        self.default("gc.getPlayer(0).initUnit(1, 1, 1,"
                "UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)")
        self.default("print('Num Units: %i' % gc.getPlayer(0).getNumUnits())")

    def do_doc(self, arg):
        """Fetch pydoc information"""
        if len(arg) > 0:
            d = "pydoc.doc(%s)" % (arg)
        else:
            d = "pydoc.doc(%s)" % ("gc")
        if not self.bImport_doc:
            d = "import pydoc; " + d
            self.bImport_doc = True

        print(d)
        self.default(d)

    def do_config(self, args):
        """Show, save, reload or edit Pitboss configuration (requires PB Mod).

        Assumed maximal nesting depth of the json structure: 2.
        Examples to edit key:
            'config edit noGui=1'
            'config edit adminpw=the_password'
            'config edit shell/port=3334'
          Note that in example the prefix 'shell/' is required because
            the key 'port' is globally not unique.
        """

        args = args.strip().split(" ")
        if len(args) > 0 and args[0] == "show":
            settings = self.getPbSettings()
            # Get some string width, firstly.
            w = 20
            for (k, v) in settings.items():
                if isinstance(v, dict):
                    for kk in v:
                        w = max(w, len(kk)+2)

                w = max(w, len(k))
            w = [w+1, w+1-2]  # +1 for ':' and -2 for indent.

            print("==================================")
            for (k, v) in settings.items():
                if isinstance(v, dict):
                    print("%s:" % (k,))
                    for kk in v:
                        print("  %*.*s  %s" % (-w[1], w[1], kk + ":", str(v[kk])))

                else:
                    print("%*.*s  %s" % (-w[0], w[0], k + ":", str(v)))
            print("==================================")

        elif len(args) > 0 and args[0] == "save":
            d = "Webserver.savePbSettings()"
            self.default(d)
        elif len(args) > 0 and args[0] == "reload":
            # Nullify settings dict to force reload of file.
            d = "Webserver.pbSettings = None; Webserver.getPbSettings()"
            self.default(d)
        elif(len(args) > 1 and args[0] == "edit"
             and "=" in args[1]):
            conf_key = args[1].split("=")[0].split("/")  # ['b'] or ['a', 'b']
            new_value = args[1].split("=")[1]
            settings = self.getPbSettings()
            template_edit1 = "Webserver.getPbSettings()['%s'] = %s('%s');"
            template_edit2 = "Webserver.getPbSettings()['%s']['%s'] = %s('%s');"
            template_del1 = "Webserver.getPbSettings().pop('%s');"
            template_del2 = "Webserver.getPbSettings()['%s'].pop('%s');"

            changes = []
            for (k, v) in settings.items():
                if isinstance(v, dict):
                    if len(conf_key) > 1 and not conf_key[0] == k:
                        continue

                    for (kk, vv) in v.items():
                        if kk == conf_key[-1]:
                            if new_value:
                                changes.append(template_edit2 % (
                                    k, kk, caster(vv), new_value))
                            else:
                                changes.append(template_del2 % (k, kk))

                else:
                    if k == conf_key[0] and caster(v):
                        if new_value:
                            changes.append(template_edit1 % (
                                k, caster(v), new_value))
                        else:
                            changes.append(template_del1 % (k,))

                        break

            if len(changes) == 1:
                # print(changes)
                self.send("p:" + changes[0])
            elif len(changes) > 1:
                print("Key not unique: %s" % ("/".join(conf_key)))
            else:
                print("No editable key: %s" % ("/".join(conf_key)))

        else:
            print("Usage: config [show|reload|save|edit [key]=[value]]")


    def do_save(self, arg):
        """Create CivBeyondSwordSave.

        Example usage: 'save MySave'

        The path is relative to [Altroot dir]\\Saves\\multi,
        if gc.getAltrootDir() function is available.

        Otherwise, it will be paced below the game
        directory [Folder of executable]\\Saves\\multi.
        """
        if len(arg) > 0:
            saveName = "%s.CivBeyondSwordSave" % (arg.split(" ")[0])
            saveName = saveName.replace(".CivBeyondSwordSave.CivBeyondSwordSave",
                             ".CivBeyondSwordSave")

            # Path relative to game dir, but not root/altroot.
            filepath = "\\".join(["Saves", "multi", saveName])

            mode = str(self.send("M:"))
            if mode == "pb_wizard":
                warn("PB server is in startup phase and no game is loaded."
                      "\nCurrent mode is '{0}' ".format(mode))
                return

            d = """\
try:
  abs_path = gc.getAltrootDir() + "\\\\"
except AttributeError:
  abs_path = ""

fpath = \"%s%s\" % (abs_path, \"{0}\") 
if CyPitboss().save(fpath):
  print(\"Game saved as %s\" % (fpath,))
else:
  print(\"Save failed\")
""".format(filepath)
            # print(d)
            self.default(d)

        else:
            warn("No file name given.")

    def do_start(self, arg):
        """ Synonym for 'pb_start'. """
        self.do_pbstart(arg)

    def do_pb_start(self, arg):
        """ Send command to PbWizard to start game and load PbAdmin window.
        """

        mode = str(self.send("M:"))
        """
        if not mode == "pb_wizard":
            warn("PB server is not in startup phase and can't load save."
                  "\nDoes the game already run?\n"
                  "Current mode is '{0}' ".format(mode))
            return
        """

        if mode in ["pb_wizard", "pb_admin"]:
            result = self.send("l:")
            if result:
                result = result[result.find("{"):result.rfind("}")+1]

            try:
                import json
                loadable_check = json.loads(result)
            except ValueError:
                print("Can not decode result of loadable check.")
                return

            if loadable_check.get("loadable") == -1:
                warn("No file for given name '%s' found." %
                     loadable_check.get("file", "name?"))
                return
            if loadable_check.get("loadable") == -2:
                warn("Given admin password is wrong and search in list of"
                     "alternatives ( see pbPasswords.json) also fails.\n\n"
                    "Fix 'adminpw' value.")

        if mode == "pb_wizard":
                self.send("q:")  # Quit loop which blockades the startup process

        if mode == "pb_admin":
            # An other game is already loaded. Update settings file
            # and quit PB server. At next startup, the new file should be
            # loaded.
            self.send("p:Webserver.pbSettings[\"save\"][\"oneOffAutostart\"] = 1; Webserver.savePbSettings()")
            print("Restart PB server")
            self.send("Q:")

        # The backend will re-create the socket and we had to
        # reflect/respect it.
        self.close()

        # TODO: re-open of socket fails...
        # Exit as workaround...
        return True

        print("Wait a few seconds...")
        sleep(2)
        for _ in xrange(60):
            sleep(2)
            sys.stdout.write(".")
            sys.stdout.flush()
            try:
                self.init()
                print("...and open socket again.")
                return
            except socket.error:  # IOError:
                # self.close()
                pass
            except:
                pass

        warn("...reconnection failed")

    def do_pb_quit(self, arg):
        """ Send quit command (and probably restarts the server).
        """
        # self.send("p:PB.quit()")
        self.send("Q:")

    def do_status(self, arg):
        """ Return some status information.

        Should return list of player (points/gold/num units/num cities) 
        Uptime, Mode, etc
        TODO """
        result = str(self.send("s:"))
        try:
            import json
            status = json.loads(result)
        except ValueError:
            status = {"error" : "Can not decode status."}

        keys = ["error", "gameName", "gameTurn", "gameYear",
                "modName", "bAutostart", "bPaused", "mode"]
        for k in keys:
            if k in status:
                print(" %14s: %s" % (k, status[k]))

        from datetime import timedelta
        upt = status.get("uptime")
        if upt:
            upt = str(timedelta(minutes=int(upt)))
            print(" %14s: %s" % ("Total uptime", upt))

        ttv = status.get("turnTimerValue")
        if ttv:
            ttv = str(timedelta(seconds=int(ttv)/4))
            print(" %14s: %s" % ("Current timer", ttv))

        ttm = status.get("turnTimerMax")
        if ttm:
            ttm = str(timedelta(hours=int(ttm)))
            print(" %14s: %s" % ("Next timer", ttm))

        def player_status(pl):
            s = pl.get("ping", "")
            if s == "Offline":
                return ""
            return s

        print("\n%c %s %12.12s %s %12.12s %12.12s %s %s %s %s" % (
            "X", "Id", "Player", "Score", "Leader", "Nation", "Gold",
                                     "Cities", "Units", "Status"))
        for pl in status.get("players", []):
            print("%c %2i %12.12s %5.5s %12.12s %12.12s %4i %6i %5i %s" % (
                "*" if pl.get("finishedTurn") else " ",
                pl.get("id", -1),
                pl.get("name", "?"),
                pl.get("score", "-1"),
                pl.get("leader", "?"),
                pl.get("civilization", "?"),
                pl.get("gold", -1),
                pl.get("nCities", -1),
                pl.get("nUnits", -1),
                player_status(pl))
            )

        print("")

    def do_list(self, sArgs):
        """ List newest available saves.

            list [Pattern] [Number]
        """

        args = sArgs.split(" ")
        if len(args) == 1:
            # Interpret arg as number or pattern
            try:
                num = int(args[0])
                pat = ".*"
            except ValueError:
                num = -1
                if args[0].strip():
                    num = -1
                    pat = args[0]
                else:
                    num = 10
                    pat = None
        else:
            try:
                num = int(args[1])
                pat = args[0]
            except ValueError:
                num = -1
                pat = args[0]

        saves = self.getPbSaves("*", pat, num)
        saves.reverse()  # Newest at top
        index = 1
        # print(saves)
        for s in saves:
            print("%2i - %20s | %s" %(index,
                                    s.get("date", "date?"),
                                    s.get("name", "name?")))
            index += 1

        self.latest_save_list = saves

    def do_load(self, arg):
        """ Load save over it's name or the index number
        in relation to the latest list command.
        """

        try:
            num = int(arg)
            pat = ".*"
        except ValueError:
            num = -1
            pat = arg

        if not self.latest_save_list:
            # Fetch new list
            self.do_list("%s %i" % (pat, num))

        dSel = None
        if num > -1:
            l = len(self.latest_save_list)
            if l > num-1:
                dSel = self.latest_save_list[num-1]
            else:
                warn("Latest list of saves only contain %i elements" % (l,))
        else:
            reg = re.compile(pat)
            for s in self.latest_save_list:
                if reg.search(s.get("name", "name?")):
                    dSel = s
                    break

        if dSel:
            name = dSel.get("name", "name?")
            print("Select %s" % (name,))
            self.do_config("edit save/filename=%s" % (name,))

    def do_pause(self, arg):
        """ Toggle pause. """

        # See Webserver.py for details
        d = """\
if not gc.getGame().isPaused():
    gc.sendPause(0)
    print(1)
else:
    gc.getGame().setPausePlayer(-1)
    gc.sendChat("RemovePause", ChatTargetTypes.CHATTARGET_ALL)
    print(0)
"""
        result = str(self.send("p:"+d))
        feedback(result)

    def do_pb_set_timer(self, arg):
        """ Set timer for next round(s).
        
            Format: pb_set_timer {iHours}
        """
        try:
            iHours = int(arg)
            d = "PB.turnTimerChanged({0})".format(iHours)
            self.send("p:"+d)
            feedback("Set timer on %i" % (iHours,))
        except ValueError:
            warn("Input no integer.")

    def do_pb_set_current_timer(self, args):
        """ Set timer for current round.

            Format: pb_set_current_timer {iHours} [iMinutes] [iSeconds]
        """
        try:
            iArgs = [int(x) for x in args.split(" ")]
            iArgs.append(0)  # Guarantee minute arg
            iArgs.append(0)  # Guarantee second arg
        except ValueError:
            warn("Can't parse arguments.")
            return

        iSeconds = iArgs[2] + 60*iArgs[1] + 3600*iArgs[0]
        if iSeconds < 5:
            iSeconds = 5

        d = "gc.getGame().incrementTurnTimer("\
                "-PB.getTurnTimeLeft() + 4 * {0})".format(iSeconds)
        self.send("p:"+d)
        feedback("Set timer on %02i:%02i:%02i" % tuple(iArgs[0:3]))

    def default(self, line):
        """Send input as python command"""
        result = str(self.send("P:"+line))
        feedback(result)

    '''
    def do_help(self, args):
        """%s"""
        if args == "":
            cmd.Cmd.do_help(self, args)
            # Apend commands with irregular python function names
            print("Civ4 help")
            print("===========")
            print(self.do_khelp.__doc__)
            print("Further commands")
            print("================")
            print("None\n")
        elif args == "!":
            print("TO DO")
        else:
            cmd.Cmd.do_help(self, args)

    do_help.__doc__ %= (cmd.Cmd.do_help.__doc__)

    def do_khelp(self, args):
        """khelp [regex pattern] lists matching library functions/important variables.

        If a more detailed description exists the entry will be
        marked with '*'.
        Patterns with an unique result show the description.
        Note: The lookup table is big, but incomplete.
        """

        kname = args.strip()
        if kname == "":
            kname = ".*"
        kname = "^"+kname+"$"
        bRegexOk = True
        try:
            re_name = re.compile(kname, re.IGNORECASE)
        except:
            bRegexOk = False
            warn("Can not compile regular expression.")
            return

        lElems = []
        if bRegexOk:
            lElems.extend([i for i in CIV4_LIB_FUNCTIONS
                           if re.search(re_name, i["name"])
                           is not None])
            lElems.extend([i for i in CIV4_LIB_CLASSES
                           if re.search(re_name, i["name"])
                           is not None])
            lElems.extend([i for i in CIV4_LIB_OTHER
                           if re.search(re_name, i["name"])
                           is not None])

        l = ["%s%s" % (el["name"],
                       "*" if el["desc"] != "" else "")
             for el in lElems]
        if(len(l) == 0):
            warn("No Civ4 function/class/etc found for %s" % (kname,))
            return
        elif(len(l) > 20):
            print(civ4_library_abc(l))
        elif(len(l) > 1):
            print(" ".join(l))
            return
        else:
            print(civ4_library_help(lElems[0]))
            return
    '''

    def close(self):
        if(self.client is not None):
            self.client.close()
        """
        if self.server is not None:
            self.server.stop()
            self.server_thread.join()
        """

    def send(self, s, bRecv=True):
        try:
            return self.client.send(s, bRecv)
        except:
            warn("Sending of '%s' failed" % (s,))

        return ""

    def getPbSettings(self):
        d = "import simplejson as json; print(json.dumps(Webserver.getPbSettings()))"
        result = str(self.send("p:"+d))
        # print(result)
        # Strip unwanted output (reason?!)
        if result:
            result = result[result.find("{"):result.rfind("}")+1]

        try:
            import json
            settings = json.loads(result)
        except ValueError:
            print("Can not decode settings")
            settings = {}

        return settings

    def getPbSaves(self, pattern="*", regPattern=None, sOptNum=-1):
        if not regPattern:
            regPattern = ".*"
        d = """\
import simplejson as json
print(json.dumps({0}'saves':Webserver.getListOfSaves('{2}','{3}', {4}){1}))
""".format("{", "}", pattern, regPattern, sOptNum)

        # print(d)
        result = str(self.send("p:"+d))
        if result:
            result = result[result.find("{"):result.rfind("}")+1]

        try:
            import json
            saves = json.loads(result)
        except ValueError:
            print("Can not decode list of saves.")
            saves = {}

        return saves.get("saves", [])

# -----------------------------------------

# Setup tab completion
class Completer:

    def __init__(self, completer=None, shell=None, bBind=True):
        self.prefix = None
        self.shell = shell

        self.matching_words = []  # For completer
        self.completer = \
            self.complete_advanced if completer is None else completer
        if bBind:
            readline.parse_and_bind('tab: complete')
            readline.set_completer(self.complete)

    def complete(self, prefix, index):
        if prefix != self.prefix:
            # New prefix. Find all words that start with this prefix.
            self.matching_words = self.completer(prefix, index)
            self.prefix = prefix
        try:
            return self.matching_words[index]
        except IndexError:
            return None

    def complete_simple(self, text, state):
        """Re-uses the lists the vim syntax file."""
        FOOBAR = []
        l = [i for i in FOOBAR if i.startswith(text)]
        l.extend([i for i in FOOBAR if i.startswith(text)])
        return l
        # if(state < len(l)):
        #    return l[state]
        # return None

    def complete_advanced(self, text, state):
        """Old stuff"""
        l = []

        if len(l) == 0:
            l.extend([i["name"] for i in CIV4_LIB_FUNCTIONS
                      if i["name"].startswith(text)])
            l.extend([i["name"] for i in CIV4_LIB_CLASSES
                      if i["name"].startswith(text)])
            l.extend([i["name"] for i in CIV4_LIB_OTHER
                      if i["name"].startswith(text)])

        return l
        # if(state < len(l)):
        #    return l[state]
        # return None


def warn(s):
    print(ColorWarn+s+ColorReset)

def feedback(s):
    if RESULT_LINE_SPLIT is not None:
        s = restrict_textwidth(
            s,
            RESULT_LINE_SPLIT[0],
            RESULT_LINE_SPLIT[1])

    s_with_tabs = "%s%s%s%s" % (
        ColorOut,
        RESULT_LINE_PREFIX,
        s.rstrip('\n').replace('\n', '\n' + RESULT_LINE_PREFIX),
        ColorReset)
    print(s_with_tabs)
    # Restore prompt
    sys.stdout.write("%s" % (MY_PROMPT))

def restrict_textwidth(text, max_width, prefix):
    """ Fill in extra line breaks if distance between two newline
    characters is to long.
    """
    if len(text) <= max_width:
        return text

    posL = 0
    while len(text) - posL > max_width:
        posR = text.find('\n', posL, posL+max_width)
        if posR == -1:
            text = "%s\n%s%s" % (
                    text[0:posL+max_width],
                    prefix,
                    text[posL+max_width:])
            posL += max_width + 1 + len(prefix) + 1
        else:
            posL = posR+1

    return text

try:
    lib_dict
except NameError:
    lib_dict = dict()

CIV4_LIB_FUNCTIONS = []
CIV4_LIB_CLASSES = []
CIV4_LIB_OTHER = []



def start(**kwargs):
    shell = Civ4Shell(**kwargs)
    # completer = Completer(shell=shell)

    # Load history
    try:
        readline.read_history_file(PYCONSOLE_HIST_FILE)
    except IOError:
        warn("Can't read history file")

    # Load help system in background thread
    # doc_thread = Thread(target=load_civ4_library)
    # doc_thread.start()

    # Start Input loop
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        warn("Ctrl+C pressed. Quitting Civ4 shell.")
        shell.close()
    except TypeError:
        warn("Type error. Quitting Civ4 shell.")
        shell.close()
    finally:
        shell.close()

    # Write history
    try:
        readline.set_history_length(100000)
        readline.write_history_file(".pyconsole.history")
    except IOError:
        warn("Can't write history file")

if __name__ == '__main__':
    print("Use 'python Pyconsole [port]' in above folder for start")
    # start()
