#pragma once

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

#ifdef __cplusplus
extern "C" {
#endif
GETSAVEOVERHTTP_API void StartServer(const char *pPortName);

#ifdef __cplusplus
}
#endif
