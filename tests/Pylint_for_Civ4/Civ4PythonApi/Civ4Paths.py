import os.path

# Defaults
CIV4 = "C:\\Civ4"
MOD = os.path.join(CIV4, "Beyond the Sword", "Mods", "PieAncientEuropeV")

#..........

def civ4_paths(civ4=CIV4, mod=MOD):
    dirs = [
        ".",
        os.path.join(mod, "Assets", "Python"),
        os.path.join(civ4, "Beyond the Sword", "Assets", "Python"),
        os.path.join(civ4, "Warlords", "Assets", "Python"),
        os.path.join(civ4, "Assets", "Python"),
        # Python 2.4 with wx, etc
        os.path.join(civ4, "Warlords", "Assets", "Python", "System"),
    ]

    o = []
    for d in dirs:
        os.path.walk(d, lambda arg, path, files: arg.append(path), o)

    return o

# import sys
# sys.path.extend(civ4_paths())
