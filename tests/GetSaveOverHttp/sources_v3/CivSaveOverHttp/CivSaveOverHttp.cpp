/*
 * Notes:
 *  - Compile it without optimazions...
 *
 */

#include "stdafx.h"
#include "CivSaveOverHttp.h"

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <iostream>
#include <string>
#include <sstream>

#include <winsock2.h>
#include <Ws2tcpip.h>
#include <windows.h>
#pragma comment(lib, "Ws2_32.lib")

#include "../Include/minhook/MinHook.h"
#if defined _M_X64
#pragma comment(lib, "MinHook.x64.lib")
#elif defined _M_IX86
#pragma comment(lib, "MinHook.x86.lib")
#endif

// To share saves in DirectIP mode
#define WITH_WEBSERVER
#ifdef WITH_WEBSERVER
#include "../Webserver/Webserver.h"
#pragma comment(lib, "Webserver.lib")
#endif

// Includes for curl download
#include "../include/curl/curl.h"
#pragma comment(lib, "libcurl.lib")
#define SKIP_PEER_VERIFICATION
int curl_download(const std::string &url, const std::string &path);

typedef int(WINAPI *SENDTO)(
    SOCKET                s,
    const char                  *buf,
    int                   len,
    int                   flags,
    const struct sockaddr *to,
    int                   tolen
    );
typedef int(WINAPI *RECVFROM)(
    SOCKET          s,
    char            *buf,
    int             len,
    int             flags,
    struct sockaddr *from,
    int             *fromlen
    );

SENDTO fpSendto = NULL;
RECVFROM fpRecvFrom = NULL;
int Webserver_Port = 8080;

static const std::string Tmp_Name = std::string("Pitboss.CivBeyondSwordSave");
static std::string Str_Extension = std::string(".CivBeyondSwordSave");
static std::string Str_Pitboss = std::string("\\pitboss\\");
static std::string Str_url_prefix1 = std::string("_http_");
static std::string Str_url_prefix2 = std::string("_https_");
static std::string Str_url_prefix3 = std::string("_url_"); //deprecated syntax. Will be handled like https case.

#define MAX_TMP_NAME_LEN 512
static std::string tmp_path = std::string(MAX_TMP_NAME_LEN, ' ');
static std::string last_cached_orig_path = std::string();

// for curl file handling
struct DownloadFile {
  const char *filename;
  FILE *stream;
};

static size_t my_fwrite(void *buffer, size_t size, size_t nmemb, void *stream)
{
  struct DownloadFile *out = (struct DownloadFile *)stream;
  if (out && !out->stream) {
    /* open file for writing */
    if (0 != fopen_s(&out->stream, out->filename, "wb")) {
      out->stream = NULL;
      return -1; /* failure, can't open file to write */
    }
  }
  return fwrite(buffer, size, nmemb, out->stream);
}

int gen_temp_file_path(std::string &path) {

  char tmp_path[MAX_TMP_NAME_LEN]; //ugly
  unsigned int tmp_len = GetTempPathA(MAX_TMP_NAME_LEN, tmp_path);
  if (tmp_len + Tmp_Name.length() > MAX_TMP_NAME_LEN) {
    path.clear();
    return -1;
  }
  path.clear();
  path.append(tmp_path); // with '/' ?!
  path.append(Tmp_Name);
  return 0;
}

int curl_download(std::string &url, std::string &path) {

  CURL *curl;
  CURLcode res = CURLE_FAILED_INIT;
  curl_global_init(CURL_GLOBAL_DEFAULT);
  curl = curl_easy_init();

  if (curl != NULL) {

    // Use curl function to encode special chars and space,
    // but restrict on the filename (everything after lastest slash).
    size_t slash_pos = url.rfind('/');
    if (std::string::npos != slash_pos && url.length() > slash_pos + 1) {
      char *curl_filename_encoded = curl_easy_escape(curl, url.c_str() + slash_pos + 1, 0);
      url.replace(slash_pos + 1, url.size() - slash_pos - 1, curl_filename_encoded);
    }
    // Set target file
    struct DownloadFile downloadFile = { path.c_str(), NULL };
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, my_fwrite);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &downloadFile);
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

