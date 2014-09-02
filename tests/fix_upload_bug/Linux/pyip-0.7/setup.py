"""pyip: assemble/disassemble raw ip packet

pyip is a Python package offering assembling/disassembling of raw ip packet,
including ip, udp, and icmp. Also it includes 2 utilities based on raw ip, 
traceroute and ping.

The primary motivation for this project is to fill the blank in Python,
i.e., handling raw ip packet. Meanwhile, the utility 'traceroute' is intended 
to be port of Unix 'traceroute' to Windows platform, as Windows' tracert has 
only very limited command line options compared with Unix 'traceroute'.
"""

classifiers = """\
License :: OSI Approved :: Python Software Foundation License
Intended Audience :: Developers
Development Status :: 3 - Alpha
Topic :: Internet
Topic :: System :: Networking
Programming Language :: Python
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
"""

from distutils.core import setup
import sys

if sys.version_info < (2, 3):
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)

doclines = __doc__.split("\n")

setup(name="pyip",
      version="0.7",
      maintainer="Kenneth Jiang",
      maintainer_email="kenneth.jiang@gmail.com",
      url = "https://sourceforge.net/projects/pyip",
      license = "Standard Python License",
      platforms = ["any"],
      py_modules = ['icmp', 'inetutils', 'ping', 'traceroute', 'udp', 'ip', ],
      description = doclines[0],
      classifiers = filter(None, classifiers.split("\n")),
      long_description = "\n".join(doclines[2:]),
      )
