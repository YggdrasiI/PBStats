# -*- coding: utf-8 -*-

# import sys
import re
# import cgi
import os
import os.path
# import cStringIO
import glob
import time
import thread
# from threading import Timer, Thread, Event
# import urllib
# import md5
import simplejson

from CvPythonExtensions import *
# import CvUtil
# import CvEventInterface

# For WB Saves
# import CvWBDesc

PB = CyPitboss()
gc = CyGlobalContext()
LT = CyTranslator()

# The class Settings loads pbSettings.json into a dict, provide some
# thread save (write) operations on this data and holds a few more object
# references, required for PB server revlevant operations,
# i.e. the AdminFrame reference is required to shutdown the server.

# Civ4:BTS provides no way to get the altroot folder of the current instance,
# but... we need this string to
#   1. Store different setting files for each pitboss
#   2. Create distinct folders for the saves
#   3. Find the PB Server releated python files outside of the mods folder
#      (Normally it is [Altroot]\..\Python\[Mod version] )
#
# As workaround we reuse a widely unused variable of the standard BTS ini file
# to store the atroot path.
AltrootDir = gc.getAltrootDir()

# Path to settings file.
#
# If the loading of the setting file failed the path will be set no None
# in getPbSettings().
PbFn = os.path.join(AltrootDir, "pbSettings.json")

# Default settings.
# Using them for multiple PB instances leads to port collision.
PbDefaultSettings = {
    "webserver": {
        "host": "",  # Leave string empty
        # Port of the python web interface of this mod. Use different port for
        # each game
        "port": 13373,
        # Password for admin commands on the webinterface
        "password": "defaultpassword",
        # Enable generation of WB files over webinterface
        "allowWB": False,
        # Enable generation of replay information over webinterface
        "allowReplay": False,
        # To fetch list of all signs ofer webinterface
        "allowSigns": False,
    },
    "webfrontend": {
        # Url of the PBSpy/PBStats web interface to use
        # Use "http:\/\/civ.zulan.net\/pbspy\/update" for our instance of PBSpy
        "url": r"http://localhost/civ/page/update.php",
        "gameId": 0,  # Id of game at above website
        # Set 0 to disable periodical sending of game data
        "sendPeriodicalData": 1,
        "sendInterval": 10,  # Seconds during automatic sending of game data
        },
    "save": {
        # File (without path) to load game startup (if autostart is enabled)
        "filename": "A.CivBeyondSwordSave",
        "adminpw": "",  # Admin password of above save
        "writefolder": "Saves\\multi\\",  # First choice to save games.
        # List of relative paths which can be used to load games.
        # Useful to load saves of game 1 in second PB instance.
        "readfolders": []
    },
    "shortnames": {  # Truncate names to fix login issue due packet drop
        "enable": True,
        # Maximal Leader name length. Length of 1 force replacement with player
        # Id, 0=A,1=B,...,51=z
        "maxLenName": 1,
        # Maximal Nation name length. Length of 1 force replacement with player
        # Id, 0=A,1=B,...,51=z
        "maxLenDesc": 4,
    },
    "shell": {  # Local Tcp shell for debugging, etc
        "enable": False,
        # Attention, use of non-local ip is an
        # security risk.
        "ip": "127.0.0.1",
        "port": 3333,
    },
    # Each login and logoff produce a save. This option controls the length of
    # history
    "numRecoverySavesPerPlayer": 5,
    "MotD": "Welcome on the modified PitBoss Server",
    # "noGui": 0,  # Deprecated key
    "gui": 1,  # Show admin window. (Value 0 will ignored in some cases.)
    "autostart": 0,  # Load savegame at startup
    "errorLogFile": "Logs\\pitbossErr.log",  # Prevent mostly alert windows
    "tmpToRestart": False,  # To break restart loop in startPitboss.py
}

# Note: Python 2.4 does not support class decorators!
'''
class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.
    Source:
    https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
'''