#ifdef SKIP_PEER_VERIFICATION
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
#endif
#ifdef SKIP_HOSTNAME_VERIFICATION
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
#endif

    /* Perform the request, res will get the return code */
    res = curl_easy_perform(curl);

    /* always cleanup */
    curl_easy_cleanup(curl);
    if (downloadFile.stream) {
      fclose(downloadFile.stream);
      downloadFile.stream = NULL;
    }

    if (res == CURLE_OK) {
      curl_global_cleanup();
      return 0;
    }
  }

  curl_global_cleanup();
  return -1;
}
// for curl file handling, end

std::string get_server_ip(struct sockaddr *from) {
  std::string server_ip("");
  char *s = NULL;

  //#define inet_ntop  InetNtopA
  switch (from->sa_family) {
#ifndef WIN_XP
    case AF_INET6: {
                     struct sockaddr_in6 *addr_in6 = (struct sockaddr_in6 *)from;
                     s = (char *)malloc(INET6_ADDRSTRLEN);
                     inet_ntop(AF_INET6, &(addr_in6->sin6_addr), s, INET6_ADDRSTRLEN);
                     server_ip.append(s);
                     break;
                   }
#endif
    case AF_INET:
                   {
                     struct sockaddr_in *addr_in = (struct sockaddr_in *)from;
#ifdef WIN_XP
                     s = inet_ntoa(addr_in->sin_addr);
                     server_ip.append(s);
#else
                     s = (char *)malloc(INET_ADDRSTRLEN);
                     inet_ntop(AF_INET, &(addr_in->sin_addr), s, INET_ADDRSTRLEN);
                     server_ip.append(s);
#endif
                     break;
                   }
    default:
                   break;
  }
  free(s);
  return server_ip;
}

int WINAPI MySendto(
    _In_       SOCKET                s,
    _In_ const char                  *buf,
    _In_       int                   len,
    _In_       int                   flags,
    _In_       const struct sockaddr *to,
    _In_       int                   tolen)
{
  int assumed_return_value = len;
  //return fpSendto(s, buf, len, flags, to, tolen);

  // FE FE 00 00 |** ** 05 08| 00 00 [...]
  if (len > 0x20) {
    unsigned int id = *((unsigned int*)(buf + 4)) >> 16; // Flips byte order...
    if (id == 0x0805 /* DirectIP game */ ||
        id == 0x0806 /* DirectIP game (2, gesehen bei Test mit multiple-Argument) */ ||
        id == 0x0807 /* Pitboss game */) {

      const unsigned int offset = 0x21; // Start of string.
      const unsigned int path_len = *((unsigned int *)(buf + offset - 4)); // Length info of string
      //const unsigned int crc32 = *((unsigned int *)(buf + offset - 8)); // crc32 value of file

      const char *begin = buf + offset;
      std::string path(begin, path_len);
      //std::string extension(".CivBeyondSwordSave");

      // Locate '\\Saves' substring
      std::string saves_substring("\\Saves");
      size_t pos_saves = path.find(saves_substring);
      if( pos_saves != std::string::npos ){
        std::string save_folder(path, 0, pos_saves+saves_substring.length());
        save_folder.append("\\");
        setRootFolder(save_folder);

        // Path in relation to web root
        std::stringstream url_stream;
        url_stream << "_http_:";
        url_stream <<  Webserver_Port;
        url_stream << path.substr(pos_saves+saves_substring.length());
        std::string url = url_stream.str();

        /* Replace the file name in the buffer. */
        uint32_t l_old = path.length();
        uint32_t l_new = url.length();
        int l_diff = ((int) l_new - (int)l_old);
        char *buf2 = (char *)malloc(len + l_diff + 1);

        // Head
        memcpy(buf2, buf, offset - 4);

        // Changed body
        memcpy(buf2 + offset - 4, &l_new, 4);
        memcpy(buf2 + offset, url.c_str(), l_new);
#if 0
        // Tail (empty)
        memcpy(buf2 + offset + l_new,
            buf + offset + l_old,
            recv_from_length - offset - l_old);
#endif
        // Copy back
        len += l_diff;
        //memset((char *)buf, 0, len+100);
        memcpy((char *)buf, buf2, len);
        free(buf2);
      }
    }
  }

  int ret = fpSendto(s, buf, len, flags, to, tolen);
  if( ret == len ){
    return assumed_return_value;
  }else{
    return ret;
  }
}

