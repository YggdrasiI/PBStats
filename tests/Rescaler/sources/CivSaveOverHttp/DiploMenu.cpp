#include "asm_templates.h"
#include "DiploMenu.h"

DiploMenuRescaling diploMenu;

/* Map (x,y,w,h) on 
 * (s*x, t*y, s*w, t*h) - ((s-1)mid_x, (t-1)mid_y, 0, 0)
 *
 */
void transformRect(const float s, const float t,
    const Rect &midpoint, 
    const Rect &source,
    Rect &dest){
  //dest.x = int(s * source.x - (s-1)*midpoint.x);
  //dest.y = int(t * source.y - (t-1)*midpoint.y);
	//offsets
  dest.x = int(s * (source.x - midpoint.x) - ( source.x - midpoint.x));
  dest.y = int(t * (source.y - midpoint.y) - ( source.y - midpoint.y));
  dest.w = int(s * source.w);
  dest.h = int(t * source.h);
}

void DiploMenuRescaling::setup(){
	const Rect midpoint = {1920/2, 1080/2, 0, 0};
	/* Note: The (x,y) coordinate depends from resolution.
	 * This given default values was evaluated for 1920x1080.
	 * => x,y should be used as offsets to get 
	 *    resolution independend changes. 
	 * */
	const Rect default_leftTop = {0x1C7, 0x0AE, 0x102, 0x1F9};
	const Rect default_leftBottom = {0x1C7, 0x2A7, 0x102, 0x0E8};
	const Rect default_rightTop = {0x4B6, 0x0AE, 0x102, 0x1F9};
	const Rect default_rightBottom = {0x4B6, 0x2A7, 0x102, 0x0E8};

	const Rect default_midHeadline = {0x2CF, 0x0AE, 0x1E1, 0x2B};
	const Rect default_midCenter = {0x2CF, 0x0D9, 0x1E1, 0x1CE};
	//const Rect default_midLeaderhead = {0x2CF, 0x0D9, 0x1C4, 0x161};
	const Rect default_midBottom = {0x2CF, 0x2A7, 0x1E1, 0xE8};

	transformRect( factorHeight, factorHeight, midpoint, 
			default_leftTop, leftTop);
	transformRect( factorHeight, factorHeight, midpoint, 
			default_leftBottom, leftBottom);
	transformRect( factorHeight, factorHeight, midpoint, 
			default_rightTop, rightTop);
	transformRect( factorHeight, factorHeight, midpoint, 
			default_rightBottom, rightBottom);

	transformRect( factorHeight, factorHeight, midpoint, 
			default_midHeadline, midHeadline);
	transformRect( factorHeight, factorHeight, midpoint, 
			default_midCenter, midCenter);
	transformRect( factorHeight, factorHeight, midpoint, 
			default_midBottom, midBottom);

	//Apply extra width change of left and right slide
	leftTop.x -= extraWidthSides;
	leftTop.w += extraWidthSides;
	leftBottom.x -= extraWidthSides;
	leftBottom.w += extraWidthSides;
	rightTop.w += extraWidthSides;
	rightBottom.w += extraWidthSides;
}

/* DiploMenu: Left top element
 * Free register: eax
 *
 * Data: x,y,w,h from esp+0x38 to esp+0x44
 * Default values: see stack trace
 * Stack trace:
 0012FBC0 					esp
 0012FBF8 dd       1C7h ; Ã
 0012FBFC dd       0AEh ; «
 0012FC00 dd       102h
 0012FC04 dd       1F9h
 * 
 */
T_REPLACE_POINTER Replace_DipLeftTop = {(VoidFunc)0x0057F4E0, NULL };
void Cv_DipLeftTop(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x3c, eax, ecx, diploMenu.leftTop.x)
			IIADD(0x40, eax, ecx, diploMenu.leftTop.y)
			pop ecx
	}
	//COPY(0x38, eax, diploMenu.leftTop.x);
	//COPY(0x3c, eax, diploMenu.leftTop.y);
	COPY(0x40, eax, diploMenu.leftTop.w);
	COPY(0x44, eax, diploMenu.leftTop.h);

	Replace_DipLeftTop.trampolin();
}

