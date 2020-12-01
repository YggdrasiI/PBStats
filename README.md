Project in transition
=======

The project is grown over the years and we decided to split it up
into several smaller projects. Visit *https://github.com/civ4-mp*
for an overview.

The main projects there are
1. https://github.com/civ4-mp/pbmod
Civ4 mod compoment with the multiplayer improvements and bug fixes.

2. https://github.com/civ4-mp/pbspy
Web interface which can control PB games with the PB Mod.


PBStats
=======

Mod and Webinterface for Civ4:BTS Pitboss games. Allows remote control of Pitboss servers. 

Many host's of Civ4 Pitboss games knows that the Pitboss server contains many bugs 
which made the hosting of your beloved game hard. This mod tries to solve some of this 
problems. The Mod does not change any game mechanics. 

If you're interested to use this mod in your games note that it's possible to transfer 
save games without mod name to save games of this mod, but you must replace the default DLL (of this mod)
with the DLL for 18 players, see Assets/CvGameCoreDLL.dll.18players.
Remove the admin password before you tranfer your save game and reset it after. 
Look at **PBs/convertSavesToMod.sh** if you want convert your saves.


Installation
=======

##A) As Player/User 
Just download this Mod package and place the folder **PB Mod_v8** in the mod folder of your Civ4:BTS installation ([Civ4 Installation Path]\Beyond the Sword\Mods ). 
*Do not* place the folder into My Games\Beyond the Sword\Mods! Civ4 would interpret this as different version of the mod. 
To start Civ4 with the modification create a new startup shortcut and extend the target with the mod-parameter. The result should look like  
`[Your Civ 4 install folder]\Civ4\Beyond the Sword\Civ4BeyondSword.exe" mod= PB Mod_v8"\"`

##B) As Pitboss Server Administrator. 

This Mod package contains three modules: **PB Mod\_v8**, **PBs** and **civdj** (or **web**). 

1. **PB Mod\_v8** is the common mod folder. Place it in the mod folder of your Civ4:BTS installation. 
2. The Pitboss server **must be started** with the ALTROOT parameter. Otherwise, some Python files can not be found! If you host multiple games on one machine you probably know this parameter... 
The **PBs**-folder contains a prepared example for the start of the Pitboss server 
with ALTROOT parameter. We recommend the usage of the startup script, see below. 
3. A) The **civdj**-folder contains the HTML front end for the game. 
It's similar to the well known civstats.com page, but allows the administration of games, too.  
The folder contains a Django project, see civdj/INSTALL and civdj/civdj/settings.py for more information.
*If you don't want setup an own webserver for this front end, you can use your server, http://civ.zulan.net/pbspy*
3. B) The old webinterface approach can be found in **web**. You can use this if you are more
familar with PHP. Place web/page on your webserver with PHP5 and MySQL or SQLite3 support. Give the server read/write access in the folders **web/sqlite** (if you use SQLite3) and **web/files** 
and read access for the other files. 
Copy web/page/php/config.dist.php to web/page/php/config.php and adapt the default passwords and environment paths of this configuration file to your needs. 
Finally, call web/page/install.php in your browser to initialize all database tables. 


Configuration of the ALTROOT Folder
=======

I assume here that you will start your Pitboss server with the ALTROOT argument. 
First, note that this modification tries to load all preferences from 
the config file **pbSettings.json** which is placed in the ALTROOT-directory.

Follow these steps to setup a new game: 

0. Copy the **PBs** folder to your desired position. 
Use this as root for your ALTROOT folders. 

1. (Linux/Wine) 
   * Open the script startPitboss.sh and adapt the following values: 
_CIV4BTS_PATH="$HOME/Civ4/Beyond the Sword"_  
_ALTROOT_BASEDIR="$HOME/PBStats/PBs"_  
Look at the case-switch where I placed two example entries (PB1 and PB2) 
Extend this list if you need more game slots. 
    * If all paths are set, run the script and enter 1 to start PB1 (example)
