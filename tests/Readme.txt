Civ4BeyondSword2015.exe:
  Bugfix of a wrong written url. The Civ4:BTS multiplayer lobby should now work.

Civ4BeyondSword2014.exe:
Civ4BeyondSword_Pitboss2014.exe:
	Modified executable where almost all gamespy domain names was replaced
	by a new domain. The new domain refers to Zulan's server which host
	a NAT service as gamespy replacement.
	This patch unlock the Direct IP mode again and fix statup issues of
	the Pitboss application, too.

	Data of Zulan's server:
	IP: 148.251.130.188
	DNS:
	civ4bts.natneg1.g.zulan.net
	civ4bts.natneg2.g.zulan.net
	civ4bts.natneg3.g.zulan.net
	civ4bts.available.g.zulan.net
	motd.g.zulan.net ( For http lookup. Server replys '404' )


Civ4BeyondSword2014.exe.patch:
	Open the command line and navigate to your BTS executeable.
	Create the patched EXE with
	bspatch Civ4BeyondSword.exe Civ4BeyondSword2014.exe Civ4BeyondSword2014.exe.patch

	Windows:
	Windows-Version of bsdiff is available here
	http://sites.inka.de/tesla/download/bsdiff4.3-win32.zip

	Linux:
	The default softwarerepository of your distrubution should
	contain the tool bspatch.

