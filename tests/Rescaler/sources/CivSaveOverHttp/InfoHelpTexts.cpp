#include "asm_templates.h"
#include "InfoHelpTexts.h"

extern float Factor;
float FactorHelp = 3.0f;
float FactorHelpInv = 1.0f/FactorHelp;

/* Parse of Leaderhead info in diplo menu.

	 Call of parseHelp(): 004D074F
	 Construction Rectangle?! 007B8BA9

Assumption:
After(!) call of Replace_helpLeaderhead.trampolin
position esp+0x30 is width of label
Note: No, this does not work becaus trampolin adress is not constant.
*/
#if 1
T_REPLACE_POINTER Replace_helpLeaderhead = {(VoidFunc)0x007D34CA, NULL };
void Cv_helpLeaderhead(){
	// Hooked function no static adress. Call manually
	//Replace_helpLeaderhead.trampolin();
	__asm{
		call    dword ptr [eax+0x18]
		//call    [eax+0x18]
			//== call sub_0x007D3462
	}
	//IFMUL(0x2c, Factor);
}
#else
xxx
T_REPLACE_POINTER Replace_helpLeaderhead = {(VoidFunc)0x007B8BAE, NULL };
void Cv_helpLeaderhead(){
	IFMUL(0x0c, FactorHelp); // Change copy
	//IFMUL(0x10, FactorHelpInv);/*Gut, aber kann zu sehr schmalem Element führen. */
	IFMUL(0x44, FactorHelp); // Change origin

	Replace_helpLeaderhead.trampolin();
}
#endif

// =================================================


void hook_info_help_texts(){
#if 1
  MH_CreateHook(
      (LPVOID)Replace_helpLeaderhead.target,
      &Cv_helpLeaderhead,
			NULL);
      //reinterpret_cast<void**>((LPVOID)&Replace_helpLeaderhead.trampolin));
#endif
}
