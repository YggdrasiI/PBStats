#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys

import zipfile
import os
import os.path
import re
import urllib
import md5

sys.dont_write_bytecode = True
import simplejson  # Add this file


# Use Windows internal unzip lib
# Work's only if DLL contains Unzip2Folder function
# Note that the Civ4 version was compiled without zlib support. Thus,
# it can not handle archives with compression.
UNZIP_OVER_DLL = True

# True if DLL contains function to evaluate absolute path of mod folder
# Reflect if us has installed under "My Games" or "Civ4 Install Dir"...
WITH_MOD_PATH = True

# Define mod name. Required if WITH_MOD_PATH = False
_MOD_NAME_FALLBACK_ = "PB Mod_v9"


# Wrap extracted files into extra folder (just for debugging)
EXTRA_NESTING = None
#EXTRA_NESTING = "UPDATE"

try:
    from CvPythonExtensions import *
    IN_CIV4 = True
except:
    IN_CIV4 = False
    DUMMY_MOD_PATH = os.path.join("/", "dev", "shm", _MOD_NAME_FALLBACK_)
    #Note that __main__ overwrites DUMMY_MOD_PATH, now.

# Because Python 2.4 version has no urllib.urlopen().getcode()
class Urlopen_with_errcode(urllib.FancyURLopener):
    errcode = 200

    def getcode(self):
        return self.errcode

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        self.errcode = errcode

    #def http_error_404(self, url, fp, errcode, errmsg, headers, data=None):
    #    self.errcode = errcode

