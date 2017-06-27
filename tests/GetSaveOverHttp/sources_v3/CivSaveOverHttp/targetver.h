#pragma once

// #define this before any windows headers are included
//#define WIN_XP
#ifdef WIN_XP
// Deprecated....
#define _WIN32_WINNT _WIN32_WINNT_WINXP // xp, but no InetNtop function
#else
#define _WIN32_WINNT _WIN32_WINNT_WIN7 // Windows 8.0
//#endif
#include <SDKDDKVer.h>
#endif

