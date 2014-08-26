#!/bin/bash
# Script for Civ4 BTS
# Add/Change a mod name in a save game.
#
# Requrement:
#  Script use xdd and hexdump
#
# Usage:
# ./convertSavesToMod.sh {New mod name or \"\"} {Name of save} [Name of converted save]



if [ "$#" -le 1 ]; then
echo "
Change the modname of a Civ4 BTS save. This does only work
if both mods are save compatible.

Usage:
./"$0" {New mod name or \"\"} {Name of save} [Name of converted save]
"
else

MODNAME="$1"
SAVE="$2"
OUTSAVE="$3"

HEXDUMPFORMAT='"" 2/1 "%02X" " "'

#Ergänze um "Mods/", falls MODNAME nicht leer
test -n "${MODNAME}" && MODNAME="Mods\\${MODNAME}\\"
test -n "${OUTSAVE}" || OUTSAVE="MOD_${SAVE}"

echo "Mod name: $MODNAME"

# Laenge des Modnamens in Hexstring von 32 bitzahl wandeln (little endian)
LENNAMEHEX=$(printf "%08x" "${#MODNAME}" | sed -e 's/^\(..\)\(..\)\(..\)\(..\)/\4\3 \2\1/')

# Name in Hex umwandeln und Rest rausfiltern.
NAMEHEX=$(echo -n "${MODNAME}" |  hexdump -e "$HEXDUMPFORMAT")

echo "Mod name as hex values:"
echo "$LENNAMEHEX" "$NAMEHEX"
echo ""

# Bestimme Länge des Modnamens im Spielstand
# O.B.d.A. ist der Modname maximal 256 Zeichen lang. (Es wird nur das niedrigste der vier Bytes gelesen)
LENNAME2HEX=$(hexdump -e "$HEXDUMPFORMAT" -s 4 -n 1 "$SAVE")
SKIP=$(echo "ibase=16;${LENNAME2HEX}+8" | bc)

#echo "Abgeschnittene Bytes des Spielstandes: $SKIP"

# Wandle Spielstand in Hex um, aber schneide vorne den Modnamen weg.
hexdump -v -e "$HEXDUMPFORMAT" -s ${SKIP} "${SAVE}" > ende.hex

# Füge vor das Save den neuen Modnamen und wandle es zurück in ein binäres Format
echo -n "2e01 0000" "$LENNAMEHEX" "$NAMEHEX" > anfang.hex
cat anfang.hex ende.hex > join.hex
xxd -r -p -u join.hex "${OUTSAVE}"


# Aufräumen
rm anfang.hex ende.hex join.hex

fi

# Ende
echo "Finish work"

