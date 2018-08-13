#include "stdafx.h"

#define _MBCS
#undef _UNICODE

#include <iostream>
#include <sstream>
#include <assert.h>

// To share saves in DirectIP mode
//#include <winsock2.h>
//#include <Ws2tcpip.h>
//#pragma comment(lib, "Ws2_32.lib")
#define WITH_WEBSERVER

#include <windows.h>

#include "RemoteOps.h"

#ifndef _UNICODE  
typedef std::string String;
#else
typedef std::wstring String;
#endif

//std::string sWebserver_Port("8080");
std::string sWebserver_Port("-1");  // Disabled
int Webserver_Port = atoi(sWebserver_Port.c_str());

// Detect filename of newest exe
const std::string getExeFilename() {

    std::string names[] = {
        "Civ4BeyondSword2020.exe",
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
#ifdef WITH_WEBSERVER
        // Filter out port arguments (-P [port])
        if( 0 == std::string("-P").compare(argv[iArg])){
            ++iArg;
            if( iArg < argc ){
                sWebserver_Port = argv[iArg];
                Webserver_Port = atoi(sWebserver_Port.c_str());
                ++iArg;
                continue;
            }
        }
#endif

        // Other arguments (mod, ALTROOT)
        argsStream << " " << argv[iArg];
        ++iArg;
    }
    std::string args = argsStream.str();

    // Dll with modified functions, requires MinHook Library
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
    HANDLE hThread = CreateRemoteThread(processInformation.hProcess, NULL, 1,
            (LPTHREAD_START_ROUTINE)pLoadLibrary, pReservedSpace, 0, NULL);
    if (!hThread)
    {
        std::cout << "Unable to create the remote thread. GetLastError() = " << GetLastError() << std::endl;
        return 0;
    }

    std::cout << "Thread created" << std::endl;

    WaitForSingleObject(hThread, INFINITE);
    VirtualFreeEx(processInformation.hProcess, pReservedSpace, strlen(dllPath), MEM_COMMIT);


    // Get return value of remote call of LoadLibrary by reading GetExitCodeThread
    // We need this value for calls of GetRemoteProcAddress later...
    // NOTE: Unfortunately this doesn’t work for 64bit processes! GetExitCodeThread returns a 32bit value; in a 64bit process, LoadLibrary will return a 64bit value.
    DWORD exitCode;
    if( !GetExitCodeThread(hThread, &exitCode) ){
        std::cout << "Unable to get exit code of remote thread. GetLastError() = " << GetLastError() << std::endl;

        return 0;
    }
    HMODULE dllHandleRemote = (HMODULE) exitCode;

#ifdef WITH_WEBSERVER
    if( Webserver_Port > -1 ){
        //2. Start Webserver as remote thread in the other process
        //2.0 get position of function StartServer in CivSaveOverHttp.dll 
        void * pStartServerRemote = (void *) /*FARPROC*/ GetRemoteProcAddress (processInformation.hProcess, dllHandleRemote, "StartServer");

        /* NOTE: Above differs from address determined by this process, i.e... */
        /*
           HMODULE dllHandle = LoadLibraryEx(dllPath, NULL, DONT_RESOLVE_DLL_REFERENCES);
           void* pStartServer = (void*)GetProcAddress(dllHandle, "StartServer");
           std::cout << "StartServer : " << std::hex << pStartServer << std::dec << std::endl;
           */
        std::cout << "StartServer: " << std::hex << pStartServerRemote << std::dec << std::endl;

        if( pStartServerRemote ){
            //2.1 Transfer the port argument into other address space
            std::cout << "Allocating virtual memory (2)" << std::endl;
            void* pReservedSpace2 = VirtualAllocEx(processInformation.hProcess, NULL,
                    strlen(sWebserver_Port.c_str()), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
            if (!pReservedSpace2)
            {
                std::cout << "Could not allocate virtual memory. GetLastError() = " << GetLastError() << std::endl;
                return 0;
            }

            std::cout << "Writing process memory (2)" << std::endl;
            if (!WriteProcessMemory(processInformation.hProcess, pReservedSpace2,
                        sWebserver_Port.c_str(), strlen(sWebserver_Port.c_str()), NULL))
            {
                std::cout << "Error while calling WriteProcessMemory(). GetLastError() = " << GetLastError() << std::endl;
                return 0;
            }

            //2.2 Call startServer(port)
            std::cout << "Creating remote thread (2)" << std::endl;
            HANDLE hThread2 = CreateRemoteThread(processInformation.hProcess, NULL, 0,
                    (LPTHREAD_START_ROUTINE)pStartServerRemote, pReservedSpace2, 0, NULL);
            if (!hThread2)
            {
                std::cout << "Unable to create the remote thread. GetLastError() = " << GetLastError() << std::endl;
                return 0;
            }

            std::cout << "Thread created (2)" << std::endl;

            WaitForSingleObject(hThread2, INFINITE);
            VirtualFreeEx(processInformation.hProcess, pReservedSpace2, strlen(sWebserver_Port.c_str()), MEM_COMMIT);
        }
    }
#endif

    //============================================
    // Propagate calling arguments for Log
    void * pSetStartArgsRemote = (void *) /*FARPROC*/ GetRemoteProcAddress (processInformation.hProcess, dllHandleRemote, "SetStartArgs");

    if( pSetStartArgsRemote ){
        // Transfer the args string into other address space
        void* pReservedSpaceArgs = VirtualAllocEx(processInformation.hProcess, NULL, args.length(), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
        if (!pReservedSpace)
        {
            std::cout << "Could not allocate virtual memory. GetLastError() = " << GetLastError() << std::endl;
            return 0;
        }
        if (!WriteProcessMemory(processInformation.hProcess, pReservedSpaceArgs, args.c_str(), args.length(), NULL))
        {
            std::cout << "Error while calling WriteProcessMemory(). GetLastError() = " << GetLastError() << std::endl;
            return 0;
        }

        // Call SetStartArgs(pArgs)
        HANDLE hThreadArgs = CreateRemoteThread(processInformation.hProcess, NULL, 0,
                (LPTHREAD_START_ROUTINE)pSetStartArgsRemote, pReservedSpaceArgs, 0, NULL);
        if (!hThreadArgs)
        {
            std::cout << "Unable to create the remote thread. GetLastError() = " << GetLastError() << std::endl;
            return 0;
        }
        WaitForSingleObject(hThreadArgs, INFINITE);
        VirtualFreeEx(processInformation.hProcess, pReservedSpaceArgs, args.length(), MEM_COMMIT);
    }
    //============================================

    std::cout << "Done" << std::endl;
    return 0;
}

