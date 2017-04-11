#include "asm_templates.h"
#include "DrawingFunctions.h"
#include "DiploMenu.h"

/* Global rescaling factor */
//float Factor = 0.75f;
float Factor = 1.0f;
extern DiploMenuRescaling diploMenu;

// =================================================


/* Overview of functions */
/*
T_REPLACE_POINTER Replace_setLabel = {NULL, NULL};
T_REPLACE_POINTER Replace_setDimensions = {NULL, NULL};
T_REPLACE_POINTER Replace_addTableControlGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addModelGraphicGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_setTextAt = {NULL, NULL};
T_REPLACE_POINTER Replace_attachTableControlGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_moveItem = {NULL, NULL};
T_REPLACE_POINTER Replace_setLabelAt = {NULL, NULL};
T_REPLACE_POINTER Replace_setHelpLabel = {NULL, NULL};
T_REPLACE_POINTER Replace_addGraphData = {NULL, NULL};
T_REPLACE_POINTER Replace_setTableColumnHeader = {NULL, NULL};
T_REPLACE_POINTER Replace_addFlagWidgetGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addReligionMovieWidgetGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_initMinimap = {NULL, NULL};
*/
T_REPLACE_POINTER Replace_addListBoxGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addScrollPanel = {NULL, NULL};
T_REPLACE_POINTER Replace_setPanelSize = {NULL, NULL};
T_REPLACE_POINTER Replace_addCheckBoxGFCAt = {NULL, NULL};
T_REPLACE_POINTER Replace_addLineGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addDDSGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_setHelpTextArea = {NULL, NULL};
T_REPLACE_POINTER Replace_setImageButton = {NULL, NULL};
T_REPLACE_POINTER Replace_addSpaceShipWidgetGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addEditBoxGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_attachMultiListControlGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addImprovementGraphicGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addStackedBarGFCAt = {NULL, NULL};
T_REPLACE_POINTER Replace_setButtonGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_attachSlider = {NULL, NULL};
T_REPLACE_POINTER Replace_setExitText = {NULL, NULL};
T_REPLACE_POINTER Replace_addUnitGraphicGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addMultiListControlGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_setImageButtonAt = {NULL, NULL};
T_REPLACE_POINTER Replace_addSlider = {NULL, NULL};
T_REPLACE_POINTER Replace_addPlotGraphicGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addStackedBarGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addDropDownBoxGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addSimpleTableControlGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addDrawControlAt = {NULL, NULL};
T_REPLACE_POINTER Replace_addSpecificUnitGraphicGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addGraphWidget = {NULL, NULL};
T_REPLACE_POINTER Replace_addDDSGFCAt = {NULL, NULL};
T_REPLACE_POINTER Replace_addTableControlGFCWithHelp = {NULL, NULL};
T_REPLACE_POINTER Replace_addDrawControl = {NULL, NULL};
T_REPLACE_POINTER Replace_addPanel = {NULL, NULL};
T_REPLACE_POINTER Replace_addMultilineText = {NULL, NULL};
//T_REPLACE_POINTER Replace_addLeaderheadGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_attachPanelAt = {NULL, NULL};
T_REPLACE_POINTER Replace_addCheckBoxGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addMultiListControlGFCAt = {NULL, NULL};
T_REPLACE_POINTER Replace_attachCheckBoxGFC = {NULL, NULL};
T_REPLACE_POINTER Replace_addBuildingGraphicGFC = {NULL, NULL};
//T_REPLACE_POINTER Replace_ = {NULL, NULL};


