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

1. As Player:  
• Copy BTS_Wrapper.exe and the three DLLs of this folder into your
Civ4:BTS installation folder. Do not delete/move the normal executable. It's still required.
• Start your game with the wrapper, i.e.
'BTS_Wrapper.exe mod= "PB Mod_v4"\"'.

• If MSVCP100.dll is missing, see http://answers.microsoft.com/en-us/windows/forum/windows_other-performance/msvcp100dll-missing/9a687c31-0619-4ee9-b511-020985e29b5f


2. As Pitboss host ( with Linux in mind):
Assume that your current Altroot folder for the server is $HOME/PBs/PB1
and your server has the ip 1.2.3.4. The follwing steps try to fit some paths/urls
into matching pairs.

• Setup a webserver and prepare a folder for your PB saves and allow symlinks.
Example path: /var/www/PBs

• Create a folder which encodes the IP/url of your server. The syntax is "_url_[ip|url]".
Move the Altroot folder into this directory.
Example path: $HOME/_url_1.2.3.4/PBs/PB1.

=> At runtime Civ4 will stores the save games into 
Z:\home\$USERNAME\_url_1.2.3.4\PBs\PB1\Saves\pitboss\auto.

• Create the directory /var/www/PBs/PB1/Save/ and place a symbolic link into the above pitboss directory.

Now, the save games are public available. If a modified client connects, it converts
_url_1.2.3.4/ into http[s]//1.2.3.4/ and try to download the file. If the download fails
the save will transfered normally.

If it does not work re-check the setup of your paths.


=== Sources ===
The sources for two Code::Blocks projects can be found in ./sources.
Moreover, you need the following libraries:
• MinHook, https://github.com/TsudaKageyu/minhook/
• Curl, https://github.com/bagder/curl


Olaf Schulz, 2015

