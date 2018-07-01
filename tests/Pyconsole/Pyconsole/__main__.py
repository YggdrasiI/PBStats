import sys
import Civ4Shell

if len(sys.argv) > 2:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
    Civ4Shell.start(port=port, host=host)
elif len(sys.argv) > 1:
    port = int(sys.argv[1])
    Civ4Shell.start(port=port)
else:
    Civ4Shell.start()
