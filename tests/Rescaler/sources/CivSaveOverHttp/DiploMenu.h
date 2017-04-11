#ifndef __DIPLO_MENU_H__
#define __DIPLO_MENU_H__

#include "MinHook.h"
#include "hook.h"

void change_diplo_menu_constants();
void hook_diplo_menu();

class DiploMenuRescaling {
	public:
		//float factorWidthMid;
		float factorHeight;
		int extraWidthSides;
		DiploMenuRescaling():
			factorHeight(1.0f),
			extraWidthSides(100){
			}
		void setup();
		// Derived values. x,y are offset values.
		Rect leftTop;
		Rect leftBottom;
		Rect rightTop;
		Rect rightBottom;
		Rect midHeadline;
		Rect midBottom;
		Rect midCenter;
};

#endif // __DIPLO_MENU_H__
