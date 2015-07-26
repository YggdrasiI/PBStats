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
# • Configure the Pitboss servers over the file pbSettings.json in the
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

# Defaut mod name. 
# Can be overwritten in selectAltroot. Moreover, the modname
# will be changed automatically if the save contains an other mod name.
MOD="PB Mod_v5"

# Insert the names of your games here.
START_MENU="""
	==== Select Game/Altroot ====
	ID - Description
	
	 1 - Pitboss 1
	 2 - Pitboss 2
	 list [ID] - Print out names of 20 youngest saves.
	 help - Print help and exit.
	
	"""

# Insert the folders of your games here
# Use linux syntax for the path's.
selectAltroot() {
	case "$1" in
		1)
			ALTROOT="$ALTROOT_BASEDIR/PB1"
			MOD="PB Mod_v5"
			;;
		2)
			ALTROOT="$ALTROOT_BASEDIR/PB2"
			MOD="PB Mod_v5"
			;;
		help)
			printHelp
			exit 0
			;;
		list)
			listSaves "$2"
			exit 0
			;;
		*)
			echo "No game defined for this index."
			exit -1
			;;
	esac
}

###### End of configuration



###### Begin of internal constants
# Timeout to wait a few seconds before the pitboss server restarts.  
RESTART_TIMEOUT=3

# Seed directory
ALTROOT_SEED="$ALTROOT_BASEDIR/seed"

###### End of internal constants



###### Begin of helper functions 

printHelp() {
	echo """Syntax: $0 gameid [savegame] [password]

 gameid: Selects the game. Edit the entries in the 'selectAltroot' function
         to define more games. Use a different ALTROOT directory for each game.
 savegame: If the server automatically load a save, it takes the filename
           defined in pbSettings.json.
           Use this argument to override the filename. Moreover, it's not required
           to write out the full filename. The script takes the youngest file which
           matches the pattern. This is useful to load the latest save of a player.
 password: Overrides the stored password. Be careful, a wrong password traps the
           server in an infinite loop. It have to be killed manually...
	"""
}

listSaves() {
	echo "Youngest saves for $1:"
	selectAltroot "$1" 
	INAME="*.CivBeyondSwordSave"
	LIST=$(	/usr/bin/find -L ${ALTROOT}  -maxdepth 20 -type f -iname "${INAME}" -printf "%11.10T@ ,%f\n" | /usr/bin/sort -n -r -k1 | /usr/bin/head -n 20 )
	echo "${LIST}" | sed -e 's/.*,/  /'
}

# Return 1 if autostart is 'true' or '1'
isAutostartEnabled() {
	AUTOSTART_VAL=$( grep '"autostart".*:' < "$1/pbSettings.json" | sed -e 's/^.*:[ ]*\([^,}]*\).*$/\1/' ) 
	if [ "$AUTOSTART_VAL" = "1" -o "${AUTOSTART_VAL,,}" = "true" ] ; then
		return 0
	fi
	return -1
}

# Open pbSettings.json to detect filename of current save
getSaveName(){
	PBSET_FNAME=$( grep -e '"filename"[^:]*:' < "$1/pbSettings.json" | sed -e 's/^.*"filename"[^:]*:[^"]*"\([^"]*\)".*$/\1/' )
	echo -n "$PBSET_FNAME"
}

# Replace filename and optionally the password in pbSettings.json
setSaveName(){
	COMPLETE_FNAME="${2##*/}"
	REGEX="s/\"filename\"[^:]*:[^\"]*\"\([^\"]*\)\"/\"filename\": \"$COMPLETE_FNAME\"/" 
	if [ "${#3}" -gt 0 ] ;
	then
		REGEX2="s/\"adminpw\"[^:]*:[^\"]*\"\([^\"]*\)\"/\"adminpw\": \"$3\"/" 
		eval "sed -i -e '$REGEX' -e '$REGEX2' '$1/pbSettings.json'"
	else
		eval "sed -i -e '$REGEX' '$1/pbSettings.json'"
	fi
}

