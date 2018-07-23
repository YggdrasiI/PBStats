#include "CvGameCoreDLL.h"

#include "CvGameCoreDLLUndefNew.h"

#include <new>

// PB Mod
#include <cstdlib>
#include <string.h>
#include <iostream>

#pragma comment(lib, "Ole32.lib")
#pragma comment(lib, "OleAut32.lib")
// PB Mod END


#include "CvGlobals.h"
#include "FProfiler.h"
#include "CvDLLInterfaceIFaceBase.h"

//
// operator global new and delete override for gamecore DLL 
//
void *__cdecl operator new(size_t size)
{
	if (gDLL)
	{
		return gDLL->newMem(size, __FILE__, __LINE__);
	}
	return malloc(size);
}

void __cdecl operator delete (void *p)
{
	if (gDLL)
	{
		gDLL->delMem(p, __FILE__, __LINE__);
	}
	else
	{
		free(p);
	}
}

void* operator new[](size_t size)
{
	if (gDLL)
		return gDLL->newMemArray(size, __FILE__, __LINE__);
	return malloc(size);
}

void operator delete[](void* pvMem)
{
	if (gDLL)
	{
		gDLL->delMemArray(pvMem, __FILE__, __LINE__);
	}
	else
	{
		free(pvMem);
	}
}

void *__cdecl operator new(size_t size, char* pcFile, int iLine)
{
	return gDLL->newMem(size, pcFile, iLine);
}

void *__cdecl operator new[](size_t size, char* pcFile, int iLine)
{
	return gDLL->newMem(size, pcFile, iLine);
}

void __cdecl operator delete(void* pvMem, char* pcFile, int iLine)
{
	gDLL->delMem(pvMem, pcFile, iLine);
}

void __cdecl operator delete[](void* pvMem, char* pcFile, int iLine)
{
	gDLL->delMem(pvMem, pcFile, iLine);
}


void* reallocMem(void* a, unsigned int uiBytes, const char* pcFile, int iLine)
{
	return gDLL->reallocMem(a, uiBytes, pcFile, iLine);
}

unsigned int memSize(void* a)
{
	return gDLL->memSize(a);
}

BOOL APIENTRY DllMain(HANDLE hModule, 
					  DWORD  ul_reason_for_call, 
					  LPVOID lpReserved)
{
	switch( ul_reason_for_call ) {
	case DLL_PROCESS_ATTACH:
		{
		// The DLL is being loaded into the virtual address space of the current process as a result of the process starting up 
		OutputDebugString("DLL_PROCESS_ATTACH\n");

		// set timer precision
		MMRESULT iTimeSet = timeBeginPeriod(1);		// set timeGetTime and sleep resolution to 1 ms, otherwise it's 10-16ms
		FAssertMsg(iTimeSet==TIMERR_NOERROR, "failed setting timer resolution to 1 ms");
		}
		break;
	case DLL_THREAD_ATTACH:
		// OutputDebugString("DLL_THREAD_ATTACH\n");
		break;
	case DLL_THREAD_DETACH:
		// OutputDebugString("DLL_THREAD_DETACH\n");
		break;
	case DLL_PROCESS_DETACH:
		OutputDebugString("DLL_PROCESS_DETACH\n");
		timeEndPeriod(1);
		GC.setDLLIFace(NULL);
		break;
	}
	
	return TRUE;	// success
}

//
// enable dll profiler if necessary, clear history
//
void startProfilingDLL()
{
	if (GC.isDLLProfilerEnabled())
	{
		gDLL->ProfilerBegin();
	}
}

//
// dump profile stats on-screen
//
void stopProfilingDLL()
{
	if (GC.isDLLProfilerEnabled())
	{
		gDLL->ProfilerEnd();
	}
}

// PB Mod

int StringToWString(std::wstring &ws, const std::string &s)
{
	std::wstring wsTmp(s.begin(), s.end());
	ws = wsTmp;
	return 0;
}

