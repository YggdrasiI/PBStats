rem Installation:
rem 1. Set ALTROOT_BASEDIR to the absoute path of to 'PBStats/PBs'.
rem 2. Check if CIV4BTS_PATH links to  your Civ4:BTS installation 
rem 3. Copy the seed folder (PBStats/PBs/seed) into the folder for your new game
rem    (i.e. PBStats/PBs/PB1 ) and set 'PitbossSMTPLogin' in PBStats/PBs/PB1/CivilizationIV.ini
rem    to the absolute path of the used ALTROOT folder. 
rem
rem Notes: 
rem - Attention, backup/move your "My Games"-Folder before
rem   you start the Pitboss Server with an empty ALTROOT-Folder.
rem   Due a bug in the Pitboss executable your current
rem   "BTS-My Games-Folder" will be moved to the new position!
rem
rem - Configurate the Pitboss servers over the file pbSettings.json in the
rem   ALTROOT-Directory of each game.
rem   The server will automatialy reload the save at startup if the autostart flag is set 
rem   (see pbSettings.json->save->autostart ) 
rem 	The save will be selected over pbSettings.json->save->filename 
rem 	and has to be placed into [ALTROOT]\Saves\Multi
rem
@echo off


SET ALTROOT_BASEDIR="I:\PBs"
SET CIV4BTS_PATH="I:\Civ\Beyond the Sword\"


echo ..........................................................
echo  Select Game
echo ..........................................................
echo  1 - Pitboss A
echo  2 - Pitboss B
echo  3 - Pitboss C
echo  4 - Pitboss D
echo ..........................................................

SET /P M=Type 1, 2, 3, or 4 then press ENTER:

rem Use new exe if possible
SET CIV4BTS_EXE="%CIV4BTS_PATH%\Civ4BeyondSword_PitBoss2014.exe"
IF not exist "%CIV4BTS_EXE%"  (
		SET CIV4BTS_EXE="%CIV4BTS_PATH%\Civ4BeyondSword_PitBoss.exe"
		)


:loop
IF %M%==1 goto game_one
IF %M%==2 goto game_two
IF %M%==3 goto game_three
IF %M%==4 goto game_four
goto exit


rem First game
:game_one
%CIV4BTS_EXE% mod= "PB Mod_v1"\" /ALTROOT="%ALTROOT_BASEDIR%\PB1"
goto loop

rem Second game
:game_two
%CIV4BTS_EXE% mod= "PB Mod_v1"\" /ALTROOT="%ALTROOT_BASEDIR%\PB2"
goto loop 

rem Third game
:game_three
%CIV4BTS_EXE% mod= "PB Mod_v1"\" /ALTROOT="%ALTROOT_BASEDIR%\PB3"
goto loop 

rem Fourth game
:game_four
%CIV4BTS_EXE% mod= "PB Mod_v1"\" /ALTROOT="%ALTROOT_BASEDIR%\PB4"
goto loop 



:exit
