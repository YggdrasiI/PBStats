from CvPythonExtensions import *
import CvUtil
import CvEventInterface

#  For WB Saves
#  import StringIO
import cStringIO
import CvWBDesc
#  import CvWBInterface
# import zlib #  not included
# import gzip #  exists in Civ4/Assets/Python/System, but can not be imported

from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
import cgi
import os.path
#  import os.listdir
import os
import glob
import time
import thread
from threading import Timer, Thread, Event
import urllib
# import hashlib #  Python 2.4 has no hashlib use md5
import md5
import simplejson
import sys

PB = CyPitboss()
gc = CyGlobalContext()
localText = CyTranslator()

#Default settings. Does not work for multiple PB instances due port collision.
pbDefaultSettings = {
    "webserver": {
        "host": "",  # Leave string empty
        #  Port of the python web interface of this mod. Use different port for
        #  each game
        "port": 13373,
        #  Password for admin commands on the webinterface
        "password": "defaultpassword"
    },
    "webfrontend": {
        #  Url of the pbStats file on your http webserver
        "url": "http://localhost/civ/page/update.php",
        "gameId": 0,  # Id of game at above website
        #  Set 0 to disable periodical sending of game data
        "sendPeriodicalData": 1,
        "sendInterval": 10,  # Seconds during automatic sending of game data
        },
    "save": {
        #  Filename (without path) of loaded game at startup (require autostart
        #  )
        "filename": "A.CivBeyondSwordSave",
        "adminpw": "",  # Admin password of above save
        "savefolder": "saves\\multi\\",  # First choice to save games.
        #  List of relative paths which can be used to load games.
        "readfolders": []
    },
    "shortnames": {  # Truncate names to fix login issue due packet drop
        "enable": True,
        #  Maximal Leader name length. Length of 1 force replacement with player
        #  Id, 0=A,1=B,...,51=z
        "maxLenName": 1,
        #  Maximal Nation name length. Length of 1 force replacement with player
        #  Id, 0=A,1=B,...,51=z
        "maxLenDesc": 4
    },
    #  Each login and logoff produce a save. This option controls the length of
    #  history
    "numRecoverySavesPerPlayer": 5,
    "MotD": "Welcome on the modified PitBoss Server",
    "noGui": 0,  # Do not show admin window. (This option force the autostart.)
    "autostart": 0,  # Load savegame at startup
    "errorLogFile": None
}
pbSettings = None

#  Try to load pbSettings file.
#  To get a different settings file for each pitboss we need
#  access to a variable in the ini file
#  We reuse a widely unused variable of the standard BTS ini file
altrootDir = gc.getAltrootDir()

#  Cut of badly formated beginning of String [...]@ (If EMail Ini variable used)
#  altrootDir = altrootDir[altrootDir.rfind("@")+1:len(altrootDir)]

#  If the loading of the setting file failed the path will be set no None
#  in getPbSettings()
pbFn = os.path.join(altrootDir, "pbSettings.json")


def getPbSettings():
    global altrootDir
    global pbFn
    global pbSettings
    global pbDefaultSettings
    if pbSettings is not None:
        return pbSettings

    if os.path.isfile(pbFn):
        fp = file(pbFn, "r")
        pbSettings = simplejson.load(fp)
        fp.close()
        return pbSettings
    elif altrootDir != "":
        pbSettings = pbDefaultSettings
        savePbSettings()
        return pbSettings
    else:
        pbSettings = pbDefaultSettings
        pbFn = None
        return pbDefaultSettings

#  Attention: Use the ThreadedHTTPServer.savePbSettings to wrap this into a mutex if you saved the file over the webinterface.
#  This function should only be called direct if the webserver wasn't started.


def savePbSettings():
    global pbFn
    global pbSettings
    if pbFn is None:
        return

    try:
        fp = file(pbFn, "w")
        #  Note that it's ness. to use the old syntax (integer value) for indent
        #  argument!
        simplejson.dump(pbSettings, fp, indent=1)
    except Exception, e:
        pass

#  Use two default paths and the given path from the setting file
#  to generate possible paths of saves.
#  A hashmap construction would destroy the ordering and OrderedDict requires
#  at least Python 2.7. Thus, the duplicates free list will be constructed
#  by hand.


def getPossibleSaveFolders():
    global altrootDir
    if not "save" in pbSettings:
        pbSettings["save"] = {}

    #  Note: "path" is the deprecated name of "savefolder"
    userPath = str(
        pbSettings["save"].get(
            "savefolder",
            pbSettings["save"].get(
                "path",
                "saves\\multi\\")))
    folders = [
        altrootDir + "\\" + userPath,
        altrootDir + "\\" + userPath + "auto\\",
        altrootDir + "\\" + "saves\\multi\\",
        altrootDir + "\\" + "saves\\multi\\auto\\",
        altrootDir + "\\" + "saves\\pitboss\\",
        altrootDir + "\\" + "saves\\pitboss\\auto\\"
        ]

    #  Add extra folders
    for extraUserPath in pbSettings["save"].get("readfolders", []):
        folders.append(altrootDir + "\\" + str(extraUserPath))
        folders.append(altrootDir + "\\" + str(extraUserPath) + "auto\\")

    def remove_duplicates(li):
        my_set = set()
        res = []
        for e in li:
            if e not in my_set:
                res.append((e, len(res)))
                my_set.add(e)
        return res
    return remove_duplicates(folders)


