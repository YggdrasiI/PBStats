#include "stdafx.h"

#define _MBCS
#undef _UNICODE

#include <windows.h>
#include <iostream>
#include <sstream>

#ifndef _UNICODE  
typedef std::string String;
#else
typedef std::wstring String;
#endif

std::string Webserver_Port("8080");

// Detect filename of newest exe
const std::string getExeFilename() {

	std::string names[] = {
		"Civ4BeyondSword2019.exe",
		"Civ4BeyondSword2018.exe",
		"Civ4BeyondSword2017.exe",
		"Civ4BeyondSword2016.exe",
		"Civ4BeyondSword2015.exe",
		"Civ4BeyondSword2014.exe",
		"Civ4BeyondSword.exe"
	};

	int n = sizeof(names) / sizeof(names[0]);
	for (int i = 0; i<n; ++i) {
		if (GetFileAttributesA(names[i].c_str()) != INVALID_FILE_ATTRIBUTES) {
			return names[i];
		}
	}
	return std::string("Exe not found");
}

int main(const int argc, const char * const argv[])
{

	// Find executable and append arguments
	std::stringstream argsStream("");
	int iArg = 1;

	// Exe argument (first position)
	if (argc > 1) {
		std::string userExe(argv[1]);
		if (userExe.compare(userExe.length() - 4, 4, ".exe") == 0
			&& GetFileAttributesA(userExe.c_str()) != INVALID_FILE_ATTRIBUTES) {
			argsStream << userExe;
			++iArg;
		}
		else {
			argsStream << getExeFilename();
		}
	}
	else {
		argsStream << getExeFilename();
	}

	while (iArg < argc) {
		// Port argument
		if( 0 == std::string("-P").compare(argv[iArg])){
			++iArg;
			if( iArg < argc ){
				Webserver_Port = argv[iArg];
				++iArg;
				continue;
			}
		}

		// Other arguments (mod, ALTROOT)
		argsStream << " " << argv[iArg];
		++iArg;
	}
	std::string args = argsStream.str();

	// Set port variable for other Process
	_putenv_s( "PORT", Webserver_Port.c_str());

	// Dll with modified functions, require MinHook Library
	char* dllPath = "CivSaveOverHttp.dll";

	void* pLoadLibrary = (void*)GetProcAddress(GetModuleHandleA("kernel32"), "LoadLibraryA");
	std::cout << "LoadLibrary : " << std::hex << pLoadLibrary << std::dec << std::endl;
	std::cout << "Creating process for " << args << std::endl;

	STARTUPINFOA startupInfo;
	PROCESS_INFORMATION processInformation;

	ZeroMemory(&startupInfo, sizeof(startupInfo));

	if (!CreateProcessA(0, (LPSTR)args.c_str(), 0, 0, 1, CREATE_NO_WINDOW, 0, 0, &startupInfo, &processInformation)
		)
	{
		std::cout << "Could not run BTS exe. GetLastError() = " << GetLastError() << std::endl;
		return 0;
	}

	std::cout << "Allocating virtual memory" << std::endl;
	void* pReservedSpace = VirtualAllocEx(processInformation.hProcess, NULL, strlen(dllPath), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	if (!pReservedSpace)
	{
		std::cout << "Could not allocate virtual memory. GetLastError() = " << GetLastError() << std::endl;
		return 0;
	}

	std::cout << "Writing process memory" << std::endl;
	if (!WriteProcessMemory(processInformation.hProcess, pReservedSpace, dllPath, strlen(dllPath), NULL))
	{
		std::cout << "Error while calling WriteProcessMemory(). GetLastError() = " << GetLastError() << std::endl;
		return 0;
	}

	std::cout << "Creating remote thread" << std::endl;
	HANDLE hThread = CreateRemoteThread(processInformation.hProcess, NULL, 0,
		(LPTHREAD_START_ROUTINE)pLoadLibrary, pReservedSpace, 0, NULL);
	if (!hThread)
	{
		std::cout << "Unable to create the remote thread. GetLastError() = " << GetLastError() << std::endl;
		return 0;
	}

	std::cout << "Thread created" << std::endl;

	WaitForSingleObject(hThread, INFINITE);
	VirtualFreeEx(processInformation.hProcess, pReservedSpace, strlen(dllPath), MEM_COMMIT);

	std::cout << "Done" << std::endl;
	return 0;
}
