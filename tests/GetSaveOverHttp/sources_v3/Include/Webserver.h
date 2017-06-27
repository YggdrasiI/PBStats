// Folgender ifdef-Block ist die Standardmethode zum Erstellen von Makros, die das Exportieren 
// aus einer DLL vereinfachen. Alle Dateien in dieser DLL werden mit dem WEBSERVER_EXPORTS-Symbol
// (in der Befehlszeile definiert) kompiliert. Dieses Symbol darf für kein Projekt definiert werden,
// das diese DLL verwendet. Alle anderen Projekte, deren Quelldateien diese Datei beinhalten, erkennen 
// WEBSERVER_API-Funktionen als aus einer DLL importiert, während die DLL
// mit diesem Makro definierte Symbole als exportiert ansieht.
#ifdef WEBSERVER_EXPORTS
#define WEBSERVER_API __declspec(dllexport)
#else
#define WEBSERVER_API __declspec(dllimport)
#endif

#include <string>
WEBSERVER_API int startServer(int port);
WEBSERVER_API int stopServer();
WEBSERVER_API void setRootFolder(std::string root);
