Linux variant of second script for faster login into PB games.

In the default configuraiton, it just speeds up logins on pb.zulan.net.
Extend the included list of urls if you host your own games.

Dependecies & Setup:

1. Install fuse for Python
	sudo apt-get install pip
	sudo pip install fusepy

2. Remap your z:-Drive of wine
  Create a folder e.g. '~/.wine/PBdrive',
  call 'winecfg' and connect drive 'z:' with the new folder.

	Note that you cann not use an other drive letter but 'z:'!

3. Create a mount point for the downloaded files, e.g.
		'~/.wine/PBdownloads'

Usage:
  python ./pb_downloader.py "~/.wine/PBdownloads" "~/.wine/PBdrive"
