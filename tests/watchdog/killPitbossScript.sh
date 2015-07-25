#!/bin/bash
# 
# Kill startup script of game. Thus, the game will not be restarted.

if [ "$1" = "-h" ] ; 
then
	echo "
# Kill startup script of game. Thus, the game will not be restarted.
	Use the name of the	ALTROOT directory as identifier.
	The full ALTROOT path shouldn't contain spaces.

	usage: ./$0 [Altroot directory, default: PB1]"
else
	PB=${1:-PB1}
	FILTER="ALTROOT=[^ ]*$PB"

	# ppid is id of parent process. This is startPitboss.sh
	# pgid is id of process group. 
	LINE=$(ps -C xvfb-run -o ppid,pgid,args |  grep -e "$FILTER" )
	PID=$(echo "${LINE}" | sed -n -e "s/^\([0-9]\+\).*$/\1/p" )
	GID=$(echo "${LINE}" | sed -n -e "s/^[^ ]\+ \([0-9]\+\).*$/\1/p" )
	NPID=$(echo ${PID} | wc -w )

	if [ "$NPID" -eq "1" ];
	then
		# Negative pid => Whole process group will be killed.
		kill -9 -$GID
		kill -9 $PID
		#return 0
	else
		echo "Can't find unique PID for '${1}'. Abort process kill."
		#return -1
	fi

fi

