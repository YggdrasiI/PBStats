=== Installation of precompiled version (32 bit) ===

1. Install WinPcap  from 
   http://www.winpcap.org/install/bin/WinPcap_4_1_3.exe 
   I do not know if 'Load Driver at Startup' is ness...

2. Open Terminal and run the executable. Add the port range
   of your pitboss servers as arguments.

3. Select the network device to track after startup.
	This index can be propagte as third argument, too.


=== Compiling with Code::Blocks and GCC-Compiler ===

0. Install Code::Blocks with GCC-Compiler, i.e
		http://sourceforge.net/projects/codeblocks/files/Binaries/13.12/Windows/codeblocks-13.12mingw-setup.exe/download

1. Download WinPcap_4_1_2.zip from 
   http://www.winpcap.org/install/bin/WpdPack_4_1_2.zip
   and extract it into this directory. This should
   produce the directory structure
   ./PitbossSniffer
   ./WdpPack

2. Open the Project file PitbossSniffer/PitbossSniffer.cbp
   with CodeBlocks. The dependencies to Wincap are configured
   as relative paths. Thus, you should be able to compile it
   without further steps....


=== Author ===
Olaf Schulz, 2014
