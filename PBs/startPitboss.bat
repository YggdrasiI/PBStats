@echo off
rem Installation:
rem 1. Set ALTROOT_BASEDIR to the absoute path of to 'PBStats/PBs'.
rem 2. Check if CIV4BTS_PATH links to  your Civ4:BTS installation 
rem 3. The scripts copy the seed folder (%ALTROOT_BASEDIR%/seed) into the folder for your new game
rem    but you has to set 'PitbossSMTPLogin' in CivilizationIV.ini of your new game on your
rem    own. Set the variable to the absolute path of the used ALTROOT folder. 
rem
rem Notes: 
rem - Attention, backup your "My Games"-Folder before
rem   you start the Pitboss Server with an empty ALTROOT-Folder.
rem   Due a bug in the Pitboss executable your current
rem   "BTS-My Games-Folder" will be moved to the new position.
rem
rem - Configurate the Pitboss servers over the file pbSettings.json in the
rem   ALTROOT-Directory of each game.
rem   The server will automatialy reload the save at startup if the autostart flag is set 
rem   (see pbSettings.json->save->autostart ) 
rem 	The save will be selected over pbSettings.json->save->filename 
rem 	and has to be placed into [ALTROOT]\Saves\Multi
rem

rem ### Begin of configuration ###

SET ALTROOT_BASEDIR=I:\PBs
SET CIV4BTS_PATH=I:\Olaf\Civ4\Beyond the Sword\


echo...........................................................
echo. Select Game
echo...........................................................
echo. 1 - Pitboss A
echo. 2 - Pitboss B
echo...........................................................
echo.

SET /P M=Type 1, 2,... to select the game and then press ENTER: 

SET ALTROOT=""

rem Place your PB Altroot paths here!
IF %M%==1 SET ALTROOT=%ALTROOT_BASEDIR%\PB1
IF %M%==2 SET ALTROOT=%ALTROOT_BASEDIR%\PB2


rem ### End of configuration ###



rem Use new exe if possible
SET CIV4BTS_EXE=%CIV4BTS_PATH%\Civ4BeyondSword_PitBoss2014.exe
IF not exist "%CIV4BTS_EXE%"  (
		SET CIV4BTS_EXE=%CIV4BTS_PATH%\Civ4BeyondSword_PitBoss.exe
		)

IF not exist "%CIV4BTS_EXE%"  (
		echo.Exe not found. Is the Path %CIV4BTS_PATH% correct?
		goto exit
		)



:loop

IF %ALTROOT%=="" (
		echo.No game selected.
		goto exit
		)

IF not exist "%ALTROOT%" (
	echo. 
	echo. 
	echo.Selected altroot folder not exists! Copy seed folder to initialize it.
	echo.PLEASE SET the variable PitbossSMTPLogin in %ALTROOT%\Civilization.ini
	echo.on %ALTROOT% and select a Port [default is 2056].
	echo.and restart the this script. 
	echo. 
	echo. 
	xcopy "%ALTROOT_BASEDIR%\seed" "%ALTROOT%" /S/E/Q/I/W
	goto exit
)

rem Start server
"%CIV4BTS_EXE%" mod= "PB Mod_v1"\" /ALTROOT=%ALTROOT%

rem Sleep some time to allow quitting of script
ping -n 3 127.0.0.1 > NUL

echo.PB Server was quitted. Restart server.
goto loop


:exit
