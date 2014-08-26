This Mod tries to fix some bugs
in the Pitboss game mode.

Fixed Bugs:
- Unbreakable pause during open diplomacy screens.
  Solution: The pause can now be removed by the player over
			the F1 Screen. This screen can be reached my mouse.
			Moreover, the web interface allows to pause/unpause
			the game without logging in.

- TCP/IP-Interface which can be used to manage the server
	or get information about the current game round.

- Automatic restart of Pitboss server. (No boring clicking in the wizard required anymore.) 

- Remove window freeze of Pitboss wizard due Gamespy shutdown.

- Fix of the upload bug: It's now possible to close open network connections to clients which
has already leaved the game. (This bug can cause extremely high traffic!) 
Look at test/fix_upload_bug for more instructions. The solution runs independently from this mod.

- Headless Mode. Disables the GUI of your Pitboss server and reduce the CPU usage. (Almost every load
was caused due the redrawing of the GUI...) Please setup your game correctly before you disable the
GUI. This option assumes the the automatic save game loading at startup is working.



(Removed from master branch)
- Password change for one special Game.
	Some players ( http://univers-civilization.leforum.eu/f286-Pit2014.htm )
	lost their admin password.
	I transfer the save from normal BTS into a Save for this mod
	and replace the admin password detection with an tiny fix to
	set a new password.
	Thus, it's theoretical possible to 'save' running games even if the 
	admin password was lost. This patch wasn't published to prevent
	cheating...


Other changes:
- Increase maximal number of players to 52.
- Add extra nation/player color combinations.
