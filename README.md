PBStats
=======

Mod and Webinterface for Civ4:BTS Pitboss games. Allows remote control of Pitboss servers. 

Many host's of Civ4 Pitboss games knows that the Pitboss server contains many bugs 
which made the hosting of your beloved game hard. This mod tries to solve some of this 
problems. The Mod does not change any game mechanics. 

If you're interested to use this mod in your games note that it's possible to transfer 
save games without mod name to save games of this mod. (This transformation isn't reversible 
if the save game is protected with a password.) 
Look at **PBs/convertSavesToMod.sh** if you want convert your saves.


Extras
=======

We developed two solution for Civ4:BTS players which are usable **without** this modification, too. 

1. test/fix_upload_bug contains a solution for the upload bug problematic of Pitboss servers. The executable (Windows) or Python script (Linux) will 
analyze the traffic of your PB servers. If it detects that a client does not response but the server sends data, it will fake the reply of the client (to simulate a normal disconnection).

2. The shutdown of the Gamespy NATNEG Servers causes many issues for Multiplayer games. This was solved 
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


Installation
=======

##A) As Player/User 
Just download this Mod package and place the folder **PB Mod_v1** in the mod folder of your Civ4:BTS installation. 
To start Civ4 with the modification create a new startup shortcut and extend the target with the mod-parameter. The result should look like  
`[Your Civ 4 install folder]\Civ4\Beyond the Sword\Civ4BeyondSword.exe" mod= PB Mod_v1"\"`

##B) As Pitboss Server Administrator. 

This Mod package contains three modules: **PB Mod\_v1**, **PBs** and **web**. 

1. **PB Mod\_v1** is the common mod folder. Place it in the mod folder of your Civ4:BTS installation. 
2. The Pitboss server should be started with the ALTROOT parameter. (If you host multiple games 
on one machine you proably know this parameter...) 
The **PBs**-folder contains a prepared example for the start of the Pitboss server 
with ALTROOT parameter. See below for more instructions. 
3. The web-folder contains the HTML front end for the game. 
It's similar to the well known civstats.com page, 
but allows the admininstration of games, too.  
Place the web-folder on your webserver with PHP5 and MySQL or SQLite3 support. Give the server read/write access in the folders **sqlite** (if you use SQLite3) and **files** 
and read access for the other files. 
Copy web/page/php/config.dist.php to web/page/php/config.php and adapt the default passwords and environment paths of this configuration file to your needs. 
Finally, call web/page/install.php in your browser to initialise all database tables. 

If you don't want setup an own webserver for this frontent, you can use your server, *http://civ.zulan.net/pb*, too. 


Configuration of the ALTROOT Folder
=======

I assume here that you will start your Pitboss server with the ALTROOT argument. 
First, note that this modification tries to load all preferences from 
the file **pbSettings.json** which is placed in the ALTROOT-directory. You can modify 
this file with any text editor. 

Follow these steps to setup a new game: 

0. Copy the **PBs** folder to your desired position. 
Use this as root for your ALTROOT folders. 

1. (Linux/Wine) 
For Linux exists a script to automate a few steps… 
   * Open the script startPitboss.sh and adapt the follwing values: 
_CIV4BTS_PATH="$HOME/Civ4/Beyond the Sword"_  
_ALTROOT_BASEDIR="$HOME/PBStats/PBs"_  
Look at the case-switch where I place two example entries (PB1 and PB2) 
Extend this list if you need more game slots. 
    * If all paths are set, run the script and enter the numer of your game 
slot. At first startup the **seed** directory will be copied to the ALTROOT path. 
 
Note that the startup of the pitboss window is capsuled into a loop. Thus, 
the game will  restart if you close the window. Use Ctrl+C to abort the script. 

1. (Windows)
For Windows users exists the script **startPitboss.bat**. 
		* Open it in a text editor and alter the values of ALTROOT_BASEDIR and CIV4BTS_PATH
		* The script contains two sample setups for the games 'PB1' and 'PB2'. Invoke the script
		* one time and start PB1. This will copy the seed folder into %ALTROOT_BASEDIR%\PB1.
    * Now, set the value of **PitbossSMTPLogin** in %ALTROOT_BASEDIR%\PB1\CivilizationIV.ini !
    * If you start the Batch-File a second time, the Pitboss server should start  and load the default save.The startup is capsuled by a loop. 
Thus, the game will restart if you close the window. Use Ctrl+C to 
abort the script. 

2. Setup of **pbSettings.json** 
The most important values are 
    * save.adminpw: Enter the admin password of your save game here. (This is the password which 
 will be enterd in the pitboss wizzard at game loading.) 
    * webserver.password: This password will be required to control this instance of the pitboss server. 
    * webserver.port: Use a unique value for each pitboss instance. 
    * webfrontent.url: This is the url which will be used to propagte the current status of the game.  Enter your web server here or use our service (not online).
    * webfrontent.gameId: Create a game entry in the webfrontend to generate this id. 

3. Create a game entry in the web interface. 

