#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path
import re

# XML file with keys for civilization releated keys.
# Second path is fallback if mod does not contain an own version of the xml file.
CIV_FILES = [(os.path.join("..", "..", "..", "Assets", "XML",
                           "Civilizations", "CIV4CivilizationInfos.xml"),
              os.path.join("..", "..", "..", "..", "..", "Assets", "XML",
                           "Civilizations", "CIV4CivilizationInfos.xml"))
            ]

CivDescKeys = set()
CivAdjectiveKeys = set()
LeaderKeys = set()

# UnitName, not used
# UnitNameKeys = set()
CityKeys = set()

def write_CvWBKeys_auto():

    civ_desc = list(CivDescKeys)
    civ_adj = list(CivAdjectiveKeys)
    leader = list(LeaderKeys)
    city = list(CityKeys)

    civ_desc.sort()
    civ_adj.sort()
    leader.sort()
    city.sort()

    text = """\
CivDescKeys = [
{civ_desc}
]
CivAdjectiveKeys = [
{civ_adj}
]
LeaderKeys = [
{leader}
]
UnitNameKeys = [ ]  # not used
CityKeys = [
{city}
]
    """.format(
        civ_desc="'" + "',\n'".join(civ_desc) + "'" if len(civ_desc) else "",
        civ_adj="'" + "',\n'".join(civ_adj) + "'" if len(civ_adj) else "",
        leader="'" + "',\n'".join(leader) + "'" if len(leader) else "",
        city="'" + "',\n'".join(city) + "'" if len(city) else "",
    )
    with open("CvWBKeys_auto.py", "w") as f:
        f.write(text)

def process_CIV4CivilizationInfos(f):
    bla = [
        {
            "reg": re.compile(".*<Description>(.*)</Description>.*"),
            "arr": CivDescKeys,
        },
        {
            "reg": re.compile(".*<ShortDescription>(.*)</ShortDescription>.*"),
            "arr": CivDescKeys,
        },
        {
            "reg": re.compile(".*<Adjective>(.*)</Adjective>.*"),
            "arr": CivAdjectiveKeys,
        },
        {
            "reg": re.compile(".*<LeaderName>(.*)</LeaderName>.*"),
            "arr": LeaderKeys,
        },
        {
            "reg": re.compile(".*<City>(.*)</City>.*"),
            "arr": CityKeys,
        },
    ]

    text = f.readline()
    while text:
        for x in bla:
            hit = x["reg"].match(text)
            if hit:
                x["arr"].add(hit.group(1))

        text = f.readline()


def load_CIV4CivilizationInfos():
    for fname in CIV_FILES[0]:
        try:
            with open(fname, "r") as f:
                process_CIV4CivilizationInfos(f)

        except FileNotFoundError:
            continue

        return

    print("Error: No existing path found for "
          "'{}'.".format(os.path.basename(fname)))


if __name__ == "__main__":
    load_CIV4CivilizationInfos()
    write_CvWBKeys_auto()

    #<City>TXT_KEY_CITY_NAME_WASHINGTON</City>
