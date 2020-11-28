This Mod tries to fix some bugs in the Pitboss game mode.

Fixed bugs and new features in version 1 (PB Mod_v1):

	• Webfrontend which communicates to your PB servers over TCP/IP.
		The webfrontend was inspired by civstats.com, but allows the 
		administration of games. 

	• Unbreakable pause during open diplomacy screens. 
		Solutions:  
		A) The pause can now be removed by the player over 
			the F1 Screen. ( This screen can be reached by mouse if the diplo menu is open.) 
		B) The web interface allows to pause/unpause the game, too. 

	• Reload of last savegame after server restart. 
		(No boring clicking in the wizard required anymore.) 

	• Remove window freeze of Pitboss wizard due Gamespy shutdown. 
		(This was solved by python in this mod. A more general solution is the usage 
		of a modified executable, see test/Civ4BeyondSword_Pitboss2014.exe ) 

	• Fix of the upload bug: It's now possible to close open network connections
		to clients which has already left the game. (This bug can cause extremely high traffic!) 
		Look into test/fix_upload_bug for more instructions.
		The solution runs independently from this mod.

	• Headless Mode. Disables the GUI of your Pitboss server and reduce the CPU usage.
		Redrawing the GUi cause almost the complete CPU load (>90%)…
		Setup your game correctly before you disable the GUI.

	• Increase maximal number of players to 52. 
	• Add extra nation/player color combinations.
	• Webinterface: Add menu to change player password.

New in version 2 (PB Mod_v2): 
	• Fix connection issue during PB login.
		Very long leader names and/or very long civ descriptions and/or many
		players increases one single IPv4 network package and it could be rejected on its way to a client.
		This mod try to reduce the size of this package and cut of leader names and civ names.
		(This change just affects the PB login screen.) You can select how many chars are allowed.
		If you use all 52 player slots, do not exceed 5 chars/player!
		The default setting is: 1 character for the player name and 4 for the nation name.
		Note that the selection of '1' do not print the first char, but the id of the player.

New in version 3 (PB Mod_v3): 
	• Bugfix on scrollable player list
	• Infoscreen (F9) fixes:
			- Reduce number of displayed graphs by selecting subset of all players in legend.
			- The screen doesn't reset the selected graph on several user actions.
	• Foreignscreen (F4) fixes:
			- The screen was nearly unusable for the player has more as 30 contacts.
				Now, its possible to select a subset of all contacts and masking the rest.
	• Some color collisions was fixed.
	• Webinterface: Add option to change the player colorset on running PB session. This
		is useful if two neighbours has the same culture border color.
	• Webinterface: Add option to change timer of current round.

New in version 4 (PB Mod_v4): 
	• Bugfixes in F4 Screen
	• Webinterface: Add Wordbuilder-Save generation

New in version 5 (PB Mod_v5):
	• More Bugfixes for F4 screen
	• Replace solution for hanging diplomaticy screen. There is 
		now a button below of the diplo window to unpause the game.
		Moreover, it works now reliable in MP.
	• Better description for "Leave" option in main menu. Now,
		it's more difficult to set a player accidental on AI.
	• Pause Button in PbAdmin window
	• OOS-Fix for games with many cities. The selection algorithm of 
		city names was depending on the game language. 
	• Fix hangup of server if the given password does not 
		match. Application should now quit.
	• Prepend loading of Pitboss save with password check.
		The PbWizard now selects the correct password from a
		given list, pbPasswords.json. 
		This made it easier to handle with different passwords/games.
	•	Espionage bugfix: Do not show espionage popup with old timestamp (turn slice).
		This suppress the faulty espionage popups at next login on the pitboss server.
	• Spaceship launch does not chrash PB server anymore.

New in version 6 (PB Mod_v6):
	• Allow start counter espionage mission at the last round of already running mission.
		This removes the 'one round hole' for the second player in a espionage war.
	• PBSpy webinterface allow kicking of players
	• PBSpy webinterface contains now an option to declare a winner.
	• BTS_Wrapper: Works now with https and http urls.

New in version 7 (PB Mod_v7):
	• Add gc.sendTurnCompletePB(iPlayer) funktion.
	• Add optional Civ4Shell-Callback in Gameloop of PB Server
	• Extend PB startup modes to allow control over Civ4Shell, only (without GUI or Webfrontend).
	• BTS_Wrapper: Fast transfer of Saves in normal MP-Games, too

New in version 8 (PB Mod_v8)
	• Integrated path detection of Mod folder (CyGame().getModPath())
	• Integrated Mod Updater (see tests/Updater for minimal example)
	• http-Links in [LINK=...]...[/LINK] open websites in browser.

New in version 9 (PB Mod_v9)
  • Alt+[Click on Playername] now shows popup, but not declare war directly.
  • Ctrl+Q not retire from the game anymore.
  • Stack attack option triggers warning if pitboss game is entered.
  • Pyconsole feature improved
  • Add improved szenario loader (pyWB). It can now handle szenario files
    for different number of players.

New in version 9.3 (PB Mod_v9)
• Made 'Advanced Start' available for Pitboss games.
• Fix infinite turn loop for sequential (non-simultaneous) PBs
• Raise scoreboard height on new contact.
• Fix password handling in startPitboss.py. Value in password prompts will not ignored, now.
• Allow change of Multiplayer Options after the game has started.
• Disable AI conversion if MPOPTION_TAKEOVER_AI is false.
• Improve chat support for Pitboss host (sound notifications, chat messages not stored as longterm log message)
• PBSpy supports now notification mails if other players finishes
their turns.
• Add several commands to Pyconsole:
list_cities, list_units, unreveal_map, remove_ocean_forrest, etc
• Fix startup crash if Pyconsole is enabled.
• Fix scroll bug in score list during contact attempt of other human player.