#  The do_POTH method of this class handle the control commands
#  of the webinterface
class HTTPRequestHandler(BaseHTTPRequestHandler):

    #  Redefine is ness. to omit python error popups!!
    def log_message(self, format, *args):
        return

    def do_POST(self):
        if None != re.search('/api/v1/', self.path):
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            #  ctype = self.headers.getheader('content-type').strip(" \n\r\t")
            if ctype == 'application/json':
                self.send_response(200)
                self.end_headers()

                try:
                    length = int(self.headers.getheader('content-length'))
                    rawdata = self.rfile.read(length)

                    parseddata = cgi.parse_qs(rawdata, keep_blank_values=1)
                    inputdata = simplejson.loads(parseddata.keys()[0])
                    """
                    parseddata = rawdata.split("&")
                    inputdata = simplejson.loads( parseddata[0] )
                    """

                    action = inputdata.get("action")

                    if(action == "chat" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        try:
                            msg = str(
                                inputdata.get(
                                    "msg",
                                    "Default message. Missing msg argument?!"))
                            msg = msg.replace('&', '&amp;')
                            msg = msg.replace('<', '&lt;')
                            msg = msg.replace('>', '&gt;')
                            PB.sendChat(msg)
                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'ok', 'info': 'Send: ' + msg}) +
                                "\n")
                        except:
                            self.wfile.write(
                                simplejson.dumps(
                                    {
                                        'return': 'fail',
                                        'info': 'Some error occured trying to send the message. Probably a character that cannot be encoded.'}) +
                                "\n")

                    elif(action == "setAutostart" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        self.server.lock.acquire()
                        pbSettings["autostart"] = int(
                            inputdata.get(
                                "value",
                                0))
                        self.server.lock.release()
                        self.server.savePbSettings()
                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'info': 'Autostart flag: ' +
                                 str(pbSettings["autostart"])}) + "\n")

                    elif(action == "setHeadless" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        self.server.lock.acquire()
                        pbSettings["noGui"] = int(inputdata.get("value", 0))
                        self.server.lock.release()
                        self.server.savePbSettings()
                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'info': 'Headless/noGui flag: ' +
                                 str(pbSettings["noGui"])}) + "\n")

                    elif(action == "save" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        defaultFile = "Pitboss_" + PB.getGamedate(True)
                        filename = str(
                            inputdata.get(
                                "filename",
                                defaultFile)) + ".CivBeyondSwordSave"
                        #  remove "\ or /" chars to cut of directory changes
                        filename = filename[
                            max(filename.rfind("/"), filename.rfind("\\")) + 1:
                            len(filename)]

                        ret = self.server.createSave(filename)
                        self.wfile.write(simplejson.dumps(ret) + "\n")

                    elif(action == "setTurnTimer" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        iHours = int(inputdata.get("value", 24))
                        PB.turnTimerChanged(iHours)
                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'info': 'Set turn timer on ' +
                                 str(iHours) + ' hours.'}) + "\n")

                    elif(action == "setCurrentTurnTimer" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        iSeconds = int(inputdata.get("seconds", 0))
                        iMinutes = int(inputdata.get("minutes", 0))
                        iHours = int(inputdata.get("hours", 0))
                        iSeconds = iSeconds + 60*iMinutes + 3600*iHours
                        if iSeconds < 60:
                            iSeconds = 60
                        gc.getGame().incrementTurnTimer(-PB.getTurnTimeLeft() +
                                                        4 * iSeconds)
                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'info':
                                 'Set timer for current round.'}) + "\n")

                    elif(action == "setPause" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        bPause = int(inputdata.get("value", 0))
                        if bPause:
                            if not gc.getGame().isPaused():
                                PB.sendChat("(Webinterface) Activate pause.")
                                #gc.getGame().setPausePlayer(gc.getMAX_PLAYERS()-1)
                                gc.sendPause(0)
                                # Note that babarian player index would
                                # be nice, but leads to an error... just use index 0...
                                #gc.sendPause(gc.getMAX_CIV_PLAYERS()-1)
                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'ok', 'info': 'Activate pause.'}) +
                                "\n")
                        else:
                            if gc.getGame().isPaused():
                                PB.sendChat("(Webinterface) Deactivate pause.")
                                # This removes the pause only locally.
                                gc.getGame().setPausePlayer(-1)
                                # This crashs on Linux/Wine
                                #gc.sendPause(-1)
                                # Workaround sends chat message
                                gc.sendChat("RemovePause", ChatTargetTypes.CHATTARGET_ALL)
                            self.wfile.write(
                                simplejson.dumps({'return': 'ok', 'info': 'Deactivate pause.'}) + "\n")

                    elif(action == "endTurn" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        #  Create Backup save in auto-Folder
                        filename = r"Auto_" + \
                            PB.getGamename() + r"_R" + str(PB.getGameturn()) + r"end_" + PB.getGamedate(False) + r".CivBeyondSwordSave"
                        self.server.createSave(str(filename), 1)

                        if(PB.getTurnTimer()):
                            gc.getGame().incrementTurnTimer(-
                                                            PB.getTurnTimeLeft() +
                                                            4 *
                                                            20)
                            msg = 'Set timer on a few seconds.'
                        else:
                            #  This variant made trouble with automated units
                            #  and KI?!
                            messageControl = CyMessageControl()
                            messageControl.sendTurnCompleteAll()
                            msg = 'End turn'

                        self.wfile.write(
                            simplejson.dumps({'return': 'ok', 'info': msg}) +
                            "\n")

                    elif(action == "restart" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        #  Save current game and reload this save if no expicit
                        #  filename is given
                        bReload = True

                        filename = str(inputdata.get("filename", ""))
                        folderIndex = int(inputdata.get("folderIndex", 0))
                        #  remove "\ or /" chars to cut of directory changes
                        filename = filename[
                            max(filename.rfind("/"), filename.rfind("\\")) + 1:
                            len(filename)]

                        #  Use first folder if no filename is given
                        if len(filename) == 0:
                            folderIndex = 0

                        if len(filename) > 0:
                            #  Save selected filename for reloading in the
                            #  settings file
                            filename = filename + ".CivBeyondSwordSave"
                            filename = filename.replace(
                                "CivBeyondSwordSave.CivBeyondSwordSave",
                                "CivBeyondSwordSave")
                            #  Now, checks if file can be found. Otherwise abort because
                            #  loading of missing files let crash the pb server
                            #  and grab 100% of cpu.
                            folderpaths = getPossibleSaveFolders()
                            try:
                                folderpaths.insert(0, folderpaths[folderIndex])
                            except IndexError:
                                pass

                            folderIndexFound = -1
                            for fp in folderpaths:
                                tmpFilePath = os.path.join(fp[0], filename)
                                if os.path.isfile(tmpFilePath):
                                    folderIndexFound = fp[1]
                                    break

                            if folderIndexFound == -1:
                                #  No save game with this filename found. Abort
                                #  reloading
                                bReload = False
                                self.wfile.write(
                                    simplejson.dumps(
                                        {
                                            'return': 'fail',
                                            'info': 'Reloading failed. Can not detect path of save "' +
                                            filename +
                                            '".'}) +
                                    "\n")
                            else:
                                self.server.lock.acquire()
                                pbSettings["save"]["filename"] = filename
                                pbSettings["save"][
                                    "folderIndex"] = folderIndexFound
                                pbSettings["save"]["oneOffAutostart"] = 1
                                self.server.lock.release()
                                self.server.savePbSettings()

                        else:
                            self.server.lock.acquire()
                            pbSettings["save"]["oneOffAutostart"] = 1
                            self.server.lock.release()
                            filename = "Reload.CivBeyondSwordSave"
                            ret = self.server.createSave(filename)
                            if ret["return"] != "ok":
                                bReload = False
                                self.wfile.write(simplejson.dumps(
                                    {'return': 'fail', 'info': 'Reloading failed. Was not able to save game.'}) + "\n")

                        if bReload:
                            #  Quit server. The loop in the batch file should
                            #  restart the server....
                            if self.server.adminWindow is not None:
                                self.wfile.write(
                                    simplejson.dumps(
                                        {'return': 'ok', 'info':
                                         'Set loaded file on "' + filename +
                                         '" and quit PB server window.'}) + "\n")
                                self.server.adminWindow.OnExit(None)
                            else:
                                self.wfile.write(
                                    simplejson.dumps(
                                        {
                                            'return': 'fail',
                                            'info': 'Reloading failed. Was not able to quit PB server window.'}) +
                                    "\n")

                    elif(action == "setPlayerPassword" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        playerId = int(inputdata.get("playerId", -1))
                        newCivPW = str(inputdata.get("newCivPW", r""))
                        ret = -1
                        if playerId > -1:
                                #  Well, the hashing should be done in the DLL, but I forgot this call
                                #  and will not change the DLL in this version of the mod.
                                #  TODO: Move this line into the DLL for newer
                                #  versions of the mod.
                            adminPW = str(
                                pbSettings.get(
                                    "save",
                                    {}).get(
                                    "adminpw",
                                    ""))
                            if len(adminPW) > 0:
                                adminPWHash = md5.new(adminPW).hexdigest()
                            else:
                                adminPWHash = ""
                            ret = gc.getGame().setCivPassword(
                                playerId,
                                newCivPW,
                                adminPWHash)

                        if ret == 0:
                            self.wfile.write(simplejson.dumps(
                                {'return': 'ok', 'info':
                                 'Passwort of player ' +
                                 str(playerId) + ' changed to "' +
                                 newCivPW + '"'}) + "\n")
                        else:
                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'fail', 'info':
                                     'Passwort change failed.'}) + "\n")

                    elif(action == "setPlayerColor" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        playerId = int(inputdata.get("playerId", -1))
                        colorId = int(inputdata.get("colorId", -1))
                        ret = -1
                        if playerId > -1 and colorId > -1:
                            gc.getPlayer(playerId).setPlayerColor(colorId)
                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'ok', 'info':
                                     'Player color of player ' + str(playerId) +
                                     ' changed to "' + str(colorId) + '"'}) + "\n")
                        else:
                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'fail', 'info':
                                     'Player color change failed.'}) + "\n")

                    elif(action == "getMotD" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        try:
                            motd = ""
                            if self.server.adminApp is not None:
                                motd = self.server.adminApp.getMotD()

                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'ok', 'info': 'Return MotD.', 'msg': motd}) + "\n")
                        except Exception, e:
                            self.wfile.write(
                                simplejson.dumps(
                                    {
                                        'return': 'fail',
                                        'info': 'Some error occured trying to get the MotD. Error msg:' +
                                        str(e)}) +
                                "\n")
                    elif(action == "getWBSave" and
                            inputdata.get("password") == pbSettings["webserver"]["password"] and
                            pbSettings["webserver"].get("allowWB", False)):
                        bCache = (inputdata.get("noCache", "0") == "0")
                        bCompress = (inputdata.get("compress", "0") == "1")
                        ret = self.server.createWBSave(bCache, bCompress)
                        self.wfile.write(simplejson.dumps(ret) + "\n")

                    elif(action == "getReplay" and pbSettings["webserver"].get("allowReplay", False)):
                        try:
                            replayInfo = gc.getGame().getReplayInfo()
                            if replayInfo.isNone():
                                replayInfo = CyReplayInfo()
                                #  (gc.getGame().getActivePlayer())
                                replayInfo.createInfo(-1)

                            iTurn = replayInfo.getInitialTurn()
                            i = 0
                            replayMessages = []
                            while (i < replayInfo.getNumReplayMessages()):
                                iPlayer = replayInfo.getReplayMessagePlayer(i)
                                iTurn = replayInfo.getReplayMessageTurn(i)
                                eMessageType = replayInfo.getReplayMessageType(
                                    i)
                                eColor = replayInfo.getReplayMessageColor(i)
                                colRgba = localText.changeTextColor("", eColor)
                                color = colRgba[7:colRgba.find(">")]
                                if eMessageType in [ReplayMessageTypes.REPLAY_MESSAGE_CITY_FOUNDED,
                                                    ReplayMessageTypes.REPLAY_MESSAGE_MAJOR_EVENT]:
                                #  Why does this not work?!
                                #  msgText = replayInfo.getReplayMessageText(i).decode('ascii', 'replace')
                                    msgText = replayInfo.getReplayMessageText(
                                        i)
                                    msgText = ''.join(
                                        i
                                        for i in
                                        msgText if ord(i) < 128)  # filtering
                                    replayMessages.append(
                                        {'id': i, 'turn': iTurn, 'player':
                                         iPlayer, 'color': color, 'text':
                                         msgText})
                                i += 1

                            #  Scores
                            #  iEnd = replayInfo.getReplayMessageTurn(i)
                            iEnd = replayInfo.getFinalTurn()
                            iStart = replayInfo.getInitialTurn()
                            playerScores = {}
                            for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
                                gcPlayer = gc.getPlayer(iPlayer)
                                if (gcPlayer.isEverAlive()):
                                    i = iStart
                                    score = []
                                    economy = []
                                    industry = []
                                    agriculture = []
                                    while (i <= iEnd):
                                        score.append(
                                            replayInfo.getPlayerScore(
                                                iPlayer,
                                                i))
                                        economy.append(
                                            replayInfo.getPlayerEconomy(
                                                iPlayer,
                                                i))
                                        industry.append(
                                            replayInfo.getPlayerIndustry(
                                                iPlayer,
                                                i))
                                        agriculture.append(
                                            replayInfo.getPlayerAgriculture(
                                                iPlayer,
                                                i))
                                        i += 1
                                    playerScores[iPlayer] = {
                                        'score': score,
                                        'economy': economy,
                                        'industry': industry,
                                        'agriculture': agriculture}

                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'ok', 'info':
                                     'Return subset of replay messages.', 'replay': replayMessages, 'graphs': playerScores}) +
                                "\n")
                        except Exception, e:
                            self.wfile.write(
                                simplejson.dumps(
                                    {
                                        'return': 'fail',
                                        'info': 'Some error occured trying to get the Replay. Error msg:' +
                                        str(e)}) +
                                "\n")

                    elif(action == "setMotD" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        try:
                            msg = str(
                                inputdata.get(
                                    "msg",
                                    "No MotD given. Missing msg argument?!"))
                            msg = msg.replace('&', '&amp;')
                            msg = msg.replace('<', '&lt;')
                            msg = msg.replace('>', '&gt;')
                            self.server.lock.acquire()
                            pbSettings["MotD"] = msg
                            self.server.lock.release()
                            self.server.savePbSettings()

                            if self.server.adminApp is not None:
                                self.server.adminApp.setMotD(msg)

                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'ok', 'info': 'New MotD: ' + msg}) +
                                "\n")
                        except Exception, e:
                            self.wfile.write(
                                simplejson.dumps(
                                    {
                                        'return': 'fail',
                                        'info': 'Some error occured trying to set the MotD. Probably a character that cannot be encoded. Error msg:' +
                                        str(e)}) +
                                "\n")

                    elif(action == "setShortNames" and inputdata.get("password") == pbSettings["webserver"]["password"]):
                        try:
                            bShortNames = bool(inputdata.get("enable", True))
                            iMaxLenName = int(inputdata.get("maxLenName", 1))
                            iMaxLenDesc = int(inputdata.get("maxLenDesc", 4))
                            self.server.lock.acquire()
                            pbSettings["shortnames"] = {
                                "enable": bShortNames,
                                "maxLenName": iMaxLenName,
                                "maxLenDesc": iMaxLenDesc}
                            self.server.lock.release()
                            self.server.savePbSettings()
                            gc.getGame().setPitbossShortNames(
                                bShortNames,
                                iMaxLenName,
                                iMaxLenDesc)

                            self.wfile.write(
                                simplejson.dumps(
                                    {'return': 'ok', 'info':
                                     'Short names enabled: ' + str(bShortNames) +
                                     ', Maximal length of Leadername: ' +
                                     str(iMaxLenName) +
                                     'Maximal length of Civ description: ' +
                                     str(iMaxLenDesc)}) + "\n")
                        except Exception, e:
                            self.wfile.write(
                                simplejson.dumps(
                                    {
                                        'return': 'fail',
                                        'info': 'Some error occured during change of short names-feature. Error msg:' +
                                        str(e)}) +
                                "\n")

                    elif(action == "info"):
                        gamedata = self.server.createGamedata()

                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'info': gamedata}) + "\n")

                    elif(action == "listSaves"):
                        #  Print list of saves of the selected folder. This can be used for a dropdown list
                        #  of available saves.
                        folderpaths = getPossibleSaveFolders()
                        saveList = []

                        for fp in folderpaths:
                            folderpath = fp[0]
                            for savefile in os.listdir(folderpath):
                                if savefile.endswith(".CivBeyondSwordSave"):
                                    timestamp = os.path.getctime(
                                        folderpath +
                                        savefile)
                                    saveList.append({
                                        'name': str(savefile),
                                        'folderIndex': fp[1],
                                        'date': time.ctime(timestamp),
                                        'timestamp': timestamp
                                        })

                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'list': saveList}) + "\n")

                    elif(action == "listPlayerColors"):
                        colorList = []
                        for c in range(gc.getNumPlayerColorInfos()):
                            playerColors = gc.getPlayerColorInfo(c)
                            col = localText.changeTextColor(
                                u"",
                                playerColors.getColorTypePrimary())
                            playerColor1 = col[7:col.find(">")]
                            col = localText.changeTextColor(
                                u"",
                                playerColors.getColorTypeSecondary())
                            playerColor2 = col[7:col.find(">")]
                            col = localText.changeTextColor(
                                u"",
                                playerColors.getTextColorType())
                            playerColor3 = col[7:col.find(">")]
                            colorList.append({
                                "primary": playerColor1,
                                "secondary": playerColor2,
                                "text": playerColor3,
                                "usedBy": []
                                })

                        for rowNum in range(gc.getMAX_CIV_PLAYERS()):
                            gcPlayer = gc.getPlayer(rowNum)
                            if (gcPlayer.isEverAlive()):
                                colorList[gcPlayer.getPlayerColor()]["usedBy"].append(
                                    {"id": rowNum, "name": gcPlayer.getName()})

                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'colors': colorList}) + "\n")

                    elif(action == "listSigns" and
                            inputdata.get("password") == pbSettings["webserver"]["password"] and
                            pbSettings["webserver"].get("allowSigns", False)):
                        engine = CyEngine()
                        signs = []
                        for i in range(engine.getNumSigns()-1, -1, -1):
                            pSign = engine.getSignByIndex(i)
                            sign = {
                                'plot': [
                                    pSign.getPlot().getX(),
                                    pSign.getPlot().getY()],
                                'id': pSign.getPlayerType(),
                                'caption': pSign.getCaption()}
                            signs.append(sign)
                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'info': signs}) + "\n")

                    elif(action == "cleanupSigns" and
                            inputdata.get("password") == pbSettings["webserver"]["password"] and
                            pbSettings["webserver"].get("allowSigns", False)):
                        # Debugging: Reset all Signs. Remove some special chars
                        engine = CyEngine()
                        signs = []
                        for i in range(engine.getNumSigns()-1, -1, -1):
                            pSign = engine.getSignByIndex(i)
                            sign = {
                                'plot': [
                                    pSign.getPlot().getX(),
                                    pSign.getPlot().getY()],
                                'id': pSign.getPlayerType(),
                                'caption': pSign.getCaption()}
                            signs.append(sign)
                            engine.removeSign(
                                pSign.getPlot(),
                                pSign.getPlayerType())

                        for sign in signs:
                            caption = sign['caption']
                            # caption = re.sub("[^A-z 0-9]","", caption) #  not enought
                            #  caption = sign['caption'].encode('ascii',
                            # 'ignore') #  does not help
                            caption = caption[0:18]  # shortening required
                            caption = ''.join(
                                i
                                for i in caption if ord(i) < 128)  # filtering required
                            sign['caption'] = caption
                            engine.addSign(
                                gc.getMap().plot(
                                    sign['plot'][0],
                                    sign['plot'][1]),
                                sign['id'],
                                caption.__str__())

                        self.wfile.write(
                            simplejson.dumps(
                                {'return': 'ok', 'info': signs}) + "\n")

                    else:
                        self.wfile.write(
                            simplejson.dumps(
                                {
                                    'return': 'fail',
                                    'info': 'Wrong password or unknown action. Available actions are info, chat, save, restart, listSaves, setAutostart, setHeadless, getMotD, setMotD, setShortNames, listPlayerColors, setPlayerColor, listSigns, cleanupSigns, getReplay, getWBSave. For security reasons the last four commands require the activation of some extra flags, see Webserver.py'}) +
                            "\n")

                except Exception, e:
                    try:
                        errInfo = str(e)
                        self.wfile.write(
                            simplejson.dumps({'return': 'fail', 'info': "Exception: " + errInfo}) + "\n")
                    except:
                        pass

            else:
                try:
                    data = {
                        "return": "fail",
                        "info": "Wrong content type. Assume JSON data."}
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(simplejson.dumps(data) + "\n")
                except Exception, e:
                    pass

        else:
            try:
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
            except Exception, e:
                pass
        return

    #  No get functionality
    def do_GET(self):
        if None != re.search('/api/v1/somepage/*', self.path):
            if True:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(
                    "Bitte weitergehen. Hier gibts nichts zu sehen.")
            else:
                self.send_response(400, 'Bad Request: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    oldGamestate = {}

    def shutdown(self):
        self.socket.close()
        self.server_close()
        #  In Python 2.4 the method 'shutdown' does not exists.
        #  But we set the Deamon flag to true, thus it should shutdown.
        #  HTTPServer.shutdown(self)

    def setPbApp(self, adminApp):
        self.adminApp = adminApp
        self.adminWindow = adminApp.adminFrame
        self.lock = thread.allocate_lock()
        #  Setup some extra Values in the DLL
        if "shortnames" not in pbSettings:
            pbSettings["shortnames"] = {
                "enable": True,
                "maxLenName": 1,
                "maxLenDesc": 4}
        shortnames = pbSettings.get("shortnames", {})

        bShortNames = bool(shortnames.get("enable", True))
        iMaxLenName = int(shortnames.get("maxLenName", 1))
        iMaxLenDesc = int(shortnames.get("maxLenDesc", 4))
        gc.getGame().setPitbossShortNames(
            bShortNames,
            iMaxLenName,
            iMaxLenDesc)

    #  Cache value because the evaluation is an expensive operation
    wbsaveCache = None

    def createWBSave(self, bCache=True, bCompress=False):
        self.lock.acquire()

        #  Reset cache for new rounds
        if self.wbsaveCache is not None and self.wbsaveCache.get("turn", -1) != PB.getGameturn():
            self.wbsaveCache = None

        if self.wbsaveCache is None or bCache == False:
            self.wbsaveCache = {"turn": PB.getGameturn()}
            #  f = file("/dev/shm/Test.WBSave", "w")
            f = cStringIO.StringIO()
            version = 11
            f.write("Version=%d\n" % (version,))

            CvWBDesc.CvGameDesc().write(f)
            for i in range(gc.getMAX_TEAMS()):
                CvWBDesc.CvTeamDesc().write(f, i)  # write team info

            for i in range(gc.getMAX_PLAYERS()):
                CvWBDesc.CvPlayerDesc().write(f, i)  # write player info

            CvWBDesc.CvMapDesc().write(f)
            f.write("\n#  #  #  Plot Info #  #  #  \n")
            iGridW = CyMap().getGridWidth()
            iGridH = CyMap().getGridHeight()
            for iX in range(iGridW):
                for iY in range(iGridH):
                    plot = CyMap().plot(iX, iY)
                    pDesc = CvWBDesc.CvPlotDesc()
                    if pDesc.needToWritePlot(plot):
                        pDesc.write(f, plot)
            #  Signs should be private
            """
            f.write("\n#  #  #  Sign Info #  #  #  \n")
            iNumSigns = CyEngine().getNumSigns()
            for i in range(iNumSigns):
                sign = CyEngine().getSignByIndex(i)
                pDesc = CvSignDesc()
                pDesc.write(f, sign)
            """

            wbsave = f.getvalue()
            self.wbsaveCache["raw"] = wbsave.decode(
                'ascii',
                'replace')  # required for umlauts
            f.close()

        if bCompress and "zip" not in self.wbsaveCache:
            #  self.wbsaveCache["zip"] = zlib.compress(self.wbsaveCache.get("raw","No WB data cached."))
            """
            zf = cStringIO.StringIO()
            z = GzipFile(None, 'w', 9, zf)
            z.write( self.wbsaveCache.get("raw","No WB data cached.") )
            self.wbsaveCache["zip"] = z.read()
            zf.close()
            """
            self.wbsaveCache["zip"] = self.wbsaveCache.get(
                "raw",
                "No WB data cached.")

        if bCompress:
            ret = {
                'return': 'ok',
                'info': 'Compressed WBSave returned.',
                'save': self.wbsaveCache["zip"]}
        else:
            ret = {
                'return': 'ok',
                'info': 'WBSave returned.',
                'save': self.wbsaveCache["raw"]}
        self.lock.release()
        return ret

    def createWBSaveDoNotWork(self, filename, folderIndex=0):
        filepath = os.path.join(self.getSaveFolder(folderIndex), filename)
        if (filepath != ""):
            self.lock.acquire()
            WBDesc = CvWBDesc.CvWBDesc()
            if 0 == WBDesc.write(filename):
                ret = {
                    'return': 'ok',
                    'info': 'File was saved in ' +
                    filepath +
                    '.',
                    'save': 'blub'}
            else:
                ret = {
                    'return': 'fail',
                    'info': 'Can not create WBSave ' +
                    filepath +
                    '.',
                    'save': ''}
        else:
            ret = {'return': 'fail', 'info': 'No filename.', 'save': ''}

            self.lock.release()
        return ret

    def createSave(self, filename, folderIndex=0):
        filepath = os.path.join(self.getSaveFolder(folderIndex), filename)

        if (filename != ""):
            self.lock.acquire()
            if (not PB.save(filepath)):
                ret = {
                    'return': 'fail',
                    'info': 'Saving of ' +
                    filepath +
                    ' failed.'}
                self.lock.release()
            else:
                #  Update last file name info and save json file
                pbSettings["save"]["filename"] = filename
                pbSettings["save"]["folderIndex"] = folderIndex
                self.lock.release()
                self.savePbSettings()
                ret = {
                    'return': 'ok',
                    'info': 'File was saved in ' +
                    filepath +
                    '.'}

        return ret

    def getSaveFolder(self, folderIndex=0):
        global altrootDir
        folderpaths = getPossibleSaveFolders()
        try:
            return folderpaths[folderIndex][0]
        except IndexError:
            return folderpaths[0][0]

    def createPlayerRecoverySave(self, playerId, playerName, bOnline):
        #  1. Check which saves already exists for this player
        #  and remove old recovery saves
        folder = self.getSaveFolder(1)
        RecoverPrefix = 'Logoff_'
        if bOnline:
            RecoverPrefix = 'Login_'

        #  Windows file names can not contain * characters. Replace the string "*Mod* ", which
        #  can prepend the player name.
        playerName = playerName.replace("*MOD* ", "MOD_").strip()

        existingRecoverySaves = glob.glob(
            folder +
            RecoverPrefix +
            'P' +
            str(playerId) +
            '_*.CivBeyondSwordSave')
        #  Add timestamp (as tuple)
        existingRecoverySavesWithTimestamps = map(
            lambda x: (
                x,
                os.path.getctime(x)),
            existingRecoverySaves)
        #  Sort by timestamp
        existingRecoverySavesWithTimestamps.sort(key=lambda xx: xx[1])
        #  Remove oldest
        while(len(existingRecoverySavesWithTimestamps) >= pbSettings.get("numRecoverySavesPerPlayer", 3)):
            old = existingRecoverySavesWithTimestamps.pop(0)
            os.remove(old[0])

        #  2. Save new recovery save
        filename = (RecoverPrefix +
                    'P' +
                    str(playerId) +
                    '_' +
                    playerName +
                    '_T' +
                    str(int(time.time())) +
                    '.CivBeyondSwordSave')
        self.createSave(str(filename), 1)

    def compareGamedata(self, new, old=None):
        if old is None:
            old = self.oldGamestate
        #  Remove volative keys
        ttvOld = old.pop("turnTimerValue", None)
        ttvNew = new.pop("turnTimerValue", None)
        bSame = (old == new)
        if ttvNew is not None:
            new["turnTimerValue"] = ttvNew

        #  cache new value
        self.oldGamestate = new
        return bSame

    def createGamedata(self):
        #  Collect all available data
        gamedata = {'gameTurn': PB.getGameturn(),
                    'gameName': PB.getGamename(),
                    'gameDate': PB.getGamedate(False),
                    'bPaused': gc.getGame().isPaused(),
                    'modName': PB.getModName(),
                    }

        if(PB.getTurnTimer()):
            gamedata["turnTimer"] = 1
            gamedata['turnTimerMax'] = gc.getGame().getPitbossTurnTime()
            gamedata['turnTimerValue'] = PB.getTurnTimeLeft()
        else:
            gamedata["turnTimer"] = 0

        players = []
        for rowNum in range(gc.getMAX_CIV_PLAYERS()):
            gcPlayer = gc.getPlayer(rowNum)
            if (gcPlayer.isEverAlive()):
                playerData = PB.getPlayerAdminData(rowNum)
                player = {'id': rowNum}
                player['finishedTurn'] = not playerData.bTurnActive
                player['name'] = gcPlayer.getName()
                player['score'] = playerData.getScore()
                player['ping'] = playerData.getPing()
                player['bHuman'] = playerData.bHuman
                player['bClaimed'] = playerData.bClaimed
                player['civilization'] = gcPlayer.getCivilizationDescription(0)
                player['leader'] = gc.getLeaderHeadInfo(
                    gcPlayer.getLeaderType()).getDescription()
                player['color'] = u"%d,%d,%d" % (
                    gcPlayer.getPlayerTextColorR(),
                    gcPlayer.getPlayerTextColorG(),
                    gcPlayer.getPlayerTextColorB())

                players.append(player)

        gamedata['players'] = players

        gamedata['bHeadless'] = pbSettings.get("noGui", 0)
        gamedata['bAutostart'] = pbSettings.get("autostart", 0)

        return gamedata

    def savePbSettings(self):
        self.lock.acquire()
        #  Call non-member function
        savePbSettings()
        self.lock.release()


#  Class to invoke request from to the 'client' side of webinterface
#  if reduceTraffic flag is set, only changed game states will be send
#  Moreover, every self.reduceFactor times an alive message will be send
#  to omit offline detection mechanisms of the webinterface.
class PerpetualTimer:

    def __init__(self, settings, webserver, reduceTraffic=False):
        self.settings = settings
        self.t = settings['sendInterval']
        self.tFirst = self.t + 10
        self.reduceTraffic = reduceTraffic
        self.reduceFactor = 12
        self.requestCounter = 0
        self.webserver = webserver
        self.hFunction = self.request
        self.thread = Timer(self.tFirst, self.handle_function)

    def handle_function(self):
        self.hFunction(self.webserver)
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

    def request(self, webserver):
        gamedata = webserver.createGamedata()
        newState = not webserver.compareGamedata(gamedata)

        #  Check if CvGame::doTurn is currently running.
        inconsistentState = CvEventInterface.getEventManager(
            ).bGameTurnProcessing

        url = self.settings["url"]
        gameId = self.settings["gameId"]
        pwHash = md5.new(pbSettings['webserver']['password']).hexdigest()

        self.requestCounter += 1

        if(not inconsistentState and (newState or not self.reduceTraffic
                                      or self.requestCounter % self.reduceFactor == 0)):
            params = urllib.urlencode(
                {'action': 'update', 'id': gameId,
                 'pwHash': pwHash, 'info':
                 simplejson.dumps(
                     {'return': 'ok', 'info': gamedata})})
        else:
            #  Minimal alive message.
            gamedataMinimal = {"turnTimer": gamedata.get("turnTimer")}
            if gamedata["turnTimer"] == 1:
                gamedataMinimal["turnTimerValue"] = gamedata.get(
                    "turnTimerValue")
            params = urllib.urlencode(
                {'action': 'update', 'id': gameId, 'pwHash': pwHash, 'info':
                 simplejson.dumps(
                     {'return': 'ok', 'info': gamedataMinimal})})

        try:
            # f = urllib.urlopen("%s?%s" % (url,params) ) #  GET method
            f = urllib.urlopen(url, params)  # POST method

        except:
            pass