class ModUpdater:
    Config_file = "update_config.json"
    Default_config = "update_config.default.json" # Dict or Filename
    """
    Default_config = {
            "update_urls": ["http://localhost:8000/[MODNAME]"],  # Location(s) of 'update.html'
            "visit_url": "http://Your_Mod_homepage",   # Information for User
            "current_version": "__vanilla__",
            "check_at_startup": 0,
        }
    """
    Config = None
    PendingUpdates = []
    __mod_path__ = None
    Info_file = "update_info.json"  # Optional special file in zip's.

    def get_mod_path(self):
        if not IN_CIV4:
            return DUMMY_MOD_PATH

        if self.__mod_path__:
            return self.__mod_path__

        if WITH_MOD_PATH and hasattr(CyGame(), "getModPath"):
            # Absolute path
            self.__mod_path__ = CyGame().getModPath()
        else:
            # Relative Mod path (do not work if Mod is installed in „My Games“
            self.__mod_path__ = os.path.join("Mods", _MOD_NAME_FALLBACK_)

        return self.__mod_path__

    def get_mod_name(self):
        if not IN_CIV4:
            return _MOD_NAME_FALLBACK_

        #mlong = CyPitboss().getModName()  # Hm, not available...
        #mshort = mlong.strip("\\").split("\\")[-1]
        #return mshort

        mlong = self.get_mod_path()
        mshort = mlong.strip("\\").split("\\")[-1]
        return mshort


    def get_config(self):
        if not self.Config:
            self.Config = self.load_config()
        return self.Config

    def get_config_path(self):
        config_path = os.path.join(self.get_config()["mod_path"],
                                   self.Config_file)
        return config_path

    def get_delayed_startup_seconds(self):
        # Negative value omit creation of updater screen
        return self.get_config().get("startup_delay", -1)

    def read_json_dict(self, filename):
        ret = {}
        if os.path.isfile(filename):
            try:
                fp = file(filename, "r")
                ret = dict(simplejson.load(fp))
            finally:
                fp.close()
        return ret

    def load_config(self):
        # Init default config
        if isinstance(self.Default_config, str):
            def_config_path = os.path.join(
                self.get_mod_path(), self.Default_config)
            config = self.read_json_dict(def_config_path)
        else:
            config = self.Default_config

        config["mod_path"] = self.get_mod_path()  # Ensure correct path

        # Config should be load from mod folder
        # Note: Without CyGame().getModPath() function,
        # this is a chicken-or-the-egg problem
        config_path = os.path.join(config["mod_path"], self.Config_file)

        # Update values from file
        config.update(self.read_json_dict(config_path))
        config["mod_path"] = self.get_mod_path()  # Ensure correct path

        # Replace mod name placeholder
        config["mod_path"] = config["mod_path"].replace(
            "[MODNAME]", self.get_mod_name())
        # Quote spaces in urls
        config["update_urls"] = [
            url.replace("[MODNAME]", urllib.quote(self.get_mod_name()))
            for url in config["update_urls"]]

        if not IN_CIV4:
            config["mod_path"] = self.get_mod_path() # == DUMMY_MOD_PATH

        return config

    def write_config(self):
        config_path = self.get_config_path()
        try:
            fp = file(config_path, "w")
            # Note that it's ness. to use the old syntax (integer value)
            # for indent parameter!
            simplejson.dump(self.get_config(), fp, indent=1)
        except:  # Old 2.4 syntax required(!)
            print("Write of '%s' failed!" % (config_path,))
            return False
        return True

    def check_for_updates(self):
        config = self.get_config()

        # This list will be extend for each update found.
        available = [None]  # Dummy entry for "__vanilla__"
        available_names = ["__vanilla__"]

        # This are the names of all instaled updates
        # by this script.
        installed_names = config.get("installed_updates", [])

        # This string should equals installed_updates[-1]
        current_version = config.get("current_version", "")

        # If users install updates manually, an other update could be
        # the latest installed one. Fetching this value here...
        current_version_by_info_file = \
            self.get_info_json().get("name", "__vanilla__")

        # Try urls and break after first available
        bFoundUrl = False
        for url_prefix in config["update_urls"]:
            try:
                url = "%s/%s" % (url_prefix, "updates.html")
                print("Fetch '%s'" % (url,))

                #f = urllib.urlopen(url)  # Note: getcode was added in Python 2.6...

                opener = Urlopen_with_errcode({})
                f = opener.open(url)
                if opener.getcode() != 200:
                    raise Exception("Server not returns statuscode 200 " \
                                    "but %d." % (opener.getcode(),))

                line = f.readline(1000)
                while len(line) > 0:
                    update = self.parse_update_link(line.strip(), url_prefix)
                    line = f.readline(1000)

                    if not update:
                        continue

                    # Skip lines without proper filename
                    if not update["url"].endswith(".zip"):
                        continue
                    for c in " <>":
                        if c in update["name"]:
                            continue

                    # Add .zip extension because name will used as filename.
                    update["name"] = (update["name"] + ".zip").replace(
                        ".zip.zip", ".zip")

                    available.append(update)
                    available_names.append(update["name"])

                f.close()
            except Exception, e:
                print("ERR: %s" % (str(e),))
                continue  # Website lookup fails
            else:
                bFoundUrl = True
                break

        if not bFoundUrl:
            return False  # All website lookups failed

        try:
            upos1 = available_names.index(current_version)
        except ValueError:
            upos1 = 0  # "__vanilla__" position
        try:
            upos2 = available_names.index(current_version_by_info_file)
        except ValueError:
            upos2 = 0  # "__vanilla__" position

        if upos2 > upos1+1:
            print("WRN: Some updates might be skipped." \
                  "     update_info.json refers to %s" \
                  "     but update_config.json to %s" \
                  % (current_version_by_info_file, current_version))

        self.PendingUpdates = available[max(upos1, upos2)+1:]
        return True  # Website lookup ok

    def parse_update_link(self, line, url_prefix):
        # Return dict with found parameter

        # Strip <!-- --> sections.
        line = re.sub(r'<!--.*?-->', "X", line)

        m = re.match('^.*<a[^>]* href="([^"]*)"[^>]*>([^<]*)</a>.*$', line)
        if m:
            name = m.group(2)
            if m.group(1).strip().startswith("http"):
                url = m.group(1)  # Absolute url
            else:
                url = "%s/%s" % (url_prefix, urllib.quote(m.group(1)))

            m_checksum = re.match(
                '^.*<a[^>]* checksum="([^"]*)"[^>]*>([^<]*)</a>.*$', line)
            if m_checksum and m_checksum.group(2) == name:
                checksum = m_checksum.group(1)
                if checksum in ["", "-1"]:
                    checksum = None
            else:
                checksum = None

            # Strip paths, etc
            name = os.path.basename(name)
            name = re.sub(r"[^a-zA-Z0-9_. ]", "", name)

            return {"name": name.strip(), "url": url.strip(), "checksum": checksum}
        else:
            return None

    def has_pending_updates(self):
        return (len(self.PendingUpdates) > 0)

    def start_update(self):
        successful = []
        status = {"successful": True, "updates": []}

        # Overwriting of DLLs is not possible at runtime.
        # Renaming currently used file helps.
        dll_moved = False
        dll_path = os.path.join(self.get_mod_path(), "Assets", "CvGameCoreDLL.dll")
        if os.path.isfile(dll_path):
            dll_path_tmp = dll_path.replace(
                "CvGameCoreDLL.dll", "CvGameCoreDLL.dll.old")
            if os.path.isfile(dll_path_tmp):
                try:
                    os.unlink(dll_path_tmp)
                except Exception, e:
                    print("ERR: Unable to remove '%s' Error was %s" %(dll_path_tmp, str(e)))
            try:
                os.rename(dll_path, dll_path_tmp)
            finally:
                dll_moved = True

        try:
            for update in self.PendingUpdates:
                if self.__start_update__(update):
                    successful.append(update)
                else:
                    status["successful"] = False
                    break

        finally:
            # Restore previous DLL if no new one was unzipped
            # (The try-nesting ensure that errors not prevent code from
            # renaming...)
            if dll_moved and not os.path.isfile(dll_path):
                try:
                    os.rename(dll_path_tmp, dll_path)
                finally:
                    dll_moved = False

        for update in successful:
            status["updates"].append({"name": update["name"],
                                      "info": update.get("info", {})
                                     })
            self.PendingUpdates.remove(update)

        return status

    def __start_update__(self, update):
        print("Download '%s'" % (update["name"],))
        config = self.get_config()
        zip_url = update["url"]
        zip_path = os.path.join(config["mod_path"], update["name"])

        # Use checksum to determine if file already preset and
        # should not be downloaded again.
        already_downloaded = False
        if update.get("checksum"):
            md5_sum = self.get_md5_sum(zip_path)
            if md5_sum == update.get("checksum"):
                print("File '%s' is already preset. " \
                      "Skip download of update file." % (update["name"],))
                already_downloaded = True

        # Download file
        if not already_downloaded:
            try:
                urllib.urlretrieve(zip_url, zip_path)
            except Exception, e:
                print("Unable to download '%s'. Err: %s" %(
                    update["name"], str(e)))
                return False

        # Check checksum of downloaded zip
        if update.get("checksum") and not already_downloaded:
            md5_sum = self.get_md5_sum(zip_path)
            if md5_sum != update.get("checksum"):
                print("ERR: Checksum do not match for '%s'\n Expected: %s\nEvaluated: %s" % (
                    update["name"], update.get("checksum"), md5_sum))
                return False

        if update["name"].endswith(".zip"):
            print("Extract '%s'" % (update["name"],))

            self.remove_old_info_txt()
            if not self.unzip(zip_path, config["mod_path"]):
                return False

            print("Handle meta info of '%s'" % (update["name"],))
            update["info"] = self.get_info_json()
            if not self.handle_info_json(update["info"]):
                return False

            config["current_version"] = update["name"]
            config["installed_updates"] = config.get(
                "installed_updates", []) +  [update["name"]]
            self.write_config()

        return True


    def unzip(self, zip_path, target_path):

        # Debugging...
        # Uncomment this to write updates into different folder
        if EXTRA_NESTING:
            target_path = os.path.join(target_path, EXTRA_NESTING)

        if IN_CIV4 and UNZIP_OVER_DLL:
            # Assume that zip_path is already absolute!
            abs_zip_path = zip_path
            print("Call unzipModUpdate(\"%s\")" % (abs_zip_path,))
            ret = CyGame().unzipModUpdate(abs_zip_path)

            return (ret == 0)

        try:
            zfile = zipfile.ZipFile(zip_path)
            for name in zfile.namelist():
                (dirname, filename) = os.path.split(name)
                if len(filename) == 0:
                    continue  # Ignore lines with folders

                full_path = os.path.join(target_path, dirname)
                print("Decompressing %s in %s" % (filename, full_path))
                if not os.path.exists(full_path):  # Nicht notwendig?!
                    os.makedirs(full_path)

                if IN_CIV4:
                    # Old Python 2.4 variant.
                    # Did not work for compressed zip's because
                    # Civ4 lib is compiled without zlib support!!
                    # An alternative way would be the replacement of
                    # ../Warlords/Assets/Python/System with an other version.
                    try:
                        fp = file(os.path.join(full_path, filename),
                                  "wb")  #, 1024*100)
                        fp.write(zfile.read(name))
                        fp.close()
                    except Exception, e2:
                        # print(str(e2))
                        raise e2

                else:
                    # NOT full_path as 2nd arg!
                    zfile.extract(name, target_path)

        except Exception, e:
            print("Unzipping of %s failed. Error: %s Abort updating" % (
                zip_path, str(e)))
            print("Abort updating")
            return False

        return True

    def get_info_json(self):
        info_path = os.path.join(
            self.get_config()["mod_path"],
            self.Info_file)
        info = {}

        # Update values from file
        if os.path.isfile(info_path):
            try:
                fp = file(info_path, "r")
                info.update(dict(simplejson.load(fp)))
            finally:
                fp.close()

        return info

    def remove_old_info_txt(self):
        info_path = os.path.join(
            self.get_config()["mod_path"],
            self.Info_file)
        if os.path.isfile(info_path):
            try:
                os.unlink(info_path)
            except:
                return False

        return True

    def handle_info_json(self, dInfo):
        if not IN_CIV4:
            print("Info file:")
            print simplejson.dumps(dInfo, sort_keys=True,
                             indent=4,
                             separators=(',', ': '))

        # Check if update meta info provides list of files
        # which should be removed. (Note that they will be removed after
        # the zip was unpacked!)
        lTo_remove = dInfo.get("mod_files_to_remove", [])
        # Use abspath because realpath resovles symbolic links..
        mod_path_abs = os.path.abspath(self.get_mod_path())

        for to_remove in lTo_remove:
            to_remove_slash = to_remove.replace("\\", os.path.sep)
            to_remove_abs = os.path.abspath(os.path.join(
                mod_path_abs, to_remove_slash))
            if not to_remove_abs.startswith(mod_path_abs):
                print("WRN: Mod updater skips unlinking of '%s'." % (to_remove,))
                continue

            if os.path.isfile(to_remove_abs):
                try:
                    os.unlink(to_remove_abs)
                    if not IN_CIV4:
                        print("Remove '%s'." % (to_remove,))
                except:
                    print("WRN: Mod updater was unable to remove '%s'." % (to_remove,))

        return True

    def get_md5_sum(self, zip_path):
        if not os.path.isfile(zip_path):
            return None

        md5_sum = "-1"
        try:
            md5_file = file(zip_path, "rb")
            zip_md5 = md5.new()
            zip_bytes = md5_file.read(1024*1024)
            while zip_bytes != "":  # b"" in Python3, but here just ""
                zip_md5.update(zip_bytes)
                # Do stuff with byte.
                zip_bytes = md5_file.read(1024*1024)

        except Exception, e:
            print("Unable to evaluate md5 of '%s'. Err: %s" %(
                zip_path, str(e)))
            #md5_file.close() # not exists
        else:  # No try-except-finally in Python 2.4
            md5_file.close()
            md5_sum = zip_md5.hexdigest()

        return md5_sum

