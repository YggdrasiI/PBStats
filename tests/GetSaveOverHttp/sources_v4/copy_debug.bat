copy BTS_Wrapper\Debug\BTS_Wrapper.exe Debug\.
copy BTS_Wrapper\Debug\CivSaveOverHttp.dll Debug\.
pause
copy "Debug\*" "I:\Olaf\Civ4\Beyond the Sword\"
pause

rem copy BTS_Wrapper\Debug\BTS_Wrapper.exe "I:\Olaf\Civ4\Beyond the Sword\"
rem copy BTS_Wrapper\Debug\CivSaveOverHttp.dll "I:\Olaf\Civ4\Beyond the Sword\"
rem pause

cd I:\Olaf\Civ4\Beyond the Sword\
BTS_Wrapper.exe mod= PB Mod_v7 -P 2055
pause

