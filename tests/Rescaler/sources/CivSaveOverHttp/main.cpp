#include "MinHook.h"
#if defined _M_X64
#pragma comment(lib, "MinHook.x64.lib")
#elif defined _M_IX86
#pragma comment(lib, "MinHook.x86.lib")
#endif

#include "SaveTransfer.h"
#include "DrawingFunctions.h"
#include "DiploMenu.h"

#include "main.h"

// ===== Hooking setup =====

extern "C" BOOL APIENTRY DllMain(HINSTANCE hinstDLL, DWORD dwReason, LPVOID lpvReserved)
{
	switch (dwReason)
	{
		case DLL_PROCESS_ATTACH:
			{
				change_diplo_menu_constants();
				MH_Initialize();

        hook_save_tranfer();
        hook_drawing_functions();
        hook_diplo_menu();

				MH_EnableHook(MH_ALL_HOOKS);
			}
			break;
		case DLL_PROCESS_DETACH:
			MH_DisableHook(MH_ALL_HOOKS);
			MH_Uninitialize();
			break;
		case DLL_THREAD_ATTACH:
			break;
		case DLL_THREAD_DETACH:
			break;
	}
	return true;
}


