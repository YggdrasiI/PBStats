#!/bin/bash
# Installation: 
# 1. Extract Altroot example to '$HOME/PBs'
# 2. Place this script to in the folder of your
#    Civ4:BTS installation or setup an 'cd' command
#    i.e
#    cd "$HOME/Civ4/Beyond the Sword"
# 3. Insert your ALTROOT paths into this script (see below)
#
# ATTENTION! Backup/Move your "My Games"-Folder before
#  you start the Pitboss Server with an empty ALTROOT-Folder.
#  Your current "BTS-My Games-Folder" will be moved!
#
# Notes: 
# • The wine drive 'Z:' should be mapped to '/' (default wine setting)
# 

# Path to Civ 4
CIV4BTS_PATH="$HOME/Civ4/Beyond the Sword"

# Folder with a good pitboss configuration set 
ALTROOT_SEED="$HOME/PBs/seed"

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
		ALTROOT="$HOME/PBs/PB1"
		;;
	2)
		ALTROOT="$HOME/PBs/PB2"
		;;
	*)
		echo "No game for this index defined."
		exit 0
		;;
esac

# Create Altroot path with backslashes
ALTROOT_W=`echo "Z:${ALTROOT}" | sed -e 's/[\/]/\\\\/g' `

# More backslash fun...
ALTROOT_W2=`echo "Z:${ALTROOT}" | sed -e 's/[\/]/\\\\\\\\/g' `

# Setup the correct ALTROOT path into the ini-file.
#(One time per game required)
if [ ! -d "$ALTROOT" ] ; then
	echo "Altroot dir does not exist. Copy default settings"
	cp -r "$ALTROOT_SEED" "$ALTROOT"

	echo "Fix path in the ini file"
	sed -i -e"s/PitbossSMTPLogin=.*/PitbossSMTPLogin=${ALTROOT_W2}/" "$ALTROOT/CivilizationIV.ini"
fi



# Start infinte loop for the selected game
cd "$CIV4BTS_PATH"
for(( ; ; )) do
	echo "Dir: ${ALTROOT_W}"
	if [ -z "$DISPLAY" ]; then
		echo "No display detected, running with xvfb-run"
		xvfb-run -s "-screen 0 640x480x24" wine "$CIV4BTS_PATH/Civ4BeyondSword_PitBoss2014.exe"  mod= "PB Mod_v1"\" /ALTROOT="${ALTROOT_W}"
	else
		wine "$CIV4BTS_PATH/Civ4BeyondSword_PitBoss2014.exe"  mod= "PB Mod_v1"\" /ALTROOT="${ALTROOT_W}"
	fi

	sleep 1
done