/* PythonApi:
 * VOID setText (
 * STRING szName, STRING szAtttachTo, STRING szText, INT uiFlags,
 * FLOAT fX, FLOAT fY, FLOAT fZ, FontType eFont,
 * WidgetType eType, INT iData1, INT iData2)

Ida, CyGInterfaceScreen-Function with above header ( |XREF|=1 ):

.text:004E7030 ; ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦ S U B R O U T I N E ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
.text:004E7030
.text:004E7030
.text:004E7030 sub_4E7030      proc near               ; DATA XREF: sub_718D50+316o
.text:004E7030
.text:004E7030 var_C           = dword ptr -0Ch
.text:004E7030 var_4           = dword ptr -4
.text:004E7030 arg_0           = dword ptr  4
.text:004E7030 arg_4           = dword ptr  8
.text:004E7030 arg_8           = dword ptr  0Ch
.text:004E7030 arg_24          = dword ptr  28h
.text:004E7030 arg_28          = dword ptr  2Ch
.text:004E7030 arg_2C          = dword ptr  30h
.text:004E7030 arg_30          = dword ptr  34h
.text:004E7030 arg_34          = dword ptr  38h
.text:004E7030 arg_38          = dword ptr  3Ch
.text:004E7030 arg_3C          = dword ptr  40h
.text:004E7030 arg_40          = dword ptr  44h

This routine push 11 arguments to the stack and then
calls this one. Is this CvGInterfaceScreen::setText(?) ?!

.text:00570E70 ; ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦ S U B R O U T I N E ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
.text:00570E70
.text:00570E70
.text:00570E70 sub_570E70      proc near               ; CODE XREF: sub_41C120+389p
.text:00570E70                                         ; sub_41C120+428p ...
.text:00570E70
.text:00570E70 var_C           = dword ptr -0Ch
.text:00570E70 var_4           = dword ptr -4
.text:00570E70 arg_0           = dword ptr  4
.text:00570E70 arg_4           = dword ptr  8
.text:00570E70 arg_C           = dword ptr  10h
.text:00570E70 arg_28          = dword ptr  2Ch
.text:00570E70 arg_2C          = dword ptr  30h
.text:00570E70 arg_30          = dword ptr  34h
.text:00570E70 arg_3C          = dword ptr  40h
.text:00570E70 arg_40          = dword ptr  44h

 * Call point: 0x00570E70
 * Critical offsets: 30, 34
*/

T_REPLACE_POINTER Replace_setText = {(VoidFunc)0x00570E70, NULL };
void Cv_setText(){
	FFMUL(0x30, Factor); // x
	FFMUL(0x34, Factor); // y

	Replace_setText.trampolin();
}

/* PythonApi:
 * VOID setLabel (
 * STRING szName, STRING szAttachTo, STRING szText, INT uiFlags,
 * FLOAT fX, FLOAT fY, FLOAT fZ, FontType eFont,
 * WidgetType eType, INT iData1, INT iData2)
 *
 *
 * Call point: 0x00570F90 (Cv)
 * Critical offsets: 0x30, 34
 *
 * Note: Alternative for Cy_setLabel were
 * Call point: 0x004E7170
 * Critical offsets: 2C, 30
 */
T_REPLACE_POINTER Replace_setLabel = {(VoidFunc)0x00570F90, NULL };
void Cv_setLabel(){
	FFMUL(0x30, Factor);
	FFMUL(0x34, Factor);

	Replace_setLabel.trampolin();
}

/* PythonApi:
 * VOID setDimensions (
 * INT iX, INT iY, INT iWidth, INT iHeight)
 *
 * (Cv-Call, not used)
 * Call point: 0x0055F9D0
 * Critical offsets: 10, 14, (18, 1C)
 *
 * Note: Only the first two arguments (top left corner) will be used.
 * Other values in eax, ecx but tested in subroutine.
 *
 *  (Cy-Call)
 * Call point: 0x004EA030
 * Critical offsets: 0x04, 0x08, 0x0C, 0x10,
 *
 * TODO
 */
T_REPLACE_POINTER Replace_setDimensions = {(VoidFunc)0x004EA030, NULL };
void Cv_setDimensions(){
	IFMUL(0x04, Factor);	// x
	IFMUL(0x08, Factor);	// y
	IFMUL(0x0C, Factor);	// w
	IFMUL(0x10, Factor);	// h
#if 0
	// Test. IIADD mess up register?!
	IIADD(0x04, eax, ecx, -200);
	IIADD(0x08, eax, ecx, -0);
	//IIADD8(0x0d, -200);
	//IIADD8(0x10, -0);
#endif

	Replace_setDimensions.trampolin();
}

/* PythonApi:
 * VOID addTableControlGFC (
 * STRING szName, INT numColumns, INT iX, INT iY,
 * INT iWidth, INT iHeight, BOOL bIncludeHeaders, BOOL bDrawGrid,
 * INT iconWidth, INT iconHeight, TableStyle style)
 *
 * Call point: 0x005717C0
 * Critical offsets: 0x10, 14, 18, 1C
 */