/* DiploMenu: Left bottom element
 *
 * Note: Similar to above.
 * Stack trace:
 0012FBC0 					esp
 0012FBF8 dd       1C7h ; Ã
 0012FBFC dd       2A7h ; º
 0012FC00 dd       102h
 0012FC04 dd       0E8h ; Þ
 * 
 */
T_REPLACE_POINTER Replace_DipLeftBottom = {(VoidFunc)0x0057F59B, NULL };
void Cv_DipLeftBottom(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x3c, eax, ecx, diploMenu.leftBottom.x)
			IIADD(0x40, eax, ecx, diploMenu.leftBottom.y)
			pop ecx
	}
	//COPY(0x38, eax, diploMenu.leftBottom.x);
	//COPY(0x3c, eax, diploMenu.leftBottom.y);
	COPY(0x40, eax, diploMenu.leftBottom.w);
	COPY(0x44, eax, diploMenu.leftBottom.h);

	Replace_DipLeftBottom.trampolin();
}

/* DiploMenu: Right top element
 *
 * Note: Similar to above.
 * Stack trace:
 0012FBC0 					esp
 0012FBF8 dd       4B6h ; Â
 0012FBFC dd       0AEh ; «
 0012FC00 dd       102h
 0012FC04 dd       1F9h ; ¨
 */
T_REPLACE_POINTER Replace_DipRightTop = {(VoidFunc)0x0057F656, NULL };
void Cv_DipRightTop(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x3c, eax, ecx, diploMenu.rightTop.x)
			IIADD(0x40, eax, ecx, diploMenu.rightTop.y)
			pop ecx
	}
	//COPY(0x38, eax, diploMenu.rightTop.x);
	//COPY(0x3c, eax, diploMenu.rightTop.y);
	COPY(0x40, eax, diploMenu.rightTop.w);
	COPY(0x44, eax, diploMenu.rightTop.h);

	Replace_DipRightTop.trampolin();
}

/* DiploMenu: Right bottom element
 *
 * Note: Similar to above.
 * Stack trace:
 0012FBC0 					esp
 0012FBF8 dd       4B6h ; Â
 0012FBFC dd       2A7h ; º
 0012FC00 dd       102h
 0012FC04 dd       0E8h ; Þ
 */
T_REPLACE_POINTER Replace_DipRightBottom = {(VoidFunc)0x0057F713, NULL };
void Cv_DipRightBottom(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x3c, eax, ecx, diploMenu.rightBottom.x)
			IIADD(0x40, eax, ecx, diploMenu.rightBottom.y)
			pop ecx
	}
	//COPY(0x38, eax, diploMenu.rightBottom.x);
	//COPY(0x3c, eax, diploMenu.rightBottom.y);
	COPY(0x40, eax, diploMenu.rightBottom.w);
	COPY(0x44, eax, diploMenu.rightBottom.h);

	Replace_DipRightBottom.trampolin();
}

/* DiploMenu: Headline in MP branch
 * Free register: eax
 *
 * Data: x,y,w,h from esp+0x30 to esp+0x3c
 * Default values: 0x2CF, 0x0AE, 0x1E1, 0x2B
 */
T_REPLACE_POINTER Replace_DipMidHeadline_MP = {(VoidFunc)0x0058CE53, NULL };
void Cv_DipMidHeadline_MP(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x34, eax, ecx, diploMenu.midHeadline.x)
			IIADD(0x38, eax, ecx, diploMenu.midHeadline.y)
			pop ecx
	}
	//COPY(0x30, eax, diploMenu.midHeadline.x);
	//COPY(0x34, eax, diploMenu.midHeadline.y);
	COPY(0x38, eax, diploMenu.midHeadline.w);
	COPY(0x3c, eax, diploMenu.midHeadline.h);
	Replace_DipMidHeadline_MP.trampolin();
}

T_REPLACE_POINTER Replace_DipMidHeadline_SP = {(VoidFunc)0x0055496C, NULL };
void Cv_DipMidHeadline_SP(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x34, eax, ecx, diploMenu.midHeadline.x)
			IIADD(0x38, eax, ecx, diploMenu.midHeadline.y)
			pop ecx
	}
	//COPY(0x30, eax, diploMenu.midHeadline.x);
	//COPY(0x34, eax, diploMenu.midHeadline.y);
	COPY(0x38, eax, diploMenu.midHeadline.w);
	COPY(0x3c, eax, diploMenu.midHeadline.h);
	Replace_DipMidHeadline_SP.trampolin();
}