# Search all subdirectories to find path for given filename substring.
findPath() {
	INAME=${1,,}
	INAME="${INAME%.civbeyondswordsave}*.CivBeyondSwordSave"
	LIST=$(	/usr/bin/find -L ${ALTROOT}  -maxdepth 20 -type f -iname "${INAME}" -printf "%11.10T@ ,%p\n" | /usr/bin/sort -n -r -k1 | /usr/bin/head -n 1 )
	echo ${LIST#*,}
}

# Return mod name for savegame
parseModName() {
	od -t x4 -j 4 -N 4 "$1" |
	if read ADR VAL
	then
		let MOD_NAME_LEN="0x$VAL - 6"
		if [ "$MOD_NAME_LEN" -gt 0 ] ; 
		then
			let END_OF_MOD_NAME="0x$VAL + 7"
			MOD_NAME=$( head -c $END_OF_MOD_NAME "$1" | tail -c $MOD_NAME_LEN )
			echo -n "$MOD_NAME"
		else
			# Savegame includes no mod name.
			echo -n ""
		fi
	fi
}

setupGame() {
	# Filename 
	# Note that the script searched the youngest file
	# with the (partial) name "FNAME*. Case will be ignored, too.
	FNAME="$2"  
	FPASSWORD="$3" # Optional, to replace password in pbSettings.json
	ALTROOT="$1"

	if isAutostartEnabled "${ALTROOT}" ;
	then
		if [ "${#FNAME}" -gt 0 ]
		then
			# Explicit filename given. Try to find file and update pbSettings.json
			FPATH=$(findPath "$FNAME")
			if [ "${#FPATH}" -gt 0 ]
			then
				echo "Update save name in pbSettings.json"
				setSaveName "${ALTROOT}" "${FPATH}" "${FPASSWORD}"
			else
				echo -n "Can not find save for $FNAME. "
				FNAME=$(getSaveName "${ALTROOT}")
				FPATH=$(findPath "$FNAME")
				echo "Use value of pbSettings ($FNAME)"
			fi
		else
			# Use filename of pbSettings.json
			FNAME=$(getSaveName "${ALTROOT}")
			FPATH=$(findPath "$FNAME")
		fi

		if [ -f "${FPATH}" ] ;
		then
			echo "Detected path for save: $FPATH"
			MOD_NAME=$(parseModName "$FPATH")
			echo "Mod name:               $MOD_NAME"
			MOD=$MOD_NAME
		else
			echo "Can not find path for save with name '$FNAME'. Filename misspelled?"
			echo "Abort start of Pitboss Server."
			exit -1
		fi
	else
		echo "Autostart is not enabled. Use given mod name '$MOD'."
		echo "The wizard GUI should be shown."
	fi
}

###### End of helper functions 


main() {

# Create Altroot path with backslashes
ALTROOT_W=`echo "Z:${ALTROOT}" | sed -e 's/[\/]/\\\\/g' `

# More backslash fun...
ALTROOT_W2=`echo "Z:${ALTROOT}" | sed -e 's/[\/]/\\\\\\\\/g' `

# Write the correct ALTROOT path into the ini-file.
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

echo "Altroot path (wine):    ${ALTROOT_W}"

# Analyse savegame to get correct mod name if autostart is enabled.
#  This updates the content of $MOD
setupGame "${ALTROOT}" "$2" "$3"

# Start infinite loop for the selected game
cd "$CIV4BTS_PATH"
for(( ; ; )) do
	if [ -z "$DISPLAY" ]; then
		echo "No display detected. Starting with xvfb-run."
		xvfb-run -s "-screen 0 640x480x24" wine "$CIV4BTS_EXE"  mod= "${MOD}"\" /ALTROOT="${ALTROOT_W}"
	else
		wine "$CIV4BTS_EXE"  mod= "${MOD}"\" /ALTROOT="${ALTROOT_W}"
	fi

	echo -n "Restart server"
	for i in $(seq $RESTART_TIMEOUT -1 1);
	do
		echo -n "."
		sleep 1
	done
	echo "now."
done

}



#### Select game and start server

GAMEID="menu"
test -n "$1" && GAMEID="$1"

if [ "${GAMEID}" = "menu" ] ; then
	# Write the names of your games here.
	echo "${START_MENU}"
	read GAMEID
fi

selectAltroot "$GAMEID" "$2"
main "$ALTROOT" "$2" "$3"