T_REPLACE_POINTER Replace_addTableControlGFC = {(VoidFunc)0x005717C0, NULL };
void Cv_addTableControlGFC(){
	IFMUL(0x10, Factor);	// x
	IFMUL(0x14, Factor);	// y
	IFMUL(0x18, Factor);	// w
	IFMUL(0x1C, Factor);	// h

	Replace_addTableControlGFC.trampolin();
}

/* PythonApi:
 * VOID addModelGraphicGFC (
 * STRING szName, STRING szFile, INT iX, INT iY,
 * INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1,
 * INT iData2, FLOAT fxRotation, FLOAT fzRotation, FLOAT fScale)
 *
 * Call point: 0x005683B0
 * Critical offsets: 0x0C, 10, 14, 18
 */
T_REPLACE_POINTER Replace_addModelGraphicGFC = {(VoidFunc)0x005683B0, NULL };
void Cv_addModelGraphicGFC(){
	IFMUL(0x0C, Factor);	// x
	IFMUL(0x10, Factor);	// y
	IFMUL(0x14, Factor);	// w
	IFMUL(0x18, Factor);	// h

	Replace_addModelGraphicGFC.trampolin();
}

/* PythonApi:
 * VOID setTextAt (
 * STRING szName, STRING szAttachTo, STRING szText, INT uiFlags,
 * FLOAT fX, FLOAT fY, FLOAT fZ, FontType eFont,
 * WidgetType eType, INT iData1, INT iData2)
 *
 * Call point: 00570F00
 * Critical offsets: 0x30, 34
 */
T_REPLACE_POINTER Replace_setTextAt = {(VoidFunc)0x005683B0, NULL };
void Cv_setTextAt(){
	FFMUL(0x30, Factor);	// x
	FFMUL(0x34, Factor);	// y

	Replace_setTextAt.trampolin();
}

/* PythonApi:
 * VOID attachTableControlGFC (
 * STRING szAttachTo, STRING szName, INT numColumns, BOOL bIncludeHeaders,
 * BOOL bDrawGrid, INT iconWidth, INT iconHeight, TableStyle style)
 *
 * Call point: 0x00561E30
 * Critical offsets: 0x18, 22
 */
T_REPLACE_POINTER Replace_attachTableControlGFC = {(VoidFunc)0x00561E30, NULL };
void Cv_attachTableControlGFC(){
	IFMUL(0x18, Factor);	// w
	IFMUL(0x22, Factor);	// h

	Replace_attachTableControlGFC.trampolin();
}

/* PythonApi:
 * VOID moveItem (
 * STRING szName, FLOAT fX, FLOAT fY, FLOAT fZ)
 *
 * Call point: 0x0055E0A0
 * Critical offsets: 4, 8
 */
T_REPLACE_POINTER Replace_moveItem = {(VoidFunc)0x0055E0A0, NULL };
void Cv_moveItem(){
	FFMUL(0x04, Factor);	// x
	FFMUL(0x08, Factor);	// y

	Replace_moveItem.trampolin();
}

/* PythonApi:
 * VOID setLabelAt (
 * STRING szName, STRING szAttachTo, STRING szText, INT uiFlags,
 * FLOAT fX, FLOAT fY, FLOAT fZ, FontType eFont,
 * WidgetType eType, INT iData1, INT iData2)
 *
 * Call point: 0x005710D0
 * Critical offsets: 0x30, 34
 */
T_REPLACE_POINTER Replace_setLabelAt = {(VoidFunc)0x005710D0, NULL };
void Cv_setLabelAt(){
	FFMUL(0x30, Factor);	// x
	FFMUL(0x34, Factor);	// y

	Replace_setLabelAt.trampolin();
}

/* PythonApi:
 * VOID setHelpLabel (
 * STRING szName, STRING szAtttachTo, STRING szText, INT uiFlags,
 * FLOAT fX, FLOAT fY, FLOAT fZ, FontType eFont,
 * STRING szHelpText)
 *
 * Call point: 0x00571020
 * Critical offsets: 0x30, 34
 */
