﻿=== The problem ===
The network code of Civ4:BTS limits the bandwidth to ancient 10kB/sec, 
but advanced saves consume a few MB. This leads to long timeouts during the login… 


=== The solution ===
Release the file transfer from Civ4 to an external library. The
external library downloads the save over http (or https) and redirects all (=4)  
file handles of Civ4 onto this file.
We wrote a wrapper executable which handle this for you!


=== How to use it ===
It requires changes on both (client & server) sides.

1) As Player:  
• Copy BTS_Wrapper.exe and *.dll files of this folder into your
Civ4:BTS installation folder. Do not delete/move the normal executable. It's still required.
• Start your game with the wrapper, i.e.
'BTS_Wrapper.exe mod= "PB Mod_v8"\"'.

• If MSVCP100.dll is missing, see http://answers.microsoft.com/en-us/windows/forum/windows_other-performance/msvcp100dll-missing/9a687c31-0619-4ee9-b511-020985e29b5f

• On Linux+Wine: If the vcruntime140.dll file can not be loaded: Delete local vcruntime140.dll and run 'winetricks vcrun2015' to install other(?) version.

2a) As Direct IP host (new in version 3 of BTS_Wrapper.exe)
• Add '-P [port number, i.e. 2055]' argument to the start arguments of BTS_Wrapper.exe.
	This port will be used to transfer the save game.
• Extend the port forwarding of Civ4 on the new port. This step depends on your network settings. 

2b) As Pitboss host (the old way / with Linux in mind):
The tricky part is the encoding of the server ip into the data, provided to the clients, if they loading the save.
• Assume that your current Altroot folder for the server is $HOME/PBs/PB1
	and your server has the ip 1.2.3.4. The following steps try to fit some paths/urls
into matching pairs.

• Setup a webserver and prepare a folder for your PB saves and allow symlinks.
Example path: /var/www/PBs

• Create a folder which encodes the IP/url of your server. The syntax is "_http_[ip|url]" (or "_https_[ip|url]").
Move the Pitboss Altroot folder into this directory.
Example path: $HOME/_http_1.2.3.4/PBs/PB1.

=> At runtime Civ4 will store the save games into 
Z:\home\$USERNAME\_http_1.2.3.4\PBs\PB1\Saves\pitboss\auto (Windows path syntax) .

• Create the directory /var/www/PBs/PB1/Save/ and place a symbolic link into the above pitboss directory.

Now, the save games are public available. If a modified client connects, it converts
_http_1.2.3.4/ into http://1.2.3.4/ and try to download the file
http://1.2.3.4/PBs/PB1/Saves/pitboss/auto/Recovery_{nickname}.CivBeyondSwordSave.
If the download fails the save will transfered normally.

If it does not work re-check the setup of your paths.


=== Sources ===
The sources and project files for Visual Studio 2017 can be found in ./sources_v4.
Used following libraries:
• MinHook, https://github.com/TsudaKageyu/minhook/
• Curl, https://github.com/bagder/curl
• LibMicroHTTPD, http://www.gnu.org/software/libmicrohttpd/


=== P.S. ===
Less flexible, but without any modifcation of the Civ4 executable, you could also mount the http folder with the saves into your local filesystem.
If the save path on the client equals the path on the server it will be loaded over the file system!

Example set of paths for parallel BTS_Wrapper.exe and Webdav usage:

Assume a public http folder with Webdav support: http://{server}/{prefix}
Altroot directory on Linux-Server: /home/$USERNAME/_http_{server}/{path}/PBs/PB1.
This altroot resolves to the following save folder (Wine Syntax): Z:\home\$USERNAME\_http_{server}\{prefix}\PBs\PB1\Saves\pitboss\auto.
Moreover, the 'pitboss/auto' folder should be accessable ofer this Url: http://{server}/{prefix}/{path}/PBs/PB1/Saves/pitboss/auto

Benefits of this setup:
1. A BTS_Wrapper.exe user profits from the '_http_'-syntax of the folder. Civ4 will download the save over http.
2. If a user maps the Z:-drive to http://{server}/{prefix} both, server and client, uses the same path syntax! Thus, Civ4 will read the saves from Z:.

Olaf Schulz, 2015-20

