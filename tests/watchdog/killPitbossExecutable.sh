#!/bin/bash
# 
# 

# pbSettings["save"]["filename"] =
#   pbSettings["save"]["previous_filename"]
load_previous_save () {
	ALTROOT="$1"
	grep "['\"]previous_filename['\"][ \t]*:" >/dev/null 2>&1 <"$ALTROOT/pbSettings.json" 
	if [ 0 -eq "$?" ] ; 
	then
		#echo "Replace filename."
		sed -e "/['\"]\(filename\|folderIndex\)['\"][ \t]*:/d" \
			-e "s/['\"]previous_filename['\"][ \t]*:/\"filename\":/" \
			-e "s/['\"]previous_folderIndex['\"][ \t]*:/\"folderIndex\":/" \
			-i "$ALTROOT/pbSettings.json"
	#else
		#echo "No previous filename found."
	fi
}

if [ "$1" = "-h" ] ; 
then
	echo "
	Kill wine process of Pitboss game.
	Use the name of the	ALTROOT directory as identifier.
	The full ALTROOT path shouldn't contain spaces.

	usage: ./$0 [Altroot directory, default: PB1] [Use previous save, optional flag ]"
else
	PB=${1:-PB1}
	FILTER="ALTROOT=[^ ]*$PB"

	# Second grep filtering out the xvfb-run lines
	LINE=$(ps -au | grep -e "Civ4BeyondSword" | grep -v -e " wine " | grep -e "$FILTER" )
	PID=$(echo "${LINE}" | sed -n -e "s/^[^ ]*[ ]\+\([0-9]\+\).*$/\1/p" )
	NPID=$(echo ${PID} | wc -w )

	if [ "$NPID" -eq "1" ];
	then
		#echo "PID: $PID, Line: $LINE"
		kill -9 $PID
		if [ "$2" = "1" ] ;
		then
			ALTROOT=$(echo ${LINE##*ALTROOT=Z:})
			ALTROOT=${ALTROOT//\\/\/}
			#echo "Linux altroot: ${ALTROOT}"
			load_previous_save "$ALTROOT"
		fi
		#return 0
	else
		echo "Can't find unique PID for '${1}'. Abort process kill."
		#return -1
	fi

fi

