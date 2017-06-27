import sys
import Civ4Shell

port = Civ4Shell.PYCONSOLE_PORT
if len(sys.argv) > 1:
    port = int(sys.argv[1])

Civ4Shell.start(port=port)