if __name__ == "__main__":
    # Select Mod folder as target
    script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
    iAssetsPos = script_folder.rfind("Assets")
    if iAssetsPos == -1:
        DUMMY_MOD_PATH = os.path.join(script_folder, _MOD_NAME_FALLBACK_)
        # => I.e. Z:\dev\shm\Updater
    else:
        DUMMY_MOD_PATH = script_folder[:iAssetsPos-1]
        (_, _MOD_NAME_FALLBACK_) = os.path.split(DUMMY_MOD_PATH)

    print("Mod path: %s" %(DUMMY_MOD_PATH,))

    # Check if updates are forced
    bForce = False
    if len(sys.argv) > 1 and sys.argv[1] in ["-f", "--force", "-y", "--yes"]:
        bForce = True


    updater = ModUpdater()
    updater.check_for_updates()

    if updater.has_pending_updates():
        print("Avaiable updates:")
        for u in updater.PendingUpdates:
            print("  - %s" %(u["name"],))

        if not bForce:
            print("" \
                  "Press [Enter] to continue installation " \
                  "and [Ctrl+C] to abort.")
            try:
                user_in = sys.stdin.readline()
            except:
                pass
            else:
                bForce = True

        if bForce:
            status = updater.start_update()
            if not status.get("successful", False):
                sys.exit(-1)

    else:
        print("No pending updates.")