T_REPLACE_POINTER Replace_setHelpLabel = {(VoidFunc)0x00571020, NULL };
void Cv_setHelpLabel(){
	FFMUL(0x30, Factor);	// x
	FFMUL(0x34, Factor);	// y

	Replace_setHelpLabel.trampolin();
}

/* PythonApi:
 * addGraphData (
 * STRING szName, FLOAT fX, FLOAT fY, INT uiLayer)
 *
 * Call point: 0x0055E920
 * Critical offsets: 0x12, 24
 */
T_REPLACE_POINTER Replace_addGraphData = {(VoidFunc)0x0055E920, NULL };
void Cv_addGraphData(){
	FFMUL(0x12, Factor);	// x
	FFMUL(0x24, Factor);	// y

	Replace_addGraphData.trampolin();
}

/* PythonApi:
 * VOID setTableColumnHeader (
 * STRING szName, INT iColumn, STRING header, INT iWidth)
 *
 * Call point: 0x00571860
 * Critical offsets: 0x24
 */
T_REPLACE_POINTER Replace_setTableColumnHeader = {(VoidFunc)0x00571860, NULL };
void Cv_setTableColumnHeader(){
	IFMUL(0x24, Factor);	// w

	Replace_setTableColumnHeader.trampolin();
}

/* PythonApi:
 * VOID addFlagWidgetGFC (
 * STRING szName, INT iX, INT iY, INT iWidth,
 * INT iHeight, INT iOwner, WidgetType eWidgetType, INT iData1,
 * INT iData2)
 *
 * (Cv-Call, not used)
 * Call point: 0x00567B70
 * Critical offsets: 0x0c, 10, 14
 *
 * Note: The fourth arg (height) is not propagated to Cv-Call.
 *
 * (Cy-Call)
 * Call point: 0x004E96A0
 * Critical offsets: 0x08, 0x0c, 10, 14
 */
T_REPLACE_POINTER Replace_addFlagWidgetGFC = {(VoidFunc)0x004E96A0, NULL };
void Cv_addFlagWidgetGFC(){
	IFMUL(0x08, Factor);	// x
	IFMUL(0x0c, Factor);	// y
	IFMUL(0x10, Factor);	// h
	IFMUL(0x14, Factor);	// w

	Replace_addFlagWidgetGFC.trampolin();
}

/* PythonApi:
 * VOID addReligionMovieWidgetGFC(
 * STRING szName, STRING szFile, INT iX, INT iY,
 * INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1,
 * INT iData2)
 *
 * (Cv-Call, not used)
 * Call point: 0x00567A50
 * Critical offsets: 0x10, 14
 *
 * Note: Only x and y will passed to Cv-Function. This could be enought...
 *
 * (Cy-Call)
 * Call point: 0x004E9670
 * Critical offsets: 0x10, 14, 18, 1C
 *
 */
T_REPLACE_POINTER Replace_addReligionMovieWidgetGFC = {(VoidFunc)0x004E9670, NULL };
void Cv_addReligionMovieWidgetGFC(){
	IFMUL(0x10, Factor);	// x
	IFMUL(0x14, Factor);	// y
	IFMUL(0x18, Factor);	// w
	IFMUL(0x1C, Factor);	// h

	Replace_addReligionMovieWidgetGFC.trampolin();
}

/* PythonApi:
 * VOID initMinimap (
 * INT iLeft, INT iRight, INT iTop, INT iBottom,
 * FLOAT fZ)
 *
 * (Cv-Call, not used)
 * Call point: 0x0055C670
 * Critical offsets: 0x08, 0c, 10,
 *
 * Note: The second argument, right, will stored in ecx, but not on the stack!
 * On the other hand the subroutine uses ecx...
 * Thus it's better to use the CyWrapper to modify the data.
 *
 * (Cy-Call)
 * Call point: 0x004E7A20
 * Critical offsets: 0x04, 08, 0C, 10
 *
 */
T_REPLACE_POINTER Replace_initMinimap = {(VoidFunc)0x004E7A20, NULL };
void Cv_initMinimap(){
	IFMUL(0x04, Factor);	// left
	IFMUL(0x08, Factor);	// right
	IFMUL(0x0c, Factor);	// top
	IFMUL(0x10, Factor);	// bottom

	Replace_initMinimap.trampolin();
}