int WINAPI MyRecvfrom(
    _In_        SOCKET          s,
    _Out_       char            *buf,
    _In_        int             len,
    _In_        int             flags,
    _Out_       struct sockaddr *from,
    _Inout_opt_ int             *fromlen)
{
  // recv_from_length = Number of fetched bytes...
  int recv_from_length = fpRecvFrom(s, buf, len, flags, from, fromlen);
  //return recv_from_length;

  // Analyse packet...
  // FE FE 00 00 ** ** 05 08 00 00 [...]
  if (recv_from_length > 0x20) {
    unsigned int id = *((unsigned int*)(buf + 4)) >> 16; // Flips byte order...
    if (id == 0x0805 /* DirectIP game */ ||
        id == 0x0806 /* DirectIP game (2, gesehen bei Test mit multiple-Argument) */ ||
        id == 0x0807 /* Pitboss game */) {

      // Extract file path from packet. Note that the path is not null terminated.
      const unsigned int offset = 0x21; // Start of string.
      const unsigned int path_len = *((unsigned int *)(buf + offset - 4)); // Length info of string
      const   unsigned int crc32 = *((unsigned int *)(buf + offset - 8)); // crc32 value of file

      if ((int)(path_len + offset) > recv_from_length) {// Buffer overflow check
        goto skip;
      }
      const char *begin = buf + offset;
      std::string path(begin, path_len);
      std::string extension(".CivBeyondSwordSave");

      // Check if filename maps to pitboss savegame.
      if (path.length() < extension.length()) {
        goto skip;
      }
      std::string path_ext = path.substr(path.length() - extension.length(), extension.length());
      if (0 != extension.compare(path_ext)) {
        goto skip;
      }

      // Check if this file was already cached to omit multiple downloads.
      if (!last_cached_orig_path.empty() &&
          0 == last_cached_orig_path.compare(path))
      {
        // TODO: compare crc32 value of file to uncover old files.
      }
      else {
        last_cached_orig_path = path;
        // Ask system to gen tmp. file name.
        if (gen_temp_file_path(tmp_path)) {
          goto skip;
        }
      }


      /* Replace the file name in the buffer. */
      uint32_t l_old = path.length();
      uint32_t l_new = tmp_path.length();
      int l_diff = ((int) l_new - (int)l_old);
      char *buf2 = (char *)malloc(recv_from_length + l_diff + 1);

      // Head
      memcpy(buf2, buf, offset - 4);

      // Changed body
      memcpy(buf2 + offset - 4, &l_new, 4);
      memcpy(buf2 + offset, tmp_path.c_str(), l_new);

#if 0
      // Tail (empty)
      memcpy(buf2 + offset + l_new,
          buf + offset + l_old,
          recv_from_length - offset - l_old);
#endif

      /* Try to download into tmp_path.
       *
       */
      /* First, construct url
       * Variant 1 (Pitboss server) path is [...]_http[s]_{server}[:{port}]\[...]
       *         Example:
       *        http://{server}/PB1/Saves/pitboss/auto/Recovery_{nick}.CivBeyondSwordSave
       *
       * Variant 2 (Direct IP) path is [...]_http[s]_:{port}\[...]
       *         Example:
       *        http://{ip}:{port}/Saves/multi/VOTE_[...].CivBeyondSwordSave
       *
       * In case 2 (empty server string) the ip of recv should be used as server ip.
       */
      std::string str_filename = std::string(path);
      int protocol(-1);
      size_t hostnameBegin(std::string::npos);
      size_t hostnameEnd(std::string::npos);

      std::string url = std::string();
      if (std::string::npos != (hostnameBegin = str_filename.find(Str_url_prefix1))) {
        // HTTP transfer
        protocol = 0;
        url.append("http://");
        hostnameBegin += Str_url_prefix1.size();
      }
      else if (std::string::npos != (hostnameBegin = str_filename.find(Str_url_prefix2))) {
        // HTTPS transfer
        protocol = 1;
        url.append("https://");
        hostnameBegin += Str_url_prefix2.size();
      }
      else if (std::string::npos != (hostnameBegin = str_filename.find(Str_url_prefix3))) {
        // HTTPS transfer
        protocol = 1;
        url.append("https://");
        hostnameBegin += Str_url_prefix3.size();
      }

      if (std::string::npos != hostnameBegin && str_filename[hostnameBegin + 0] == ':') {
        // Construct ip of server
        std::string server_ip = get_server_ip(from);
        url.append(server_ip);
      }

      hostnameEnd = str_filename.find('\\', hostnameBegin); // The backslash after {server}.
      if( std::string::npos == hostnameEnd ){
        protocol = -1;
      }else{
        url.append(str_filename, hostnameBegin, hostnameEnd - hostnameBegin);

        // Add '/' and uri part after port.
        size_t backslash_pos(url.size());
        url.append("/");
        url.append(str_filename, hostnameEnd + 1, str_filename.size() - hostnameEnd - 1);

        //Replace backslashes by slashes
        while (std::string::npos != (backslash_pos = url.find('\\', backslash_pos))) {
          url[backslash_pos] = '/';
        }
      }

      if (protocol > -1 &&
          0 == curl_download(url, tmp_path))
      {
        last_cached_orig_path = str_filename;

        // Replace buffer with copy
        recv_from_length += l_diff;
        memcpy(buf, buf2, recv_from_length);

      }else{
        // Input wrong or download failed. The filename should still be upadated to local path...
        recv_from_length += l_diff;
        memcpy(buf, buf2, recv_from_length);
      }

      free(buf2);
    }
  }
skip:
  return recv_from_length;
}

