#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Shell to Civ4.
        See Readme for setup information.
"""

import cmd
import sys
import re
import json
import os.path
import socket
from socket import gethostname
from time import sleep

if sys.platform[0:3] != "win32":
    import readline  # For history, do not remove
else:
    import pyreadline as readline

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
# PYCONSOLE_HOSTNAME = "127.0.0.1" Ok on windows
PYCONSOLE_HOSTNAME = "localhost"

# MY_HOSTNAME = "0.0.0.0"  # Invalid on windows
# MY_HOSTNAME = "127.0.0.1"  # Ok on windows
MY_HOSTNAME = "localhost"  #
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

# Civ4 3D font rendering is not utf-8-ready, but uses
# predifined char images.
# The latin1-encoding uses 7 bits, only and  suffers from
# the 'ß'-char, etc.
# cp1252 aka windows-1252 is the best choice in terms
# of compatibility.
ENCODING = 'cp1252'
ENCODING2 = 'utf-8'

################################################
ColorOut = ""
ColorWarn = ""
ColorReset = ""

if USE_COLORAMA:
    from colorama import init, Fore, Back, Style
    init()

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self, tAddrPort):
        print("Connect to %s" % str(tAddrPort))
        self.s.connect(tAddrPort)

    def close(self):
        if self.s is not None:
            # print("Close Client")
            try:
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.s = None
            except OSError as e:
                print("Shutdown failed. Error was {}".format(e))
                # Catching error avoid skip of history file write.

    def send(self, msg, bRecv=True):
        self.s.send((msg + EOF).encode(ENCODING2))  # Python3: str->bytes
        ret = ""
        if bRecv:
            recv = self.s.recv(BUFFER_SIZE).decode(ENCODING2)  # Python3: bytes->str
            while len(recv) == BUFFER_SIZE and recv[-1] != EOF:
                ret += recv
                recv = self.s.recv(BUFFER_SIZE).decode(ENCODING2)  # Python3: bytes->str

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

    MODDING-NOTE: Predefined commands are designed for pitboss servers.
                  They had no effect on normal Civ4 instances.
    """

    remote_server_adr = (PYCONSOLE_HOSTNAME, PYCONSOLE_PORT)
    local_server_adr = (MY_HOSTNAME, PYCONSOLE_PORT + 1)

    prompt = ''

    short_config_usage = "Usage: config [show|reload|save|edit [key]=[value]]"
    term_background_dark = True
    automatic_print = True

    def __init__(self, *args, **kwargs):
        cmd.Cmd.__init__(self, *args)
        self.client = None
        self.server = None
        self.bImport_doc = False
        self.latest_save_list = None

        self.setColors(self.term_background_dark)

        # Overwrite address
        self.remote_server_adr = (
            kwargs.get("host", self.remote_server_adr[0]),
            kwargs.get("port", self.remote_server_adr[1]))
        # print(kwargs)
        print("Remote machine: {}".format(str(self.remote_server_adr)))

        if "host" in kwargs:
            # Replace 'localhost' by value accessable from
            # other machines
            self.local_server_adr = (gethostname(),
                                     self.local_server_adr[1])
            print("This machine: {}".format(str(self.local_server_adr)))

        print("")
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
            self.warn("Connecting failed. Invalid port?")
        except socket.error:
            self.warn("Connecting failed. Invalid port?")

    def setColors(self, bDarkTerminal):
        if USE_COLORAMA and bDarkTerminal:
            self.colorOut = Fore.YELLOW
            self.colorWarn = Fore.RED
            self.colorReset = Style.RESET_ALL
        elif USE_COLORAMA and not bDarkTerminal:
            self.colorOut = Fore.BLUE
            self.colorWarn = Fore.RED
            self.colorReset = Style.RESET_ALL
        else:
            self.colorOut = ""
            self.colorWarn = ""
            self.colorReset = ""

    def warn(self, msg):
        print(self.colorWarn + msg + self.colorReset)

    def feedback(self, s):
        if RESULT_LINE_SPLIT is not None:
            s = restrict_textwidth(
                s,
                RESULT_LINE_SPLIT[0],
                RESULT_LINE_SPLIT[1])

        s_with_tabs = "%s%s%s%s" % (
            self.colorOut,
            RESULT_LINE_PREFIX,
            s.rstrip('\n').replace('\n', '\n' + RESULT_LINE_PREFIX),
            self.colorReset)
        print(s_with_tabs)
        # Restore prompt
        sys.stdout.write("%s" % (MY_PROMPT))


    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def webserver_action(self, action_name, action_args, iprint_result=0):
        """ Call Webserver.ActionHandlers entry"""

        action = {"action": action_name, "args": action_args}
        result = str(self.send("A:"+json.dumps(action)))
        try:
            # result_json = json.loads(result, encoding=ENCODING2)
            result_json = json.loads(result, encoding=ENCODING)
        except ValueError as e:
            print(result)
            result_json = {"info" : "Can not decode PB reply.", 'return': 'fail'}

        # Predefined styles for output printing
        if iprint_result == 2:
            self.feedback("Return value: {0}\n{1}".format(
                result_json.get("return", "None"),
                result_json.get("info")
            ))
        elif iprint_result == 1:
            self.feedback("{0}".format(
                result_json.get("info")
            ))

        return result_json

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
        self.warn('Quitting Civ4 shell.')
        # self.send("q:", True)  # Inform server that client quits.
        self.close()
        return True

    def do_test(self, arg):
        """Send test commands to backend."""
        print(" Change amount of gold (Player 0):")
        self.verbose("gc.getPlayer(0).setGold(gc.getPlayer(0).getGold())")

        print(" Number of units (Player 0):")
        self.verbose("print('Num Units: %i' % gc.getPlayer(0).getNumUnits())")
        """
        print(" Add unit (Player 0):")
        # Attention pydoc.doc(CyPlayer.initUnit)) returns wrong declaration!
        self.verbose("gc.getPlayer(0).initUnit(1, 1, 1,"
                     "UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)")
        self.verbose("print('Num Units: %i' % gc.getPlayer(0).getNumUnits())")
        """

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
        Examples to edit a value:
            'config edit gui=0'
            'config edit adminpw=the_password'
            'config edit shell/port=3334'
          Note that the prefix 'shell/' in the last example is required because
            the key 'port' is globally not unique.

            %s
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
            s = [w+1, w+1-2]  # +1 for ':' and -2 for indent.

            print("==================================")
            for (k, v) in settings.items():
                if isinstance(v, dict):
                    print("%s:" % (k,))
                    for kk in v:
                        print("  %*.*s  %s" % (-s[1], s[1], kk + ":",
                                               str(v[kk])))
                else:
                    print("%*.*s  %s" % (-s[0], s[0], k + ":", str(v)))
            print("==================================")

        elif len(args) > 0 and args[0] == "save":
            d = "PbSettings.save()"
            self.default(d)
        elif len(args) > 0 and args[0] == "reload":
            # Nullify settings dict to force reload of file.
            d = "PbSettings.load()"
            self.default(d)
        elif(len(args) > 1 and args[0] == "edit"
             and "=" in args[1]):
            conf_key = args[1].split("=")[0].split("/")  # ['b'] or ['a', 'b']
            new_value = args[1].split("=")[1]
            settings = self.getPbSettings()
            self.config_edit(conf_key, new_value, settings)
        else:
            print(self.short_config_usage)

    do_config.__doc__ %= (short_config_usage,)

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
            # filepath = "\\".join(["Saves", "multi", saveName])

            mode = str(self.send("M:"))
            if mode == "pb_wizard":
                self.warn("PB server is in startup phase and no game is loaded."
                          "\nCurrent mode is '{0}' ".format(mode))
                return

            d = """\
sname = '{0}'
if PbSettings.createSave(sname)['return'] == 'ok':
  print('Game saved as %s' % (sname,))
else:
  print('Save failed')
""".format(saveName)
            # print(d)

            # Disable automatic_print because above code can not be nested
            # (why?)
            automatic_print_backup = self.automatic_print
            self.automatic_print = False

            self.default(d)
            self.automatic_print = automatic_print_backup

        else:
            self.warn("No file name given.")

    def do_start(self, arg):
        """ Alias for 'pb_start'. """
        self.do_pb_start(arg)

    def do_pb_start(self, arg):
        """ The Pitboss startup is two staged.
        At first, a config wizard is shown.
        Later, the PbAdmin window will be drawn.

        If the game is at stage 1, this command continues with stage 2, based
        on the current settings. (Use 'config show' to list them.)

        If the game is at stage 2, it trigger a restart of the server.
        """

        mode = str(self.send("M:"))
        """
        if not mode == "pb_wizard":
            self.warn("PB server is not in startup phase and can't load save."
                  "\nDoes the game already run?\n"
                  "Current mode is '{0}' ".format(mode))
            return
        """

        if mode in ["pb_wizard", "pb_admin"]:
            result = self.send("l:")
            if result:
                result = result[result.find("{"):result.rfind("}")+1]

            try:
                loadable_check = json.loads(result, encoding=ENCODING2)
            except ValueError:
                print("Can not decode result of loadable check.")
                return

            if loadable_check.get("loadable") == -1:
                self.warn("No file for given name '%s' found." %
                          loadable_check.get("file", "name?"))
                return
            if loadable_check.get("loadable") == -2:
                self.warn("Given admin password is wrong and search in list of"
                          "alternatives ( see pbPasswords.json) also fails.\n\n"
                          "Fix 'adminpw' value.")

        if mode == "pb_wizard":
            self.send("q:")  # Quit loop which blockades the startup process

        if mode == "pb_admin":
            # An other game is already loaded. Update settings file
            # and quit PB server. At next startup, the new file should be
            # loaded.
            self.send('p:PbSettings["save"]["oneOffAutostart"]'
                      '= 1; PbSettings.save()')
            print("Restart PB server")
            sleep(1)
            self.send("Q:")

        # The backend will re-create the socket and we had to
        # reflect/respect it.
        self.close()

        # re-open of socket was failing...
        # Exit as workaround...
        # return True

        print("Wait a few seconds...")
        for _ in range(10):
            sleep(1)
            sys.stdout.write(".")
            sys.stdout.flush()

        for _ in range(60):
            sleep(2)
            sys.stdout.write(":")
            sys.stdout.flush()
            try:
                self.init()
                print("...and open socket again.")
                return
            except socket.error:  # IOError:
                # self.close()
                print("Socket error on re-opening")
            except:
                print("Error due re-opening of socket")

            try:
                self.close()
            except:
                pass

        self.warn("...reconnection failed")

    def do_pb_quit(self, arg):
        """ Send quit command (and probably restarts the server).
        """
        # self.send("p:PB.quit()")
        self.send("Q:")

        # End shell, too
        return True

    def do_pb_mod_update(self, arg):
        """ Create save without password protection.

        Save required for mod updates.
        """
        # self.send("p:PB.quit()")
        result = str(self.send("U:"))
        try:
            update_status = json.loads(result, encoding=ENCODING2)
        except ValueError:
            update_status = {"info" : "Can not decode PB reply.", 'return': 'fail'}

        self.feedback(update_status.get("info"))

    def do_pb_autostart(self, arg):
        """ Set autostart flag. Without argument, the value will be swaped.

        pb_autostart [0|1]
        """
        try:
            num = int(arg)
            args = {"value": min(num, 1)}
        except ValueError:
            args = None

        self.webserver_action("setAutostart", args, 2)

    def do_pb_headless(self, arg):
        """ Set headless mode. Without argument, the value will be swaped.

        pb_headless [0|1]
        """
        try:
            num = int(arg)
            args = {"value": min(num, 1)}
        except ValueError:
            args = None

        self.webserver_action("setHeadless", args, 2)

    def do_status(self, arg):
        """ Return some status information.

        status [full] [sort={id|score|conn}] [reverse]

        With all, the list of players contains gold, #units and #cities.
        """
        args = arg.split(" ")
        bAll = "full" in args
        bReverse = "reverse" in args
        sort_type = "id"
        for a in args:
            if a.startswith("sort="):
                sort_type = a.split("=")[1]
            if a in ["conn", "score", "id"]:
                sort_type = a

        result = str(self.send("s:"))
        try:
            status = json.loads(result, encoding=ENCODING2)
        except ValueError:
            status = {"error" : "Can not decode status."}

        # Truncate mod name
        if "modName" in status:
            m = status["modName"]
            status["modName"] = m.replace("Mods", "").strip("\\")

        mode = status.get("mode", "")
        if mode == "pb_wizard":
            keys = ["error", "modName", "bAutostart", "mode"]
        else:
            keys = ["error", "gameName", "gameTurn", "gameYear",
                    "modName", "bAutostart", "bPaused", "mode"]

        for k in keys:
            if k in status:
                print(" %14s: %s" % (k, status[k]))

        if mode == "pb_admin":
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

        if mode == "pb_admin" and "players" in status:

            players = status.get("players", [])
            if sort_type == "conn":
                players_sorted = sorted(players, key=lambda pl:
                                        hash(pl.get("ping", "")) & 0xFF00 + int(pl.get("id", 0)),
                                        reverse=not bReverse)
            elif sort_type == "score":
                players_sorted = sorted(players, key=lambda pl:
                                        int(pl.get("score", 0))*100 + int(pl.get("id", 0)),
                                        reverse=not bReverse)
            else:
                players_sorted = players.__reversed__() if bReverse else players

            gcu_head = "%s %s %s " % ("Gold", "Cities", "Units") if bAll else ""
            print("\n%c %s %12.12s %s %12.12s %12.12s %s%s" % (
                "X", "Id", "Player", "Score", "Leader",
                "Nation", gcu_head, "Status"))
            for pl in players_sorted:
                gcu = "%4i %6i %5i " % (
                    pl.get("gold", -1),
                    pl.get("nCities", -1),
                    pl.get("nUnits", -1),
                ) if bAll else ""
                print("%c %2i %12.12s %5.5s %12.12s %12.12s %s%s" % (
                    "*" if pl.get("finishedTurn") else " ",
                    pl.get("id", -1),
                    pl.get("name", "?"),
                    pl.get("score", "-1"),
                    pl.get("leader", "?"),
                    pl.get("civilization", "?"),
                    gcu,
                    player_status(pl)))

        if mode == "pb_wizard":
            print("""\n
                  Currently, no game is loaded by the server
                  because autostart is disabled or the save loading failed.

                  Use 'list', 'load' and 'pb_start' to start a game.
                  Saves with a different mod name requires a complete
                  restart of the program.""")

        print("")

    def do_ls(self, sArgs):
        """ Alias for 'list' """
        return self.do_list(sArgs)

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
                self.warn("Latest list of saves only contain %i elements" % (l,))
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
            #self.do_config("save")
            print("Type 'pb_start' to trigger restart with above file.")

    def do_pause(self, arg):
        """ Set pause. Without argument, the value will be swaped.

        pause [0|1]
        """
        try:
            num = int(arg)
            args = {"value": min(num, 1)}
        except ValueError:
            args = None

        self.webserver_action("setPause", args, 1)

    '''
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
        self.feedback(result)
    '''

    def do_pb_end_turn(self, arg):
        """ Set turn complete flag of player. Use 'status' to get player id.

            Format: pb_end_turn {iPlayer}
        """

        d = None
        if len(arg) > 0:
            # Interpret arg as number or pattern
            try:
                iPlayer = int(arg.split(" ")[0])
                d = """\
if( gc.getMAX_CIV_PLAYERS() > {iPlayer} and {iPlayer} > -1):
    if not CyPitboss().getPlayerAdminData({iPlayer}).bTurnActive:
        print(-1)
    else:
        gc.getGame().sendTurnCompletePB({iPlayer})
        print(0)
else:
    print(-2)
""".format(iPlayer=iPlayer)
                # Note that setActivePlayer(...) could crash the game if
                # the player id is to big.
            except ValueError:
                self.warn("Input argument is no integer.")
        else:
            self.warn("Argument for Player id missing.")

        if d:
            result = str(self.send("p:"+d)).strip()
            if result == "0":
                self.feedback("End turn of player {0} successful.".format(iPlayer))
            elif result == "-1":
                self.warn("Turn of player {0} is already finished.".format(iPlayer))
            else:
                self.warn("End turn of player {0} failed. Server returns '{1}'".format(iPlayer, result))


    def do_pb_set_timer(self, arg):
        """ Set timer for next round(s).

            Format: pb_set_timer {iHours}
        """
        try:
            iHours = int(arg)
            d = "PB.turnTimerChanged({0})".format(iHours)
            self.send("p:"+d)
            self.feedback("Set timer on %i" % (iHours,))
        except ValueError:
            self.warn("Input is no integer.")

    def do_pb_set_current_timer(self, args):
        """ Set timer for current round.

            Format: pb_set_current_timer {iHours} [iMinutes] [iSeconds]
        """
        try:
            iArgs = [int(x) for x in args.split(" ")]
            iArgs.append(0)  # Guarantee minute arg
            iArgs.append(0)  # Guarantee second arg
        except ValueError:
            self.warn("Can't parse arguments.")
            return

        iSeconds = iArgs[2] + 60*iArgs[1] + 3600*iArgs[0]
        if iSeconds < 5:
            iSeconds = 5

        d = "gc.getGame().incrementTurnTimer("\
                "-PB.getTurnTimeLeft() + 4 * {0})".format(iSeconds)
        self.send("p:"+d)
        self.feedback("Set timer on %02i:%02i:%02i" % tuple(iArgs[0:3]))

    def do_kick_player(self, arg):
        """ Convert player status to AI.

        kick {player id}
        """
        try:
            kick_args = {"playerId": int(arg)}
        except ValueError:
            self.warn("Cannot parse player id.")
            return

        self.webserver_action("kickPlayer", kick_args, 1)

    def do_end_player_turn(self, arg):
        """ Set turn status on done for player.

        end_player_turn {player id}
        """
        try:
            end_args = {"playerId": int(arg)}
        except ValueError:
            self.warn("Cannot parse player id.")
            return

        self.webserver_action("endPlayerTurn", end_args, 1)

    def do_chat(self, arg):
        """ Send chat message.

        Example usage: chat My message

        Type text without any quotes.
        Avoid special charatcers, Civ4 can't print out. The
        text will be encoded as windows-1252.
        """
        msg = arg
        result = self.webserver_action("chat", {"msg": msg}, 1)
        if result.get('return') ==  'ok':
            chat_log = result.get('log', [])
            for chat_msg in chat_log:
                self.feedback("|> {0}".format(chat_msg))

    def do_setMotD(self, arg):
        """ Sets message of the day.

        Example usage: setMotD  My message

        Type text without any quotes.
        Avoid special charatcers, Civ4 can't print out. The
        text will be encoded as windows-1252.
        """
        msg = arg
        self.webserver_action("setMotD", {"msg": msg}, 2)

    def do_getMotD(self, arg):
        """ Gets message of the day."""
        result_json = self.webserver_action("getMotD", {}, 0)
        if result_json.get('return') == 'ok':
            print("MotD: " + result_json.get("msg", ""))
        else:
            print(str(result_json))

    def do_list_cities(self, arg):
        """List all cities of a player.

        Usage: list_cities {Player id}

        The id can be used in 'rename_city'.
        """
        if len(arg) < 1:
            print(self.do_list_cities.__doc__)
            return

        d = None
        try:
            args = arg.split(" ")
            iPlayer = int(args[0])
            d = '''\
if( gc.getMAX_CIV_PLAYERS() > {iPlayer} and {iPlayer} > -1):
    __pPl = gc.getPlayer({iPlayer})
    (__c, __iterOut) = __pPl.firstCity(False)
    __cNames = []
    while __c is not None:
        __cNames.append(__c.getName().encode("utf-8"))
        (__c, __iterOut) = __pPl.nextCity(__iterOut, False)

    print("\\n".join(__cNames))
'''.format(iPlayer=iPlayer)

        except ValueError:
            self.warn("First argument is no integer.")

        if d:
            # Avoid contamination with string 'load_module encodings.utf_8'
            self.send("p:"+"encodings.utf_8")

            result = str(self.send("p:"+d)).strip()
            if len(result) > 0:
                self.feedback("Cities of player {0}:".format(iPlayer))
                cNames = result.split("\n")
                cID = 0
                for cName in cNames:
                    self.feedback("{:3d} {}".format(cID, cName))
                    cID += 1
            else:
                self.warn("Player {0} has no city.".format(iPlayer))

    def do_list_units(self, arg):
        """List all units of a player.

        Usage: list_units {Player id}

        The id can be used in 'rename_unit'.
        """
        if len(arg) < 1:
            print(self.do_list_units.__doc__)
            return

        d = None
        try:
            args = arg.split(" ")
            iPlayer = int(args[0])
            d = '''\
if( gc.getMAX_CIV_PLAYERS() > {iPlayer} and {iPlayer} > -1):
    __pPl = gc.getPlayer({iPlayer})
    (__u, __iterOut) = __pPl.firstUnit(False)
    __uNames = []
    while __u is not None:
        if  __u.plot().isCity():
            __pos = __u.plot().getPlotCity().getName().encode("utf-8")
        else:
            __pos = "(%i,%i)" % (__u.plot().getX(),__u.plot().getY())
        __uNames.append("%3i %-30s %s" % (
          __u.getID(),
          __u.getName().encode("utf-8"),
          __pos)
          )
        (__u, __iterOut) = __pPl.nextUnit(__iterOut, False)

    print("\\n".join(__uNames))
'''.format(iPlayer=iPlayer)

        except ValueError:
            self.warn("First argument is no integer.")

        if d:
            # Avoid contamination with string 'load_module encodings.utf_8'
            self.send("p:"+"encodings.utf_8")

            result = str(self.send("p:"+d)).strip()
            if len(result) > 0:
                self.feedback("Units of player {0}:".format(iPlayer))
                uNames = result.split("\n")
                for uName in uNames:
                    self.feedback(uName)
            else:
                self.warn("Player {0} has no units?!".format(iPlayer))

    def do_rename_player(self, arg):
        """Allows renaming with respect to some Non-ASCII characters (cp1252 encoding).

        Usage rename_player {Player id} {New name}

        Note that Civ4's functions .setName(...) and .getName() are tricky because
        the return values are from type unicode.
        Crash: print(pPlayer.getName())
           Ok: print(pPlayer.getName.encode('utf-8'))
        """

        if len(arg) < 2:
            print(self.do_rename_player.__doc__)
            return

        d = None
        try:
            args = arg.split(" ")
            iPlayer = int(args[0])
            sName = " ".join(args[1:])
            sName.replace('"', " ")
            d = '''\
if( gc.getMAX_CIV_PLAYERS() > {iPlayer} and {iPlayer} > -1):
    __name = """{sName}"""
    if gc.getPlayer({iPlayer}).setName(__name.decode("utf-8")) is None:
        print("0")
    else:
        print("-1")
else:
    print("-2")
'''.format(iPlayer=iPlayer, sName=sName)

        except ValueError:
            self.warn("First input argument is no integer.")

        if d:
            result = str(self.send("p:"+d)).strip()
            # Note: Possible return value is 'load_module encodings.utf_8\n0'
            if result.endswith("0"):
                self.feedback("Renaming of player {0} successful.".format(iPlayer))
            else:
                self.warn("Renaming of player {0} failed. Server returns '{1}'".format(iPlayer, result))

    def do_rename_city(self, arg):
        """Allows renaming with respect to some Non-ASCII characters (cp1252 encoding).

        Usage rename_city {Player id} {City id} {New name}

        Fetch the city id with list_cities.
        """

        if len(arg) < 3:
            print(self.do_rename_city.__doc__)
            return

        d = None
        try:
            args = arg.split(" ")
            iPlayer = int(args[0])
            iCity = int(args[1])
            sName = " ".join(args[2:])
            sName.replace('"', " ")
            d = '''\
if( gc.getMAX_CIV_PLAYERS() > {iPlayer} and {iPlayer} > -1):
    __name = """{sName}"""
    __iCity = int("{iCity}")
    __pPl = gc.getPlayer({iPlayer})
    (__c, __iterOut) = __pPl.firstCity(False)
    while __iCity > 0:
        __iCity -= 1
        (__c, __iterOut) = __pPl.nextCity(__iterOut, False)

    if __c and __c.setName(__name.decode("utf-8"), False) is None:
        print("0")
    else:
        print("-1")
else:
    print("-2")
'''.format(iPlayer=iPlayer, iCity=iCity, sName=sName)

        except ValueError:
            self.warn("First or second argument is no integer.")

        if d:
            result = str(self.send("p:"+d)).strip()
            # Note: Possible return value is 'load_module encodings.utf_8\n0'
            if result.endswith("0"):
                self.feedback("Renaming of city {0} successful.".format(iCity))
            else:
                self.warn("Renaming of city {0} failed. Server returns '{1}'".format(iCity, result))

    def do_rename_unit(self, arg):
        """Allows renaming with respect to some Non-ASCII characters (cp1252 encoding).

        Usage rename_unit {Player id} {Unit id} {New name}

        Fetch the unit id with list_units.
        """

        if len(arg) < 3:
            print(self.do_rename_unit.__doc__)
            return

        d = None
        try:
            args = arg.split(" ")
            iPlayer = int(args[0])
            iUnit = int(args[1])
            sName = " ".join(args[2:])
            sName.replace('"', " ")
            d = '''\
if( gc.getMAX_CIV_PLAYERS() > {iPlayer} and {iPlayer} > -1):
    __name = """{sName}"""
    __unit = gc.getPlayer({iPlayer}).getUnit({eID})
    if not __unit.isNone() and __unit.setName(__name.decode("utf-8")) is None:
        print("0")
    else:
        print("-1")
else:
    print("-2")
'''.format(iPlayer=iPlayer, eID=iUnit, sName=sName)

        except ValueError:
            self.warn("First or second argument is no integer.")

        if d:
            result = str(self.send("p:"+d)).strip()
            # Note: Possible return value is 'load_module encodings.utf_8\n0'
            if result.endswith("0"):
                self.feedback("Renaming of unit {0} successful.".format(iUnit))
            else:
                self.warn("Renaming of unit {0} failed. Server returns '{1}'".format(iUnit, result))

    def do_enable_dark_mode(self, arg):
        """ Swap used colors used by Pyconsole

            Useful for better readability in dark terminals.
            Format: enable_dark_mode [0|1]
        """
        if len(arg) > 0:
            try:
                self.term_background_dark = bool(int(arg))
            except ValueError:
                self.warn("Input no bool.")
        else:
            self.term_background_dark = not self.term_background_dark

        self.setColors(self.term_background_dark)

    def do_enable_expression_print(self, arg):
        """ Enable output printing of expressions.

            Format: enable_expression_print [0|1]
        """
        if len(arg) > 0:
            try:
                self.automatic_print = bool(int(arg))
            except ValueError:
                self.warn("Input no bool.")
        else:
            self.automatic_print = not self.automatic_print

    def do_unreveal(self, arg):
        """Hide plots outside of view ranges."""
        d = '''\
__counter = 0
for __iPl in xrange(CyMap().numPlots()):
    __p = CyMap().plotByIndex(__iPl)
    for __iP in xrange(gc.getMAX_CIV_PLAYERS()-1):
        if __p.isRevealed(__iP, False) and __p.getVisibilityCount(__iP) == 0:
            __counter += 1
            __p.setRevealed(__iP, False, False, -1)

print(__counter)
'''
        result = str(self.send("p:"+d)).strip()
        print("Number of affected plots: '{}'".format(result))

    def verbose(self, line, print_input_line=True):
        """Print line and then send it as python command"""
        if print_input_line:
            print(line)

        self.default(line)

    def default(self, line):
        """Send input as python command"""
        if self.automatic_print:
            # Escape \, " and '
            line = line.replace('\\', '\\\\')
            line = line.replace("'", r"\'").replace('"', r'\"')
            # Wrap by expression detection
            line = '''
try:
    __to_print = eval('{0}')
    print(__to_print)
except SyntaxError:
    exec('{0}')
'''.format(line)

        result = str(self.send("P:" + line))
        self.feedback(result)

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
            self.warn("Can not compile regular expression.")
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
            self.warn("No Civ4 function/class/etc found for %s" % (kname,))
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
        except Exception as e:
            self.warn("Sending of '{}' failed. Error: {}"
                      "".format(s,e))

        return ""

    def config_edit(self, conf_key, new_value, settings):
        template_edit1 = "PbSettings['%s'] = %s('%s');"
        template_edit2 = "PbSettings['%s']['%s'] = %s('%s');"
        template_del1 = "PbSettings.pop('%s');"
        template_del2 = "PbSettings['%s'].pop('%s');"

        changes = []
        for (k, v) in settings.items():
            if isinstance(v, dict):
                if len(conf_key) > 1 and conf_key[0] != k:
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


    def getPbSettings(self):
        d = "import simplejson as json; print(" \
                "json.dumps(PbSettings, encoding='{}'))".format(ENCODING2)
        result = str(self.send("p:"+d))
        # print(result)
        # Strip unwanted output (reason?!)
        if result:
            result = result[result.find("{"):result.rfind("}")+1]

        # print(result)
        try:
            settings = json.loads(result, encoding=ENCODING2)
        except ValueError:
            print("Can not decode settings")
            settings = {}

        return settings

    def getPbSaves(self, pattern="*", regPattern=None, sOptNum=-1):
        if not regPattern:
            regPattern = ".*"
        d = """\
import simplejson as json
print(json.dumps({0}'saves':PbSettings.getListOfSaves('{2}','{3}', {4}){1},
encoding='{5}'))""".format("{", "}", pattern, regPattern, sOptNum, ENCODING2)

        # print(d)
        result = str(self.send("p:"+d))
        if result:
            json_str = result[result.find("{"):result.rfind("}")+1]

            try:
                saves = json.loads(json_str, encoding=ENCODING2)
                return saves.get("saves", [])
            except ValueError:
                self.warn("Can not decode list of saves.")
                self.warn(result)

        return []

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
        shell.warn("Can't read history file")

    # Load help system in background thread
    # doc_thread = Thread(target=load_civ4_library)
    # doc_thread.start()

    # Start Input loop
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        shell.warn("Ctrl+C pressed. Quitting Civ4 shell.")
        shell.close()
    except TypeError:
        shell.warn("Type error. Quitting Civ4 shell.")
        shell.close()
    finally:
        shell.close()

    # Write history
    try:
        readline.set_history_length(100000)
        readline.write_history_file(".pyconsole.history")
    except IOError:
        shell.warn("Can't write history file")

if __name__ == '__main__':
    print("Use 'python Pyconsole [port]' in above folder for start")
    # start()