int CharToWString(std::wstring &ws, const char *chars)
{
	std::string s(chars);
	return StringToWString(ws, s);
}

/* Return folder of this DLL/EXE.
 *
 * Free returned char after usage! */
const char *get_dll_folder(){

#define MAX_PARAM 1000
	//char path[MAX_PARAM];
	char *path = (char *)calloc( (MAX_PARAM + 1), sizeof(char));
	path[0] = '\0';
	HMODULE hm = NULL;

	if (!GetModuleHandleExA( /*0x04 | 0x02*/ GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
				(LPCSTR) &get_dll_folder,
				&hm))
	{
		int ret = GetLastError();
		fprintf(stderr, "GetModuleHandle returned %d\n", ret);
	}
	GetModuleFileNameA(hm, path, MAX_PARAM /*sizeof(path)*/);

	// path variable should now contain the full filepath to localFunc
	// Strip dll filename.
	char *last_slash = strrchr(path, '\\');
	*last_slash = '\0';
	fprintf(stdout, "%s\n", path);

	return path;
}

/* Wrapper to System libraries to unzip file.
 *
 * BSTR is a wchar-array prefixed by its length...
 * */
// Ok ==> 0, Error ==> 1
bool Unzip2Folder( BSTR lpZipFile, BSTR lpFolder)
{
//#define LOG(MSG) std::cout << MSG << std::endl;
#define LOG(MSG) gDLL->logMsg("PythonErr.log", MSG)

	//LOG( ((const TCHAR *)lpZipFile)+1); // nö...
	//LOG( ((const TCHAR *)lpFolder)+1);

	IShellDispatch *pISD;

	Folder  *pZippedFile = 0L;
	Folder  *pDestination = 0L;

	long FilesCount = 0;
	IDispatch* pItem = 0L;
	FolderItems *pFilesInside = 0L;

	VARIANT Options, OutFolder, InZipFile, Item;
	CoInitialize( NULL);
	__try{
		if (CoCreateInstance(CLSID_Shell, NULL, CLSCTX_INPROC_SERVER, IID_IShellDispatch, (void **)&pISD) != S_OK){
			LOG("Instance creation failed.");
			return 1;
		}

		InZipFile.vt = VT_BSTR;
		InZipFile.bstrVal = lpZipFile;
		pISD->NameSpace( InZipFile, &pZippedFile);
		if (!pZippedFile)
		{
			pISD->Release();
			LOG("Zip file not found.");
			return 1;
		}

		OutFolder.vt = VT_BSTR;
		OutFolder.bstrVal = lpFolder;
		pISD->NameSpace( OutFolder, &pDestination);
		if(!pDestination)
		{
			pZippedFile->Release();
			pISD->Release();
			LOG("Outfolder argument invalid.");
			return 1;
		}

		pZippedFile->Items(&pFilesInside);
		if(!pFilesInside)
		{
			pDestination->Release();
			pZippedFile->Release();
			pISD->Release();
			LOG("Can not create file list.");
			return 1;
		}

		pFilesInside->get_Count( &FilesCount);
		if( FilesCount < 1)
		{
			pFilesInside->Release();
			pDestination->Release();
			pZippedFile->Release();
			pISD->Release();
			LOG("Zip file empty.");
			return 0;
		}

		pFilesInside->QueryInterface(IID_IDispatch,(void**)&pItem);

		Item.vt = VT_DISPATCH;
		Item.pdispVal = pItem;

		Options.vt = VT_I4;
		Options.lVal = 1024 | 512 | 16 | 4;//http://msdn.microsoft.com/en-us/library/bb787866(VS.85).aspx

		bool retval = pDestination->CopyHere( Item, Options) != S_OK;

		pItem->Release();pItem = 0L;
		pFilesInside->Release();pFilesInside = 0L;
		pDestination->Release();pDestination = 0L;
		pZippedFile->Release();pZippedFile = 0L;
		pISD->Release();pISD = 0L;

		return retval;

	}__finally
	{
		CoUninitialize();
	}
}

// PB Mod END
