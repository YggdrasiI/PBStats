=== The problem ===
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
• Copy BTS_Wrapper.exe, *.dll and *.lib files of this folder into your
Civ4:BTS installation folder. Do not delete/move the normal executable. It's still required.
• Start your game with the wrapper, i.e.
'BTS_Wrapper.exe mod= "PB Mod_v7"\"'.

• If MSVCP100.dll is missing, see http://answers.microsoft.com/en-us/windows/forum/windows_other-performance/msvcp100dll-missing/9a687c31-0619-4ee9-b511-020985e29b5f

2a) As Direct IP host (new in version 3 of BTS_Wrapper.exe)
• Add '-P [port number, i.e. 2055]' argument to the start arguments of BTS_Wrapper.exe.
	This port will be used to transfer the save game.
• Extend the port forwarding of Civ4 on the new port. This step depends on your network settings. 

2b) As Pitboss host (the old way / with Linux in mind):
• Assume that your current Altroot folder for the server is $HOME/PBs/PB1
	and your server has the ip 1.2.3.4. The follwing steps try to fit some paths/urls
into matching pairs.

• Setup a webserver and prepare a folder for your PB saves and allow symlinks.
Example path: /var/www/PBs

• Create a folder which encodes the IP/url of your server. The syntax is "_http_[ip|url]" (or "_https_[ip|url]").
Move the Pitboss Altroot folder into this directory.
Example path: $HOME/_http_1.2.3.4/PBs/PB1.

=> At runtime Civ4 will stores the save games into 
Z:\home\$USERNAME\_http_1.2.3.4\PBs\PB1\Saves\pitboss\auto.

• Create the directory /var/www/PBs/PB1/Save/ and place a symbolic link into the above pitboss directory.

Now, the save games are public available. If a modified client connects, it converts
_http_1.2.3.4/ into http://1.2.3.4/ and try to download the file
http://1.2.3.4/PBs/PB1/Saves/pitboss/auto/Recovery_{nickname}.CivBeyondSwordSave.
If the download fails the save will transfered normally.

If it does not work re-check the setup of your paths.


=== Sources ===
The sources and project files for Visual Studio 2017 can be found in ./sources_v3.
Used following libraries:
• MinHook, https://github.com/TsudaKageyu/minhook/
• Curl, https://github.com/bagder/curl
• LibMicroHTTPD, http://www.gnu.org/software/libmicrohttpd/


=== P.S. ===
Less flexible, but without any modifcation of the Civ4 executable, you could also mount the http folder with the saves into your local filesystem. If the save path on the client equals the path on the server it will be loaded over this way.

Example set of paths for BTS_Wrapper.exe and Webdav usage:

Public http folder with Webdav support: http://{server}/{prefix}
Altroot directory on Server: /home/$USERNAME/_http_{server}/{path}/PBs/PB1.
Save folder (Wine Syntax): Z:\home\$USERNAME\_http_{server}\{prefix}\PBs\PB1\Saves\pitboss\auto.
Url of saves: http://{server}/{prefix}/home/$USERNAME/_http_{server}/{path}/PBs/PB1/Saves/pitboss/auto

=>
1. A BTS_Wrapper.exe user profits from the '_http_'-syntax. Civ4 download the save over http.
2. If the user maps Z: drive  to http://{server}/{prefix} server and client share the same path syntax. Civ4 reads the save from Z:.

Olaf Schulz, 2015-17

