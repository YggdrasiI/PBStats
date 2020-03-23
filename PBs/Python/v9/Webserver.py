# -*- coding: utf-8 -*-
from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys
import re
import cgi
import os
import os.path
# import os.listdir
import cStringIO
import glob
import time
import thread
from threading import Timer, Thread, Event
import urllib
# import hashlib # Python 2.4 has no hashlib use md5
import md5
import simplejson

from CvPythonExtensions import *
import CvPythonExtensions as E
import CvUtil
import CvEventInterface

# For WB Saves
import CvWBDesc
# import CvWBInterface
# import zlib # not included
# import gzip # exists in Civ4/Assets/Python/System, but can not be imported

PB = E.CyPitboss()
gc = E.CyGlobalContext()
LT = E.CyTranslator()

# Add Altroot python folder as import path
pythonDir = os.path.join(gc.getAltrootDir(), '..', 'Python', 'v9')
if pythonDir not in sys.path:
    sys.path.append(pythonDir)
from Settings import Settings
import FindHash
from WebserverActions import Action_Handlers, createGameData \
        , gen_answer \
        #, getListOfSaves, getSaveFolder


PbSettings = Settings() #.instance()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """The do_POST method of this class handle the control commands
    of the webinterface
    """

    def log_message(self, _format, *args):
        "Redefine is ness. to omit python error popups!!"
        return

    def check_password(self, input_pw):
        if input_pw == PbSettings['webserver']['password']:
            return True

        # The old webinterface does not store the original password
        # and could only send it's hashed value.
        hashed_pw = md5.new(PbSettings['webserver']['password']).hexdigest()
        if input_pw == hashed_pw:
            return True
        return False

    def do_POST(self):
        if re.search('/api/v1/', self.path) != None:
            ctype, _ = cgi.parse_header(
                self.headers.getheader('content-type'))
            # ctype = self.headers.getheader('content-type').strip(" \n\r\t")
            if ctype == 'application/json':
                self.send_response(200)
                self.end_headers()

                try:
                    length = int(self.headers.getheader('content-length'))
                    rawdata = self.rfile.read(length)

                    parseddata = cgi.parse_qs(rawdata, keep_blank_values=1)
                    inputdata = dict(simplejson.loads(
                        parseddata.keys()[0], encoding='utf-8'))
                    # PB.consoleOut(str(inputdata))

                    if self.check_password(inputdata.get("password", "")):
                        action = inputdata.get("action")

                        if action in Action_Handlers:
                            Action_Handlers[action](
                                inputdata, self.server, self.wfile)
                        else:
                            action_unknown(Action_Handlers,
                                           inputdata, self.server, self.wfile)
                    else:
                        self.wfile.write(gen_answer(
                            {'return': 'fail',
                             'info': 'Wrong password.'}))

                except Exception, e:  # Old Python 2.4 syntax!
                    try:
                        errInfo = str(e)
                        # exc_type, exc_obj, exc_tb = sys.exc_info()
                        # errInfo += " Linenumber: " + str(exc_tb.tb_lineno)
                        self.wfile.write(simplejson.dumps(
                            {'return': 'fail',
                             'info': "Exception: " + errInfo}) + "\n")
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
                except Exception:
                    pass

        else:
            try:
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
            except Exception:
                pass
        return

    def do_GET(self):
        """Server has no get functionality."""
        if re.search('/api/v1/somepage/*', self.path) != None:
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
    # allow_reuse_address = True
    allow_reuse_address = 1

    def __init__(self, *args, **kwargs):
        # super(ThreadedHTTPServer, self).__init__(args, kwargs)  # super-on-old-class
        HTTPServer.__init__(self, *args, **kwargs)
        self.oldGamestate = {}
        self.adminApp = None
        self.adminFrame = None  # Required in some functions in WebserverActions.py
        # Mutex for write operation, i.e. (WB)Saves
        self.lock = thread.allocate_lock()

    def shutdown(self):
        self.socket.close()
        self.server_close()
        # In Python 2.4 the method 'shutdown' does not exists.
        # But we set the Deamon flag to true, thus it should shutdown.
        # HTTPServer.shutdown(self)

    def setPbApp(self, adminApp):
        self.adminApp = adminApp               # class AdminIFace(wx.App)
        self.adminFrame = adminApp.adminFrame  # class AdminFrame(wx.Frame)

        # Setup some extra Values in the DLL
        shortnames = PbSettings.setdefault(
            "shortnames", {"enable": True, "maxLenName": 1, "maxLenDesc": 4})

        bShortNames = bool(shortnames["enable"])
        iMaxLenName = int(shortnames["maxLenName"])
        iMaxLenDesc = int(shortnames["maxLenDesc"])
        if hasattr(gc.getGame(), "setPitbossShortNames"):
            gc.getGame().setPitbossShortNames(bShortNames,
                                              iMaxLenName, iMaxLenDesc)

    # Cache value because the evaluation is an expensive operation
    wbsaveCache = None

    def createWBSave(self, bCache=True, bCompress=False):
        self.lock.acquire()

        # Reset cache for new rounds
        if self.wbsaveCache is not None and self.wbsaveCache.get("turn", -1) != PB.getGameturn():
            self.wbsaveCache = None

        if self.wbsaveCache is None or bCache is False:
            self.wbsaveCache = {"turn": PB.getGameturn()}

            f = cStringIO.StringIO()
            version = 11
            f.write("Version=%d\n" % (version,))
            CvWBDesc.CvGameDesc().write(f)
            for i in range(gc.getMAX_TEAMS()):
                CvWBDesc.CvTeamDesc().write(f, i)  # write team info

            for i in range(gc.getMAX_PLAYERS()):
                CvWBDesc.CvPlayerDesc().write(f, i)  # write player info

            CvWBDesc.CvMapDesc().write(f)
            f.write("\n# # # Plot Info # # # \n")
            iGridW = E.CyMap().getGridWidth()
            iGridH = E.CyMap().getGridHeight()
            for iX in range(iGridW):
                for iY in range(iGridH):
                    plot = E.CyMap().plot(iX, iY)
                    pDesc = CvWBDesc.CvPlotDesc()
                    if pDesc.needToWritePlot(plot):
                        pDesc.write(f, plot)
            # Signs should be private
            """
            f.write("\n# # # Sign Info # # # \n")
            iNumSigns = E.CyEngine().getNumSigns()
            for i in range(iNumSigns):
                sign = E.CyEngine().getSignByIndex(i)
                pDesc = CvSignDesc()
                pDesc.write(f, sign)
            """

            wbsave = f.getvalue()
            self.wbsaveCache["raw"] = wbsave.decode(
                'ascii',
                'replace')  # required for umlauts
            f.close()

        if bCompress and "zip" not in self.wbsaveCache:
            # self.wbsaveCache["zip"] = zlib.compress(self.wbsaveCache.get("raw","No WB data cached."))
            """
            zf = cStringIO.StringIO()
            z = GzipFile(None, 'w', 9, zf)
            z.write( self.wbsaveCache.get("raw","No WB data cached.") )
            self.wbsaveCache["zip"] = z.read()
            zf.close()
            """

            import tempfile
            prefix = "%s_R%i" % (PB.getGamename(), PB.getGameturn())
            f = tempfile.NamedTemporaryFile(
                suffix='.CivBeyondSwordWBSave', prefix=prefix)
            f.write(self.wbsaveCache.get("raw", "No WB data cached."))
            f.flush()
            #f.seek(0) # return to beginning of file
            #print f.read() # reads data back from the file
            # Call of external zip command
            f.close() # temporary file is automatically deleted here

            self.wbsaveCache["zip"] = self.wbsaveCache.get(
                "raw", "No WB data cached.")

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

    def compareGamedata(self, new, old=None):
        if old is None:
            old = self.oldGamestate
        # Remove volatile keys
        old.pop("turnTimerValue", None)
        ttvNew = new.pop("turnTimerValue", None)

        # Compare dicts without volatile keys
        bSame = (old == new)
        if ttvNew is not None:
            new["turnTimerValue"] = ttvNew

        # Cache new value as old for next call
        self.oldGamestate = new
        return bSame

    """
    def savePbSettings(self):
        self.lock.acquire()
        # Call non-member function
        savePbSettings()
        self.lock.release()
    """


class PerpetualTimer:
    """Class to invoke request from to the 'client' side of webinterface.

    If reduceTraffic flag is set, only changed game states will be send.
    Moreover, every self.reduceFactor times an alive message will be send
    to respect some offline detection mechanism of the webinterface.
    """

    def __init__(self, settings, webserver, reduceTraffic=False):
        self.settings = settings
        self.t = settings['sendInterval']
        self.tFirst = self.t + 10
        self.reduceTraffic = reduceTraffic
        self.reduceFactor = 12
        self.requestCounter = 0
        self.webserver = webserver
        self.threadMain = None  # Waits 'tStart' seconds
        self.timer = None  # periodical timer with 't' seconds
        self.url = ""
        self.gameId = -1
        self.pwHash = ""

    def update_connection_vars(self):
        self.url = self.settings["url"]
        self.gameId = self.settings["gameId"]
        self.pwHash = md5.new(PbSettings['webserver']['password']).hexdigest()

    def main(self):
        # Invoked after tFirst
        self.request(self.webserver)

        # loop over (second) timer and wait by joining.
        # (Starting this timer again in this thread, but not the timed one
        # avoids maximal recursion issues.
        #
        # Edit I do not see any avantages over a simple time.sleep here?!
        while self.threadMain:
            self.timer = Timer(self.t, self.handle_function)
            self.timer.start()
            self.timer.join()


    def handle_function(self):
        self.request(self.webserver)

    def start(self):
        if self.threadMain:
            return  # Already active...

        self.update_connection_vars()
        self.threadMain = Timer(self.tFirst, self.main) # To unblock
        # self.threadMain.start()
        self.threadMain.start()

    def cancel(self):
        # Falscher Thread zum canceln?!
        #if self.timer:
        #    self.timer.cancel()

        if self.threadMain:
            self.threadMain.cancel()
            self.threadMain = None

    def request(self, webserver):
        gamedata = createGameData()
        newState = not webserver.compareGamedata(gamedata)

        # Check if CvGame::doTurn is currently running.
        # Try ness for mods without the DLL changes for bGameTurnProcessing
        inconsistentState = False
        try:
            inconsistentState = CvEventInterface.getEventManager(
            ).bGameTurnProcessing
        except AttributeError:
            for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
                if gc.getPlayer(iPlayer).isTurnActive():
                    inconsistentState = True
                    break
        except:
            pass

        # PB.consoleOut("Webupload request %i" % (self.requestCounter,))
        self.requestCounter += 1

        if (not inconsistentState
                and (newState or not self.reduceTraffic or
                     self.requestCounter % self.reduceFactor == 0)
           ):
            params = urllib.urlencode(
                {'action': 'update', 'id': self.gameId,
                 'pwHash': self.pwHash, 'info':
                 simplejson.dumps(
                     {'return': 'ok', 'info': gamedata})})
        else:
            # Minimal alive message.
            gamedataMinimal = {"turnTimer": gamedata.get("turnTimer")}
            if gamedata["turnTimer"] == 1:
                gamedataMinimal["turnTimerValue"] = gamedata.get(
                    "turnTimerValue")
            params = urllib.urlencode(
                {'action': 'update', 'id': self.gameId, 'pwHash': self.pwHash, 'info':
                 simplejson.dumps(
                     {'return': 'ok', 'info': gamedataMinimal})})

        try:
            # f = urllib.urlopen("%s?%s" % (url,params) ) # GET method
            urllib.urlopen(self.url, params)  # POST method

        except:
            # PB.consoleOut("Webupload failed")
            pass


# =====================================================
'''
def getPbSettings():
    # TODO
    """Loads settings file and use default settings as fallback."""
    if len(PbSettings) > 0:
        return PbSettings

    PbSettings.load(True)

    # Convert old key names
    if "noGui" in PbSettings:
        # Old key overrides default key/new key
        PbSettings["gui"] = 1 - int(PbSettings["noGui"])
        del(PbSettings["noGui"])
        PbSettings.save()

    return PbSettings
'''



def searchMatchingPassword(filename, adminPwds=None):
    """ Return correct password of given list for a savegame.
    filename - The save
    adminPwds - List of passwords which md5 sum should compared

    return: Password ("" if save not password protected) or None
    """
    hSave = FindHash.get_admin_hash(filename, "")
    if hSave is None:
        sys.stderr.write("(searchMatchingPassword) failed. Can not detect admin hash value. " +
                         "Filepath correct?")
        return None
    if hSave == "":
        return ""

    if adminPwds is None:
        return None

    for adminPwd in adminPwds:
        if hSave == md5.new(adminPwd).hexdigest():
            return adminPwd

    return None


def isLoadableSave(filename, folderIndex=0, pwdCandidates=None):
    """Check if filename can be resolved into loadable
    path and test if one of the given passwords match.

    If filename already contains the full path use
    folderIndex = -1.

    Return 0 on succes, -1 if file not be found,
      and -2 if no password match.
    """
    filepath = None

    if folderIndex == -1:
        if os.path.isfile(filename):
            filepath = filename
    else:
        folderpaths = PbSettings.getPossibleSaveFolders()
        try:
            folderpaths.insert(0, folderpaths[folderIndex])
        except IndexError:
            pass

        for fp in folderpaths:
            tmpFilePath = os.path.join(fp[0], filename)
            # Convert into unicode because otherwise files
            # with umlaut/etc aren't found
            tmpFilePath = tmpFilePath.decode('utf-8')
            if os.path.isfile(tmpFilePath):
                filepath = tmpFilePath
                break

    if filepath is None:
        iResult = -1
    else:
        matchingPwd = searchMatchingPassword(filepath, pwdCandidates)
        if matchingPwd is None:
            iResult = -2
        else:
            iResult = 0

    return iResult