/* DiploMenu: Center in MP branch
 * Free register: eax
 *
 * Data: x,y,w,h from esp+0x30 to esp+0x3c
 * Default values: 0x2CF, 0x0D9, 0x1E1, 0x1CE
 */
T_REPLACE_POINTER Replace_DipMidCenter_MP = {(VoidFunc)0x0058D71F, NULL };
void Cv_DipMidCenter_MP(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x34, eax, ecx, diploMenu.midCenter.x)
			IIADD(0x38, eax, ecx, diploMenu.midCenter.y)
			pop ecx
	}
	//COPY(0x30, eax, diploMenu.midCenter.x);
	//COPY(0x34, eax, diploMenu.midCenter.y);
	COPY(0x38, eax, diploMenu.midCenter.w);
	COPY(0x3c, eax, diploMenu.midCenter.h);
	Replace_DipMidCenter_MP.trampolin();
}

/* DiploMenu: Leaderhead a.k.a. center in SP branch
 * Free register: eax, edx
 *
 * Data: x,y, decoration_x, decoration_y from esp+0x34 to esp+0x40
 * Default values: see stack trace
 *
 * Note: The rescaling will be done by an other hook, see Cv_addLeaderheadGFC.
 * Note: Finally, it proves as same like Cv_DipMidCenter_MP
 * Stack trace:
 0012FC5C esp
 0012FC90 dd       2CFh ; ¤
 0012FC94 dd       0D9h ; +
 0012FC98 dd       1E1h ; ß
 0012FC9C dd       1CEh ; +
 * 
 */
T_REPLACE_POINTER Replace_DipMidCenter_SP = {(VoidFunc)0x005521F2, NULL };
void Cv_DipMidCenter_SP(){
	__asm{
		//push ecx
			IIADD(0x34, edx, eax, diploMenu.midCenter.x)
			IIADD(0x38, edx, eax, diploMenu.midCenter.y)
			//pop ecx
	}
	//COPY(0x34, edx, diploMenu.midCenter.x);
	//COPY(0x38, edx, diploMenu.midCenter.y);
	// Decoration handle
	/*
	__asm{
		IFMUL(0x3C, diploMenu.factorHeight)
		IFMUL(0x40, diploMenu.factorHeight)
	}*/
	COPY(0x3c, eax, diploMenu.midCenter.w);
	COPY(0x40, eax, diploMenu.midCenter.h);

	Replace_DipMidCenter_SP.trampolin();
}

/*
 * The above hook scales the container of the leaderhead. This
 *	disturb the center position of the animation, which will be fixed 
 *	by this offset change a few instructions later.
 *
 *	Lattest instrutions was:
.text:0055220B                 push    6
.text:0055220D                 push    0
.text:0055220F                 push    0
.text:00552211                 push    5
.text:00552213                 push    40h
 * We change the 0x40.
 */
T_REPLACE_POINTER Replace_DipLeaderhead_RestoreCenter = {(VoidFunc)0x00552215, NULL };
void Cv_DipLeaderhead_RestoreCenter(){
	//(40,5) *= scale
	IFMUL(0x00, diploMenu.factorHeight)
	IFMUL(0x04, diploMenu.factorHeight)
	Replace_DipLeaderhead_RestoreCenter.trampolin();
}


/* DiploMenu: Bottom in MP variant
 * Free register: eax
 *
 * Data: x,y,w,h from esp+0x30 to esp+0x3c
 * Default values: 0x2CF, 0x2A7, 0x1E1, 0xE8
 */
T_REPLACE_POINTER Replace_DipMidBottom_MP = {(VoidFunc)0x0058D966, NULL };
void Cv_DipMidBottom_MP(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x34, eax, ecx, diploMenu.midBottom.x)
			IIADD(0x38, eax, ecx, diploMenu.midBottom.y)
			pop ecx
	}
	//COPY(0x30, eax, diploMenu.midBottom.x);
	//COPY(0x34, eax, diploMenu.midBottom.y);
	COPY(0x38, eax, diploMenu.midBottom.w);
	COPY(0x3c, eax, diploMenu.midBottom.h);
	Replace_DipMidBottom_MP.trampolin();
}