extern "C" BOOL APIENTRY DllMain(HINSTANCE hinstDLL, DWORD dwReason, LPVOID lpvReserved)
{
  switch (dwReason)
  {
    case DLL_PROCESS_ATTACH:
      {
#ifdef WITH_WEBSERVER
        // Read port from environment...
        char* libvar;
        size_t requiredSize;
        getenv_s( &requiredSize, NULL, 0, "PORT");
        libvar = (char*) malloc(requiredSize * sizeof(char));
        if (libvar)
        {
          getenv_s( &requiredSize, libvar, requiredSize, "PORT" );
        }
        if( libvar != NULL ){
          Webserver_Port = atoi(libvar);
        }

        startServer(Webserver_Port);
#endif

        MH_Initialize();
        LPVOID pfn3 = GetProcAddress(GetModuleHandleA("WS2_32.dll"), "sendto");
        LPVOID pfn4 = GetProcAddress(GetModuleHandleA("WS2_32.dll"), "recvfrom");
        MH_CreateHook(pfn3, &MySendto, reinterpret_cast<void**>((LPVOID)&fpSendto));
        MH_CreateHook(pfn4, &MyRecvfrom, reinterpret_cast<void**>((LPVOID)&fpRecvFrom));
        MH_EnableHook(MH_ALL_HOOKS);

      }
      break;
    case DLL_PROCESS_DETACH:
      {
#ifdef WITH_WEBSERVER
        stopServer();
#endif

        MH_DisableHook(MH_ALL_HOOKS);
        MH_Uninitialize();

      }
      break;
    case DLL_THREAD_ATTACH:
      break;
    case DLL_THREAD_DETACH:
      break;
  }
  return true;

}


/*
 * Examples of traffic packages:
 *
 * (Pitboss game)
 * crc32: ecaf54ee
 0000  fe fe 00 00|85 00 07 08|00 00 00 01 ff ff ff ff  ................
 0010  fe 54 15 01 37 00 00 00 00|ee 54 af ec|62 00 00  .T..7.....T..b..
 0020  00 5a 3a 5c 68 6f 6d 65 5c 70 62 5c 5f 75 72 6c  .Z:\home\pb\_url
 [...]
 0070  2e 43 69 76 42 65 79 6f 6e 64 53 77 6f 72 64 53  .CivBeyondSwordS
 0080  61 76 65                                         ave

 * (Direct IP game)
 0000  fe fe 00 00|3f 00 05 08|00 00 00 01 00 00 00 00  ....?...........
 0010  01 00 00 00 7c 00 00 00 00 5a 2c 23 07 5d 00 00  ....|....Z,#.]..
 0020  00 43 3a 5c 55 73 65 72 73 5c 85 65 85 65 5c 44  .C:\Users\XxXx\D
 [...]
 0060  49 50 5f 50 42 4d 6f 64 5f 76 58 2e 43 69 76 42  IP_PBMod_vX.CivB
 0070  65 79 6f 6e 64 53 77 6f 72 64 53 61 76 65        eyondSwordSave
 */


