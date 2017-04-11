#ifndef __HOOK_H__
#define __HOOK_H__

/* Headers for GUI Rescaling. */
typedef void (*VoidFunc)(); //use argument-less stub for all hooks.
struct T_REPLACE_POINTER{
	VoidFunc target;
	VoidFunc trampolin;
};

struct Rect {
	int x,y,w,h;
};

#endif