/* DiploMenu: Bottom in SP variant
 * Free register: eax, edi
 *
 * Data: x,y,w,h from esp+0x48 to esp+0x50
 * Default values: 0x2CF, 0x2A7, 0x1E1, 0xE8
 *
 * Note: Different offset from esp as mp variant!
 */
T_REPLACE_POINTER Replace_DipMidBottom_SP = {(VoidFunc)0x005541FC, NULL };
void Cv_DipMidBottom_SP(){
	// Use pre-evaluated values...
	__asm{
		push ecx
			IIADD(0x48, eax, ecx, diploMenu.midBottom.x)
			IIADD(0x4c, eax, ecx, diploMenu.midBottom.y)
			pop ecx
	}
	//COPY(0x30, eax, diploMenu.midBottom.x);
	//COPY(0x34, eax, diploMenu.midBottom.y);
	COPY(0x4c, eax, diploMenu.midBottom.w);
	COPY(0x50, eax, diploMenu.midBottom.h);
	Replace_DipMidBottom_SP.trampolin();
}

// ==== WIP Tests ====

#define ENABLE_TEST1 1
#if ENABLE_TEST1
/* Exe Button/Label rect
 * Achtung, hier ist man so weit innen, dass jeder faktor n-mal anwegendet
 * wird mit wechselndem n...
 * */
/*
T_REPLACE_POINTER Replace_Test1 = {(VoidFunc)0x007AE5F0, NULL };
	IFMUL(0x0c, fTest1)	// w
	IFMUL(0x10, fTest1)	// h
	*/


T_REPLACE_POINTER Replace_Test1 = {(VoidFunc)0x00552215, NULL };
void Cv_Test1(){
	__asm { 
		pop eax
			push 0x80
	}
	Replace_Test1.trampolin();
}
#endif

// =================================================


void change_diplo_menu_constants(){
	diploMenu.factorHeight = 1.25f;
	diploMenu.extraWidthSides = 200;
	diploMenu.setup();
}

void hook_diplo_menu(){
  MH_CreateHook(
      (LPVOID)Replace_DipLeftTop.target,
      &Cv_DipLeftTop,
      reinterpret_cast<void**>((LPVOID)&Replace_DipLeftTop.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_DipLeftBottom.target,
      &Cv_DipLeftBottom,
      reinterpret_cast<void**>((LPVOID)&Replace_DipLeftBottom.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_DipRightTop.target,
      &Cv_DipRightTop,
      reinterpret_cast<void**>((LPVOID)&Replace_DipRightTop.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_DipRightBottom.target,
      &Cv_DipRightBottom,
      reinterpret_cast<void**>((LPVOID)&Replace_DipRightBottom.trampolin));

  MH_CreateHook(
      (LPVOID)Replace_DipMidHeadline_SP.target,
      &Cv_DipMidHeadline_SP,
      reinterpret_cast<void**>((LPVOID)&Replace_DipMidHeadline_SP.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_DipMidCenter_SP.target,
      &Cv_DipMidCenter_SP,
      reinterpret_cast<void**>((LPVOID)&Replace_DipMidCenter_SP.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_DipLeaderhead_RestoreCenter.target,
      &Cv_DipLeaderhead_RestoreCenter,
      reinterpret_cast<void**>((LPVOID)&Replace_DipLeaderhead_RestoreCenter.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_DipMidBottom_SP.target,
      &Cv_DipMidBottom_SP,
      reinterpret_cast<void**>((LPVOID)&Replace_DipMidBottom_SP.trampolin));

  MH_CreateHook(
      (LPVOID)Replace_DipMidHeadline_MP.target,
      &Cv_DipMidHeadline_MP,
      reinterpret_cast<void**>((LPVOID)&Replace_DipMidHeadline_MP.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_DipMidCenter_MP.target,
      &Cv_DipMidCenter_MP,
      reinterpret_cast<void**>((LPVOID)&Replace_DipMidCenter_MP.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_DipMidBottom_MP.target,
      &Cv_DipMidBottom_MP,
      reinterpret_cast<void**>((LPVOID)&Replace_DipMidBottom_MP.trampolin));

#if ENABLE_TEST1
  MH_CreateHook( (LPVOID)Replace_Test1.target,
      &Cv_Test1,
      reinterpret_cast<void**>((LPVOID)&Replace_Test1.trampolin));
#endif
}