/* PythonApi:
 * VOID addLeaderheadGFC (
 * STRING szName, INT eWho, INT eInitAttitude, INT iX,
 * INT iY, INT iWidth, INT iHeight, WidgetType eWidget,
 * INT iData1, INT iData2)
 *
 * Call point: 0x0054F180
 * Critical offsets: 0x08 (height), ecx (width)
 *
 * Note: The changed positition is far behind the Cy-Wrapper because sometimes
 * the changed position will be called with values which are pushed directly
 * on the stack/or in register, i.e. '00553EBA mov     ecx, 161h'
 *
 * Todo: Control position (iX, iY)
 */
T_REPLACE_POINTER Replace_addLeaderheadGFC = {(VoidFunc)0x0054F180, NULL };
void Cv_addLeaderheadGFC(){
	IFMUL(0x08, diploMenu.factorHeight);	// height
	IFMUL_PUSH(ecx, diploMenu.factorHeight); //width

	Replace_addLeaderheadGFC.trampolin();
}

#if 0
// ==== Template ====
/* PythonApi:
 *
 *
 * Call point: 0x
 * Critical offsets: 0x
 */
T_REPLACE_POINTER Replace_ = {(VoidFunc)0x, NULL };
void Cv_(){
	IFMUL(0x00, Factor);	//
	FFMUL(0x00, Factor);	//

	Replace_();
}
MH_CreateHook((LPVOID), &Cv_, reinterpret_cast<void**>((LPVOID)&Replace_));
#endif


// =================================================


void hook_drawing_functions(){

  MH_CreateHook(
      (LPVOID)Replace_setText.target,
      &Cv_setText,
      reinterpret_cast<void**>((LPVOID)&Replace_setText.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_setLabel.target,
      &Cv_setLabel,
      reinterpret_cast<void**>((LPVOID)&Replace_setLabel.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_setDimensions.target,
      &Cv_setDimensions,
      reinterpret_cast<void**>((LPVOID)&Replace_setDimensions.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_addTableControlGFC.target,
      &Cv_addTableControlGFC,
      reinterpret_cast<void**>((LPVOID)&Replace_addTableControlGFC.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_addModelGraphicGFC.target,
      &Cv_addModelGraphicGFC,
      reinterpret_cast<void**>((LPVOID)&Replace_addModelGraphicGFC.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_setTextAt.target,
      &Cv_setTextAt,
      reinterpret_cast<void**>((LPVOID)&Replace_setTextAt.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_attachTableControlGFC.target,
      &Cv_attachTableControlGFC,
      reinterpret_cast<void**>((LPVOID)&Replace_attachTableControlGFC.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_moveItem.target,
      &Cv_moveItem,
      reinterpret_cast<void**>((LPVOID)&Replace_moveItem.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_setLabelAt.target,
      &Cv_setLabelAt,
      reinterpret_cast<void**>((LPVOID)&Replace_setLabelAt.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_setHelpLabel.target,
      &Cv_setHelpLabel,
      reinterpret_cast<void**>((LPVOID)&Replace_setHelpLabel.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_addGraphData.target,
      &Cv_addGraphData,
      reinterpret_cast<void**>((LPVOID)&Replace_addGraphData.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_setTableColumnHeader.target,
      &Cv_setTableColumnHeader,
      reinterpret_cast<void**>((LPVOID)&Replace_setTableColumnHeader.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_addFlagWidgetGFC.target,
      &Cv_addFlagWidgetGFC,
      reinterpret_cast<void**>((LPVOID)&Replace_addFlagWidgetGFC.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_addReligionMovieWidgetGFC.target,
      &Cv_addReligionMovieWidgetGFC,
      reinterpret_cast<void**>((LPVOID)&Replace_addReligionMovieWidgetGFC.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_initMinimap.target,
      &Cv_initMinimap,
      reinterpret_cast<void**>((LPVOID)&Replace_initMinimap.trampolin));
  MH_CreateHook(
      (LPVOID)Replace_addLeaderheadGFC.target,
      &Cv_addLeaderheadGFC,
      reinterpret_cast<void**>((LPVOID)&Replace_addLeaderheadGFC.trampolin));
}
