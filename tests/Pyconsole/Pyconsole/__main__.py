#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Civ4Shell

try:
    from ports_local import PORT_MAPS
except:
    PORT_MAPS = {
        "PB1": 3333,
    }


if len(sys.argv) < 2:
    print("""Usage: python {} [hostname] {{PORT or GAME NAME}}

            If no hostname is given, localhost is used.
            Fill game names into PORT_MAPS dict for easier startup.
            """.format(sys.argv[0])
    )
    sys.exit(0)


port = Civ4Shell.PYCONSOLE_PORT
if len(sys.argv) > 2:
    host = str(sys.argv[1])
    port = sys.argv[2]
elif len(sys.argv) > 1:
    port = sys.argv[1]

if port in PORT_MAPS:
    port = PORT_MAPS[port]

port = int(port)

if len(sys.argv) > 2:
    Civ4Shell.start(port=port, host=host)
else:
    Civ4Shell.start(port=port)
