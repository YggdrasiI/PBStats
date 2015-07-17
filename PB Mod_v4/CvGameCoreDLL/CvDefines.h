#pragma once

#ifndef CVDEFINES_H
#define CVDEFINES_H

// defines.h

// The following #defines should not be moddable...

#define MOVE_IGNORE_DANGER										(0x00000001)
#define MOVE_SAFE_TERRITORY										(0x00000002)
#define MOVE_NO_ENEMY_TERRITORY								(0x00000004)
#define MOVE_DECLARE_WAR											(0x00000008)
#define MOVE_DIRECT_ATTACK										(0x00000010)
#define MOVE_THROUGH_ENEMY										(0x00000020)
#define MOVE_MAX_MOVES											(0x00000040)

#define RANDPLOT_LAND													(0x00000001)
#define RANDPLOT_UNOWNED											(0x00000002)
#define RANDPLOT_ADJACENT_UNOWNED							(0x00000004)
#define RANDPLOT_ADJACENT_LAND								(0x00000008)
#define RANDPLOT_PASSIBLE											(0x00000010)
#define RANDPLOT_NOT_VISIBLE_TO_CIV						(0x00000020)
#define RANDPLOT_NOT_CITY											(0x00000040)

#ifdef _USRDLL
//#define MAX_CIV_PLAYERS												(18)
#define MAX_CIV_PLAYERS												(52)
// Set this value to 18 for 18->52 player conversion.
#define MAX_CIV_PLAYERS2												(18)
#else
#define MAX_CIV_PLAYERS												(CvGlobals::getInstance().getMaxCivPlayers())
#define MAX_CIV_PLAYERS2												(CvGlobals::getInstance().getMaxCivPlayers())
#endif

#define MAX_CIV_TEAMS													(MAX_CIV_PLAYERS)
#define MAX_PLAYERS														(MAX_CIV_PLAYERS + 1)
#define MAX_TEAMS															(MAX_PLAYERS)
#define BARBARIAN_PLAYER											((PlayerTypes)MAX_CIV_PLAYERS)
#define BARBARIAN_TEAM												((TeamTypes)MAX_CIV_TEAMS)

// Derived values for MAX_CIV_PLAYERS2 (=18)
#define MAX_CIV_TEAMS2													(MAX_CIV_PLAYERS2)
#define MAX_PLAYERS2														(MAX_CIV_PLAYERS2 + 1)
#define MAX_TEAMS2															(MAX_PLAYERS2)
#define BARBARIAN_PLAYER2											((PlayerTypes)MAX_CIV_PLAYERS2)
#define BARBARIAN_TEAM2												((TeamTypes)MAX_CIV_TEAMS2)

// TODO: Should be a variable to change this at runtime
#define expand_arrays													(1)
// Read b values into array and fill up with A-b default values, b<A
// Moreover swap values of POINTER+A and POINTER+b (=>swap barbarian slots)
#define READ_ARRAY(STREAM, A, b, DEFAULT_VALUE, POINTER) \
	if( (expand_arrays) ){ \
	(STREAM)->Read(b, (POINTER) ); \
	*(POINTER+A-1) = *(POINTER+b-1); \
	for( int rai=b-1; rai<A-1; ++rai){ *( (POINTER) + rai ) = DEFAULT_VALUE }\
	}else{\
		(STREAM)->Read(A,(POINTER) ); \
	}

#define READ_STRING_ARRAY(STREAM, A, b, POINTER) \
	if( (expand_arrays) ){ \
	(STREAM)->ReadString(b, (POINTER) ); \
	*(POINTER+A-1) = *(POINTER+b-1); \
	*(POINTER+b-1) = ""; \
	}else{\
		(STREAM)->Read(A,(POINTER) ); \
	}

#define SWAP_BARBARIAN(POINTER) \
	if( (expand_arrays) ){ \
		*((POINTER)+ (BARBARIAN_PLAYER)) ^= *((POINTER) +(BARBARIAN_PLAYER2)); \
		*((POINTER)+(BARBARIAN_PLAYER2)) ^= *((POINTER)+(BARBARIAN_PLAYER)); \
		*((POINTER)+ (BARBARIAN_PLAYER)) ^= *((POINTER) +(BARBARIAN_PLAYER2)); \
	}

