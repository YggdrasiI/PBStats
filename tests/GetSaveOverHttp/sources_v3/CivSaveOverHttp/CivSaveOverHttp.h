#define NEU
#ifdef NEU
// Folgender ifdef-Block ist die Standardmethode zum Erstellen von Makros, die das Exportieren 
// aus einer DLL vereinfachen. Alle Dateien in dieser DLL werden mit dem GETSAVEOVERHTTP_EXPORTS-Symbol
// (in der Befehlszeile definiert) kompiliert. Dieses Symbol darf für kein Projekt definiert werden,
// das diese DLL verwendet. Alle anderen Projekte, deren Quelldateien diese Datei beinhalten, erkennen 
// GETSAVEOVERHTTP_API-Funktionen als aus einer DLL importiert, während die DLL
// mit diesem Makro definierte Symbole als exportiert ansieht.
#ifdef GETSAVEOVERHTTP_EXPORTS
#define GETSAVEOVERHTTP_API __declspec(dllexport)
#else
#define GETSAVEOVERHTTP_API __declspec(dllimport)
#endif

//#include <windows.h>

#else

#ifndef __MAIN_H__
#define __MAIN_H__

#include <windows.h>

/*  To use this exported function of dll, include this header
 *  in your project.
 */

#ifdef BUILD_DLL
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT __declspec(dllimport)
#endif


#ifdef __cplusplus
extern "C"
{
#endif

void DLL_EXPORT SomeFunction(const LPCSTR sometext);

#ifdef __cplusplus
}
#endif

#endif // __MAIN_H__

#endif
