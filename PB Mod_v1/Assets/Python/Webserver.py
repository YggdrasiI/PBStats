## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
#
# Pitboss admin framework
# Dan McGarry 3-24-05
#

# This file is only a stub in this Mod. The main content 
# can be found in 'PBs/Python'

from CvPythonExtensions import *
import sys
import string
gc = CyGlobalContext()

# Extra path for extra python modules
pythonDir = gc.getAltrootDir()+'\\..\\Python\\'
#sys.path.append(pythonDir)
execfile(pythonDir + '\\Webserver.py')


