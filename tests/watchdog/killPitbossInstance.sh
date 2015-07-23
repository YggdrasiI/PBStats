#!/bin/bash
# 
# 
#

if [ "$1" = "-h" ] ; 
then
	echo "
	Kill wine process of Pitboss game.
	Use the name of the	ALTROOT directory as identifier.
	The full ALTROOT path shouldn't contain spaces.

	usage: ./$0 [Altroot directory, default: PB1]"
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
		#return 0
	else
		echo "Can't find unique PID for '${1}'. Abort process kill."
		#return -1
	fi

fi

