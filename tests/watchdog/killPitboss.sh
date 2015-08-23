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

list_instances () {
	echo "
	List of running games:"
	GAMES=$(ps -ao ppid,pgid,args | grep -e "Civ4BeyondSword" | grep -v -e " wine " | grep -e "ALTROOT=" )
	echo "Name		  PID  GID"
	GAMES=$( echo "$GAMES" | sed -n -e "s/^\([0-9]\+\)[ ]\+\([0-9]\+\).*ALTROOT=[^ ]*[\]\([^ \]*\).*/\3\t\t\1  \2/p" )
	echo "$GAMES"
}

kill_instance () {

	PB=${1}
	FILTER="ALTROOT=[^ ]*[\]$PB"

	# Second grep filtering out the xvfb-run lines
	LINE=$(ps -au | grep -e "Civ4BeyondSword" | grep -v -e " wine " | grep -e "$FILTER" )
	PID=$(echo "${LINE}" | sed -n -e "s/^[^ ]*[ ]\+\([0-9]\+\).*$/\1/p" )
	NPID=$(echo ${PID} | wc -w )

	if [ "$NPID" -eq "1" ];
	then
		echo "Kill $PB, PID=$PID"
		kill -9 $PID
		if [ "$2" = "-p" ] ;
		then
			ALTROOT=$(echo ${LINE##*ALTROOT=Z:})
			ALTROOT=${ALTROOT//\\/\/}
			#echo "Linux altroot: ${ALTROOT}"
			load_previous_save "$ALTROOT"
		fi
	else
		echo "Can't find unique PID for '${PB}'. Abort process kill."
		echo "$LINE"
	fi
}

kill_script () {
	PB=${1}
	FILTER="ALTROOT=[^ ]*[\]$PB"

	# ppid is id of parent process. This is startPitboss.sh
	# pgid is id of process group. 
	LINE=$(ps -C xvfb-run -o ppid,pgid,args |  grep -e "$FILTER" )
	PID=$(echo "${LINE}" | sed -n -e "s/^\([0-9]\+\).*$/\1/p" )
	GID=$(echo "${LINE}" | sed -n -e "s/^[^ ]\+ \([0-9]\+\).*$/\1/p" )
	NPID=$(echo ${PID} | wc -w )

	if [ "$NPID" -eq "1" ];
	then
		echo "Kill startup script of $PB, PID=$PID, GID=$GID"
		# Negative pid => Whole process group will be killed.
		kill -9 -$GID
		sleep 1
		kill -9 $PID
		#return 0
	else
		echo "Can't find unique PID for '${PB}'. Abort process kill."
		#return -1
	fi
}

if [ "$1" = "-h" ] ; 
then
	echo "
	Kill wine process of Pitboss game to invoke restart.
	Use the name of the ALTROOT directory as identifier.
	The full ALTROOT path should not contain spaces.

	Usage: 
	$0 -l			List instances
	$0 [-p] {instance} 	Kill executable, -p for previous save
	$0 -s {instance}	Kill looping script (no restart)
	"
	exit 0
fi

if [ "$1" = "-l" ] ; 
then 
	list_instances;
	exit 0
fi

if [ "$1" = "-s" ] ; 
then 
	kill_script "$2" 
else
	kill_instance "$2" "$1" 
fi
exit 0