During the first startup the **seed** directory will be copied to the ALTROOT path of PB1.
Now, the example save should load and the PB window pops up.
    * Note that the startup of the pitboss window is capsuled into a loop. Thus, the game will restart if you close the window. Use Ctrl+C to abort the script. 
    * Set the autostart flag in **pbSettings.json** to 0 to setup a new game in the wizzard dialog.
Update the saved password in **pbSettings.json**, if you activate auto starting!

2. (Windows)
For Windows users exists the script **startPitboss.bat**. The script contains two sample setups for the games 'PB1' and 'PB2'.
    * Open **startPitboss.bat** in a text editor and adapt the values of
_ALTROOT_BASEDIR=C:\PBStats\PBs_
_CIV4BTS_PATH=C:\Civ4\Beyond the Sword\_
    * Copy the folder PBs\seed to PBs\PB1 (and PBs\PB2, etc…).
    * Open PB1\CivilizationIV.ini and set the value of **PitbossSMTPLogin** to the full path of this directory, i.e. C:\PBStats\PBs\PB1. Without this information Civ4 can not find **pbSettings.json**!
    * Now, start the Batch-File and enter 1 to start PB1. The example save should load and the PB window pops up.
    * The startup is capsuled by a loop. Thus, the game will restart if you close the window. Use Ctrl+C to abort the script. 
    * Set the autostart flag in **pbSettings.json** to 0 to setup a new game in the wizard dialog.
Update the saved password in **pbSettings.json**, if you active auto starting!

3. Setup of **pbSettings.json** 
The most important values are 
    * save.adminpw: Enter the admin password of your save game here. (This is the password which
normally should be entered in the Pitboss wizard at game loading.) 
    * webserver.password: This password will be required to control this instance of the Pitboss server. 
    * webserver.port: Use a unique value for each Pitboss instance. 
    * webfrontent.url: This is the url which will be used to propagate the current status of the game.  Enter your web server here or use our service ( pb.zulan.net/pbspy ).
    * webfrontent.gameId: Create a game entry in the webfrontend to generate this id. 

4. Create a game entry in the web interface. Your PB server should run if you register a new game.

5. (Optional) If you handle with different games or passwords you should edit the file PBs/pbPasswords.json and collect your passwords there. At startup, the server will find the correct one for the
	given save, if possible. Nervertheless you can still use the adminpw-field in pbSettings.json.


Extras
=======

We developed three extras for Civ4:BTS players which are usable **without** this modification, too. 

1. tests/fix_upload_bug contains a solution for the upload bug problematic of Pitboss servers. The executable (Windows) or Python script (Linux) will 
analyze the traffic of your PB servers. If it detects that a client does not response but the server sends data, it will fake the reply of the client (to simulate a normal disconnection).

2. tests/Civ4BeyondSword2015.exe and tests/Civ4BeyondSword_Pitboss2014.exe
The shutdown of the Gamespy NATNEG Servers causes many issues for Multiplayer games. This was solved 
by the community with open NATNEG servers for several games. We've patched the Civ4:BTS executable to 
redirect you to a reliable and stable NATNEG server. The server is hosted for the next years by the well known community member *Zulan* of *civforum.de*.

If you do not want patch your executables you can also use the following entries in your hosts-File:
```
148.251.130.188 civ4bts.natneg1.gamespy.com
148.251.130.188 civ4bts.natneg2.gamespy.com
148.251.130.188 civ4bts.natneg3.gamespy.com
148.251.130.188 civ4bts.available.gamespy.com
```

Note that all players have to use the same NATNEG server. 
Visit http://realmsbeyond.net/forums/showthread.php?tid=7123 (English) or  
http://civ-wiki.de/wiki/Mehrspieler_(Civ4) (German)  for more information.

3. tests/GetSaveOverHttp provides our solution for the incredible slow loading of
Pitboss games. We extended the Civ4:BTS executable and reelease the file transfer 
from Civ4 to an external library (libcurl). The external library downloads the save
over http(s).
