This Mod tries to fix some bugs in the Pitboss game mode.

Fixed bugs and new features:

- Webfrontend which communicates to your PB servers over TCP/IP. The webfrontend was inspired by civstats.com, but allows the 
	administration of games. 

- Unbreakable pause during open diplomacy screens. 
  Solutions:  
    A) The pause can now be removed by the player over 
      the F1 Screen. ( This screen can be reached per mouse if the diplo menu is open.) 
    B)  The web interface allows to pause/unpause the game, too. 

- Reload of last savegame after server restart. 
  (No boring clicking in the wizard required anymore.) 

- Remove window freeze of Pitboss wizard due Gamespy shutdown. 
  (This was solved by python in this mod. A more general solution is the usage 
  of a modified executable, see test/Civ4BeyondSword_Pitboss2014.exe ) 

- Fix of the upload bug: It's now possible to close open network connections to clients which 
has already leaved the game. (This bug can cause extremely high traffic!) 
Look into test/fix_upload_bug for more instructions. The solution runs independently from this mod.

- Headless Mode. Disables the GUI of your Pitboss server and reduce the CPU usage. (Almost every cpu load (>90%)
is caused due the redrawing of the GUI...) Please setup your game correctly before you disable the 
GUI. This option assumes that a savegame will be loaded at startup. Thus, enable and test the reloading of save games.

- Increase maximal number of players to 52. 

- Add extra nation/player color combinations.

- Player password could be changed over webinterface.

New in version 2 (PB Mod_v2): 
- Connection Issue during PB login screen. Very long leader names and/or very long civ descriptions and/or many
players increases one single IPv4 network package and it could be rejected on its way to a client.
This mod try to reduce the size of this package and cut of leader names and civ names. (This change just affects
		the PB login screen.) You can select how many chars are allowed. If you use all 52 player slots, do not exceed 5 chars per player.
		The default setting is: 1 character for the name and 4 for the nation. 
		Note that both strings will be replaced by the Id of the player if only one character is allowed.


New in version 3 (PB Mod_v3): 
  • Bugfix on scrollable player list


(Removed from master branch)
- Admin password change in one special Game.
	Some players ( http://univers-civilization.leforum.eu/f286-Pit2014.htm )
	lost their admin password.
	I transfer the save from normal BTS into a Save for this mod
	and replace the admin password detection with an tiny fix to
	set a new password.
	Thus, it's theoretical possible to 'save' running games even if the 
	admin password was lost. This patch wasn't published to prevent
	cheating...