# @Singleton
class Settings(dict):

    # Older Singleton approach
    # https://de.wikipedia.org/wiki/Liste_von_Singleton-Implementierungen#Ab_Python_Version_2.2
    def __new__(cls, *args):
        if '_instance' not in cls.__dict__:
            cls._instance = dict.__new__(cls)
        return cls._instance

    def __init__(self):
        if '_ready' not in dir(self):
            super(Settings, self).__init__()  # Removes lint waring
            # _pbSettings = {}
            # Holds values which should not be saved.
            self.temp = {}

            self.lock = thread.allocate_lock()
            self.load(True)
            self._ready = True

    """
    def __get__(self, obj, _type=None):
        return self._pbSettings.get(obj, _type)

    def __set__(self, obj, value):
        self._pbSettings.__set__(obj, value)

    def __delete__(self, obj):
        self._pbSettings.__delete__(obj)

    def setdefault(self, key, value):
        return self._pbSettings.setdefault(key, value)
    """

    """
    def __init__(self):  # , *args, **kwargs):
        # super(Settings, self).__init__(args, kwargs)
        super(Settings, self).__init__()  # Removes lint waring
        # _pbSettings = {}
        # Holds values which should not be saved.
        self.temp = {}
        self.lock = thread.allocate_lock()
        self.load(True)
    """

    def load(self, bFallbackToDefaults=False):
        if os.path.isfile(PbFn):
            fp = open(PbFn, "r")
            tmpSettings = dict(PbDefaultSettings)
            nested_dict_update(tmpSettings, simplejson.load(fp), 1)
            fp.close()
        elif bFallbackToDefaults:
            tmpSettings = dict(PbDefaultSettings)
            if AltrootDir != "":
                self.save()
            else:
                globals()["PbFn"] = None

        self.lock.acquire()
        self.clear()
        self.update(tmpSettings)
        self.lock.release()

    def getPbPasswords(self):
        """Loads list of alternative passwords for your games.
        Settings['save']['adminpw'] and this list will be tested
        as valid values before the game try to load the save.
        """

        pwdFile = os.path.join(AltrootDir, "..", "pbPasswords.json")
        passwords = []
        pw1 = self.get("save", {}).get("adminpw", "")
        if len(str(pw1)) > 0:
            passwords.append(pw1)

        if os.path.isfile(pwdFile):
            try:
                fp = open(pwdFile, "r")
                pbPasswords = dict(simplejson.load(fp))  # Wrap for Pylint
            finally:
                fp.close()
            passwords.extend(pbPasswords.get("adminPasswords", []))

        return passwords

    def save(self):
        """ Save the current state into pbSettings.json.

        Attention: Use the ThreadedHTTPServer.save to wrap this
        into a mutex if you saved the file over the webinterface.
        This function should only be called directly if the webserver
        wasn't started.
        """

        if PbFn is None:
            return

        self.lock.acquire()
        try:
            fp = open(PbFn, "w")
            # Note that it's ness. to use the old syntax (integer value)
            # for indent argument!
            simplejson.dump(self, fp, indent=1)
        except Exception:
            pass

        self.lock.release()

    def getPossibleSaveFolders(self):
        """Use two default values and the value(s) from the setting file
        to generate possible source paths of saves.

        The return value does not contain duplicates. There are two reasons
        why this was constructed by hand:
        A hashmap construction would destroy the ordering and OrderedDict
        requires at least Python 2.7.
        """
        if "save" not in self:
            self["save"] = {}

        # Note: "path" is the deprecated name of "writefolder"
        userPath = str(self["save"].get(
            "writefolder", self["save"].get(
                "path",
                "Saves\\multi\\")))
        folders = [
            AltrootDir + "\\" + userPath,
            AltrootDir + "\\" + userPath + "auto\\",
            AltrootDir + "\\" + "Saves\\multi\\",
            AltrootDir + "\\" + "Saves\\multi\\auto\\",
            AltrootDir + "\\" + "Saves\\pitboss\\",
            AltrootDir + "\\" + "Saves\\pitboss\\auto\\"
            ]

        # Add extra folders
        for extraUserPath in self["save"].get("readfolders", []):
            folders.append(AltrootDir + "\\" + str(extraUserPath))
            folders.append(AltrootDir + "\\" + str(extraUserPath) + "auto\\")

        def remove_duplicates(li):
            my_set = set()
            res = []
            for e in li:
                if e not in my_set:
                    res.append((e, len(res)))
                    my_set.add(e)
            return res
        return remove_duplicates(folders)

    def getSaveFolder(self, folderIndex=0):
        folderpaths = self.getPossibleSaveFolders()
        try:
            return folderpaths[folderIndex][0]
        except IndexError:
            return folderpaths[0][0]

    def getListOfSaves(self, pattern="*", regPattern=None, num=-1):
        folderpaths = self.getPossibleSaveFolders()
        saveList = []
        fileList = []
        if regPattern:
            reg = re.compile(regPattern)

        for fp in folderpaths:
            folderpath = os.path.join(fp[0], pattern)
            for f in glob.glob(folderpath):
                fileList.append((f, fp[1]))

        # Add timestamp (as tuple)
        existingWithTimestamps = [
            (x[0], x[1], os.path.getctime(x[0])) for x in fileList]

        # Sort by timestamp
        existingWithTimestamps.sort(key=lambda xx: xx[2])

        # Remove oldest and non-saves
        existingWithTimestamps = [x for x in existingWithTimestamps if
                                  x[0].endswith(".CivBeyondSwordSave")]
        if regPattern:
            existingWithTimestamps = [x for x in existingWithTimestamps if
                                      reg.search(x[0])]

        while len(existingWithTimestamps) > num and num >= 0:
            existingWithTimestamps.pop(0)

        for savefile in existingWithTimestamps:
            saveList.append({
                'name': os.path.basename(savefile[0]),
                'folder': os.path.dirname(savefile[0]),
                'folderIndex': savefile[1],
                'date': time.ctime(savefile[2]),
                'timestamp': savefile[2]
                })

        return saveList

    def createSave(self, filename, folderIndex=0):
        filepath = os.path.join(self.getSaveFolder(folderIndex), filename)

        if (filename != ""):
            if (not PB.save(filepath)):
                ret = {'return': 'fail',
                       'info': 'Saving of "%s" failed.' % (filepath,)}
            else:
                # Update last file name info and save json file
                self.lock.acquire()
                self.load(False)
                self["save"]["filename"] = filename
                self["save"]["folderIndex"] = folderIndex
                self.lock.release()
                self.save()
                ret = {'return': 'ok',
                       'info': 'File was saved in "%s".' % (filepath,)}

        return ret

    def createPlayerRecoverySave(self, playerId, playerName, bOnline):
        # 1. Check which saves already exists for this player
        # and remove old recovery saves
        folder = self.getSaveFolder(1)
        recoverPrefix = 'Logoff_'
        if bOnline:
            recoverPrefix = 'Login_'

        # Windows file names can not contain * characters.
        # Replace the string "*Mod* ", which
        # can prepend the player name.
        playerName = playerName.replace("*MOD* ", "MOD_").strip()

        existingRecoverySaves = glob.glob(
            "%s%sP%i_*.CivBeyondSwordSave" % (folder, recoverPrefix, playerId))
        # Add timestamp (as tuple)
        existingRecoverySavesWithTimestamps = [
            (x, os.path.getctime(x)) for x in existingRecoverySaves]
        # Sort by timestamp
        existingRecoverySavesWithTimestamps.sort(key=lambda xx: xx[1])
        # Remove oldest
        while(len(existingRecoverySavesWithTimestamps) >=
              self.get("numRecoverySavesPerPlayer", 3)):
            old = existingRecoverySavesWithTimestamps.pop(0)
            os.remove(old[0])

        # 2. Save new recovery save
        filename = "%sP%i_%s_T%i.CivBeyondSwordSave" % (recoverPrefix,
                                                        playerId, playerName,
                                                        int(time.time()))
        self.createSave(str(filename), 1)


def nested_dict_update(dBase, dUpdate, max_depth=-1):
    """ Overwrite dBase values with dUpdate values,
    but join them if both are dicts.

    Note that this function alter both input dicts.
    """

    # 0. Lowest level is without recursion.
    if max_depth == 0:
        dBase.update(dUpdate)
        return

    # 1. Update existing keys
    for k in dBase:
        if k in dUpdate:
            if(isinstance(dBase[k], dict) and isinstance(dUpdate[k], dict)):
                nested_dict_update(dBase[k], dUpdate[k], max_depth-1)
            else:
                dBase[k] = dUpdate[k]

            dUpdate.pop(k)

    # 2. Add new keys
    dBase.update(dUpdate)
