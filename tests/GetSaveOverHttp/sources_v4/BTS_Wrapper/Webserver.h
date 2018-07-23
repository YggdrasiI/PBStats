#pragma once

#include <string>


#ifdef __cplusplus
extern "C" {
#endif

int startServer(int port);
int stopServer();
void setRootFolder(std::string root);

#ifdef __cplusplus
}
#endif


