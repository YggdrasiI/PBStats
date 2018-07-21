copy BTS_Wrapper\Release\BTS_Wrapper.exe Release\.
copy BTS_Wrapper\Release\CivSaveOverHttp.dll Release\.
copy Lib\libmicrohttpd-dll.dll Release\.
pause

copy "Release\*" "I:\Olaf\Civ4\Beyond the Sword\"
pause

cd I:\Olaf\Civ4\Beyond the Sword\
BTS_Wrapper.exe mod= PB Mod_v7 -P 2055
pause

