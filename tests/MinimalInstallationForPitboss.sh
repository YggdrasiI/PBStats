#!/bin/bash
# Creates minimal set of files for a pitboss server
# Add your mods manually.

if [ $# -le 1 ] ; 
then
	echo "Usage: ./$0 {Path to Civ4 folder} {Path to new, reduced Copy}"
else
	#Append / for rsync 
	SRC="$1/"
	DST="$2"

	echo "Create set of files for minimal installation in $DST."
	echo "The script creates no output if no error occurs."

	# 1. Copy files
	rsync -r --exclude 'CvGameCoreDLL' --exclude "*.wav" --exclude "*.mp3" --exclude 'Mods' "$SRC" "$DST"

	# 2. Replace art files with empty files. At least one of these files is required for
	# the startup of the pitboss executable !
	find "$DST/Assets/Art" "$2/Warlords/Assets/Art" "$2/Beyond the Sword/Assets/Art" -name "*.*" -delete -exec touch {} \; # -print

	# 3. Finish message
	echo "Finish. Disk usage of $DST:"
	du -hs "$DST"

fi
