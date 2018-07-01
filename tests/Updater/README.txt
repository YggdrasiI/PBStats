=== Information about Civ4 mod updater component ===

Features:
  • Adds extra screen to main menu which inform user about mod updates.
  • Installs (aka unzip + sugar) mod updates with one click within the game.

Usage:
  As user: Just click on 'search updates' in the main screen.
    If an error occours, remove update_config.json and update_info.json. 

  As mod developer:
   To prepare your mod update, just…
   1. Put all changed/new files of your mod into a zip archive.
      Use the mod directory as root directory.

   2. (optional) Add the file 'update_info.json' into the zip archive.
      The name field should equals the link name in step 3!

      {
        "name": "Update 1.zip",
        "desc": "My update description",
        "mod_files_to_remove": ["Assets\\Python\\some_file.py"]
      }

   3. Put the archive  on your webserver (or github, forum attachment, etc)
      and add a link to your updates.html site, i.e.

      <a href="example_update001.zip" checksum="-1">Update 1.zip</a><br />

   4. (Optional) Add correct checksum of your update zip. Useful if you
      not host the zip on your own...
      On *nix systems use 'md5sum [Zip file]' to get the md5 checksum.

   If you use git for your mod development you could automatize above steps with
   following script:
      generate_update_package.py (TODO)


Requirements:
   • Web space to provide "updates.html" and the update zip's (i.e. update001.zip)
     The html-file just lists links to all updates.
     Use PBStats/tests/Updater/server as example/template for your mod.

   • Implementation of some extra DLL functions, see dll_changes.diff
     Copy the *.obj-Files into your CvGameCoreDLL folder! They contain some Boost libaries
     for boost::thread, etc.
     It is difficult to compile them today on your own because Boost 1.32
     is very old…

   • Adding of new Screen (Python/Screens/CvModUpdater.py, XML/Text/PBModUpdater.xml) and
     updater file (Python/Extra/ModUpdater.py, Python/simplejson.py)

   • Add update_config.json to your mod with following content:
        {
            "update_urls": ["http://localhost:8000/[MODNAME]"],
            "visit_url": "http://Your_Mod_homepage",
            "current_version": "__vanilla__",
            "check_at_startup": 0
        }

      Notes:
        Above struct could be out-dated. Current values can be found in ModUpdater.load_config(self) 
        The "mod_path" key should not be defined because it will be auto detect.


Implementation:
   A minimal working example mod is included: Mods/Updater.

   New Files:
    ./Python/Screens/CvModUpdaterScreen.py
    ./Python/Extras/simplejson.py
    ./Python/Extras/ModUpdater.py
    ./XML/Text/PBModUpdater.xml
    ./CvGameCoreDLL.dll

   Changed Files: (search for 'Updater Mod')
    ./Python/Screens/CvScreenEnums.py
    ./Python/CvEventManager.py

   Notes:
     - To minimize the number of affected files, some function definitions will be made on runtime,
     see Python/Screens/CvModUpdaterScreen.integrate()
     - DLL changes could be found in Mods/Updater/CvGameCoreDLL/


A few more notes for Modders:
 • The Python-Version of Civ4 does not contain zlib-support! Thus, you can not just use the internal
   python lib to unzip files, but the indirection over the dll.

 • Normally, you can not decide if the user has installed the mod into the game installation directory
   or My Games\Beyond the Sword\Mods. You can just guess, but in some corner cases not.
   This Mod contains a reliable way to detect the correct path. It ask the operating system where
   the CvGameCoreDLL.dll is located.

 • Adding a Screen to the main menu is a bit tricky! You can not use the OnInit-Eventhandler
   because it fires to early. At this game startup stage, it is not possible to draw anything
   on the screen.
   The only useful event handler is onWindowActivation. Unfortunately, the first call of this event
   has two pitfalls.
   Firstly, some data is still not initialized and i.e.
     CyTranslator.getText can throw a C++-Exceptions and the call of
     CvModUpdaterScreen.getScreen also fails.

   Secondly, the drawing of the main menu begins after onWindowActivation(). This hides everything
   behind the background image.

   Starting a new Python thread for some delayed redrawing command fails because the Cy*-Objects did
   not live long enough. (?!)
   I resolved this problem by starting a new thread over a DLL call.


Issues:
 • Unzipping does not work in WINE. The (correct) path is not acceptad as valid in…
   The problematic code part:

      pISD->NameSpace( InZipFile, &pZippedFile);  // Returns NULL in Wine :-(
      if (!pZippedFile)
      {
        pISD->Release();
        LOG("Zip file not found.");
        return 1;
      }


Thanks:
  The Caveman2Cosmos developer, who compiled the missing boost libraries for the ancient 1.32 version.

