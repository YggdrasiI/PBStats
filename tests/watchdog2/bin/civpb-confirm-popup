#!/bin/bash
#

if [ "$1" = "-h" ] ; 
then
	echo "
	Detects xvfb-display of Pitboss game and sends 'Return' keystroke
	to active window of this framebuffer. This should be used to
	close popups of 'save errors'.
	Use the name of the	ALTROOT directory as identifier of your game.
	The full ALTROOT path shouldn't contain spaces.
	Requires xdotool.

	Security note: Use 'auth merge [Magic cookie file]' to allow xdotool
	the usage of the framebuffer. The current version of startPitboss.sh
	already contain this line. The cookie should be stored in /tmp/$PB.

	Usage: ./$0 [Altroot directory, default: PB1]"
else
	PB=${1:-PB1}

	# Find display for this game.
	PB_DISPLAY=$(xauth -n -f /tmp/${PB} list)
	PB_DISPLAY="${PB_DISPLAY%% *}"
	PB_DISPLAY=${PB_DISPLAY:=:0} #Optional, use :0 as default value
	PB_DISPLAY=":${PB_DISPLAY##*:}"

	# Title of popup was received by
	# DISPLAY=:100 xwininfo -children -root
	PB_POPUP_TITLE="Save Error"

	if [ -n "${PB_DISPLAY}" ]; 
	then
		DISPLAY=$PB_DISPLAY xdotool search --onlyvisible --name "${PB_POPUP_TITLE}" key --window %1 Return
	else
		echo "Display not found."
	fi

fi

