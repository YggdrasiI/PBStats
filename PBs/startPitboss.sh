#!/bin/bash
#
# Installation: 
# 1. Set ALTROOT_BASEDIR to the subfolder PBStats/PBs or copy this directory 
#    at the desired position of your Pitboss games, i.e. $HOME/PBs.
# 2. Check if CIV4BTS_PATH links to  your Civ4:BTS installation 
#    i.e "$HOME/Civ4/Beyond the Sword"
# 3. Insert your ALTROOT paths into this script (see below)
#   This should be subfolders of ALTROOT_BASEDIR.
#
# Notes: 
# • Attention, backup/move your "My Games"-Folder before
#   you start the Pitboss Server with an empty ALTROOT-Folder.
#   Due a bug in the Pitboss executable your current
#   "BTS-My Games-Folder" will be moved to the new position!
#
# • Configurate the Pitboss servers over the file pbSettings.json in the
#   ALTROOT-Directory of each game.
#
# • The script assumes that the wine drive 'Z:' 
#   is mapped to '/' (default wine setting).
# 

### Begin of configuration

# Path to Civ 4
CIV4BTS_PATH="$HOME/Civ4/Beyond the Sword"

# Folder which will be used as container for all ALTROOT directories.
# It should contains the configuration seed folder (seed) 
# Set this to the subfolder '[...]/PBStats/PBs' !
ALTROOT_BASEDIR="$HOME/PBStats/PBs"

GAMEID="menu"
test -n "$1" && GAMEID="$1"

if [ "${GAMEID}" = "menu" ] ; then
	# Write the names of your games here.
	echo ""
	echo " ==== Select Game/Altroot ===="
	echo ""
	echo " 1 - Pitboss 1"
	echo " 2 - Pitboss 2"
	read GAMEID

fi


# Insert the folders of your games here
# Use linux syntax for the path's.
case $GAMEID in
	1)
		ALTROOT="$ALTROOT_BASEDIR/PB1"
		;;
	2)
		ALTROOT="$ALTROOT_BASEDIR/PB2"
		;;
	*)
		echo "No game definded for this index."
		exit 0
		;;
esac

###### END of configuration


# Seed directory
ALTROOT_SEED="$ALTROOT_BASEDIR/seed"

# Create Altroot path with backslashes
ALTROOT_W=`echo "Z:${ALTROOT}" | sed -e 's/[\/]/\\\\/g' `

# More backslash fun...
ALTROOT_W2=`echo "Z:${ALTROOT}" | sed -e 's/[\/]/\\\\\\\\/g' `

# Setup the correct ALTROOT path into the ini-file.
#(One time per game required)
if [ ! -d "$ALTROOT" ] ; then
	echo "Altroot dir does not exist. Copy default settings"
	cp -L -r "$ALTROOT_SEED" "$ALTROOT"

	echo "Fix path in the ini file"
	sed -i -e"s/PitbossSMTPLogin=.*/PitbossSMTPLogin=${ALTROOT_W2}/" "$ALTROOT/CivilizationIV.ini"
fi


# Check if patched executable is available
if [ -f "$CIV4BTS_PATH/Civ4BeyondSword_PitBoss2014.exe" ] ; then
	CIV4BTS_EXE="$CIV4BTS_PATH/Civ4BeyondSword_PitBoss2014.exe"
else
	CIV4BTS_EXE="$CIV4BTS_PATH/Civ4BeyondSword_PitBoss.exe"
fi


# Start infinte loop for the selected game
cd "$CIV4BTS_PATH"
for(( ; ; )) do
	echo "Dir: ${ALTROOT_W}"
	if [ -z "$DISPLAY" ]; then
		echo "No display detected, running with xvfb-run"
		xvfb-run -s "-screen 0 640x480x24" wine "$CIV4BTS_EXE"  mod= "PB Mod_v1"\" /ALTROOT="${ALTROOT_W}"
	else
		wine "$CIV4BTS_EXE"  mod= "PB Mod_v1"\" /ALTROOT="${ALTROOT_W}"
	fi

	sleep 1
done

