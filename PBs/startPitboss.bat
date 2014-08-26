rem Civ4BeyondSword_PitBoss.exe mod= Pitboss Mod"\" /ALTROOT="[PLACE YOUR PB Folder here]
rem
rem infinite loop which restarts the server. 
rem Configurate the server over the file pbSettings.json in your
rem ALTROOT-Directory of each game.
rem The server will automatialy reload the save at startup if the autostart flag is set (see pbSettings.json->save->autostart ) 
rem The save will be selected over pbSettings.json->save->filename 
rem and has to be placed into [ALTROOT]\Saves\Multi
rem
rem Use the webinterface to change the loaded game.
rem
@echo off

echo ..........................................................
echo  Select Game
echo ..........................................................
echo  1 - Pitboss A
echo  2 - Pitboss B
echo ..........................................................

rem SET /P M=Type 1, 2, 3, or 4 then press ENTER:
SET /P M=Type 1, 2, 3, or 4 then press ENTER:

:loop
IF %M%==1 goto game_one
IF %M%==2 goto game_two
goto exit


rem First game
:game_one
..\Civ4BeyondSword_PitBoss.exe mod= "PB Mod_v1"\" /ALTROOT="I:\PBs\PB1"
goto loop


rem Second game
:game_two
..\Civ4BeyondSword_PitBoss.exe mod= "PB Mod_v1"\" /ALTROOT="I:\PBs\PB2"
goto loop 



:exit