#define REPLACE_BARBARIAN(POINTER) \
	if( (expand_arrays) && *(POINTER) == (BARBARIAN_PLAYER2) ){ \
		*(POINTER) = (BARBARIAN_PLAYER); \
	}

// Char Count limit for edit boxes
#define PREFERRED_EDIT_CHAR_COUNT							(15)
#define MAX_GAMENAME_CHAR_COUNT								(32)
#define MAX_PLAYERINFO_CHAR_COUNT							(32)
#define MAX_PLAYEREMAIL_CHAR_COUNT						(64)
#define MAX_PASSWORD_CHAR_COUNT								(32)
#define MAX_GSLOGIN_CHAR_COUNT								(17)
#define MAX_GSEMAIL_CHAR_COUNT								(50)
#define MAX_GSPASSWORD_CHAR_COUNT							(30)
#define MAX_CHAT_CHAR_COUNT										(256)
#define MAX_ADDRESS_CHAR_COUNT								(64)

#define INVALID_PLOT_COORD										(-(MAX_INT))	// don't use -1 since that is a valid wrap coordinate
#define DIRECTION_RADIUS											(1)
#define DIRECTION_DIAMETER										((DIRECTION_RADIUS * 2) + 1)
#define NUM_CITY_PLOTS												(21)
#define CITY_HOME_PLOT												(0)
#define CITY_PLOTS_RADIUS											(2)
#define CITY_PLOTS_DIAMETER										((CITY_PLOTS_RADIUS*2) + 1)

#define GAME_NAME															("Game")

#define LANDSCAPE_FOW_RESOLUTION							(4)
															
#define Z_ORDER_LAYER													(-0.1f)
#define Z_ORDER_LEVEL													(-0.3f)

#define CIV4_GUID															"civ4bts"
#define CIV4_PRODUCT_ID												11081
#define CIV4_NAMESPACE_ID											17
#define CIV4_NAMESPACE_EXT										"-tk"

#define MAP_TRANSFER_EXT											"_t"

#define USER_CHANNEL_PREFIX										"#civ4buser!"

#define SETCOLR																L"<color=%d,%d,%d,%d>"
#define ENDCOLR																L"</color>"
#define NEWLINE																L"\n"
#define SEPARATOR															L"\n-----------------------"
#define TEXT_COLOR(szColor)										((int)(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString(szColor)).getColor().r * 255)), ((int)(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString(szColor)).getColor().g * 255)), ((int)(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString(szColor)).getColor().b * 255)), ((int)(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString(szColor)).getColor().a * 255))

// Version Verification files and folders
#ifdef _DEBUG
#define CIV4_EXE_FILE													".\\Civ4BeyondSword_DEBUG.exe"
#define CIV4_DLL_FILE													".\\Assets\\CvGameCoreDLL_DEBUG.dll"
#else
#define CIV4_EXE_FILE													".\\Civ4BeyondSword.exe"
#define CIV4_DLL_FILE													".\\Assets\\CvGameCoreDLL.dll"
#endif
#define CIV4_SHADERS													".\\Shaders\\FXO"
#define CIV4_ASSETS_PYTHON										".\\Assets\\Python"
#define CIV4_ASSETS_XML												".\\Assets\\XML"

#define MAX_PLAYER_NAME_LEN										(64)
#define MAX_VOTE_CHOICES											(8)
#define VOTE_TIMEOUT													(600000)	// 10 minute vote timeout - temporary

#define ANIMATION_DEFAULT											(1)			// Default idle animation

// python module names
#define PYDebugToolModule			"CvDebugInterface"
#define PYScreensModule				"CvScreensInterface"
#define PYCivModule						"CvAppInterface"
#define PYWorldBuilderModule	"CvWBInterface"
#define PYPopupModule					"CvPopupInterface"
#define PYDiplomacyModule			"CvDiplomacyInterface"
#define PYUnitControlModule		"CvUnitControlInterface"
#define PYTextMgrModule				"CvTextMgrInterface"
#define PYPerfTestModule			"CvPerfTest"
#define PYDebugScriptsModule	"DebugScripts"
#define PYPitBossModule				"PbMain"
#define PYTranslatorModule		"CvTranslator"
#define PYGameModule					"CvGameInterface"
#define PYEventModule					"CvEventInterface"
#define PYRandomEventModule					"CvRandomEventInterface"

#endif	// CVDEFINES_H
