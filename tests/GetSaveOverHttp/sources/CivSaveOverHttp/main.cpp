#include <windows.h>
#include <iostream>
#include <string.h>
#include <string>


#include "MinHook.h"
#if defined _M_X64
#pragma comment(lib, "MinHook.x64.lib")
#elif defined _M_IX86
#pragma comment(lib, "MinHook.x86.lib")
#endif

// Includes for url download
#include "curl/curl.h"
#define SKIP_PEER_VERIFICATION

typedef HANDLE (WINAPI  *CREATEFILEA)( LPCTSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE);
typedef DWORD (WINAPI  *GETFILEATTRIBUTESA)( LPCTSTR );

CREATEFILEA fpCreateFileA = NULL;
GETFILEATTRIBUTESA fpGetFileAttributesA = NULL;

#define _T(X) (X)

#define STRLEN(s) (sizeof(s)-sizeof(s[0]))
static const char EXTENSION[] = _T(".CivBeyondSwordSave");
static const int EXTENSION_LEN = STRLEN(EXTENSION); //19; //with leading dot
static const char PITBOSS[] = _T("\\pitboss\\");
static const char TMP_NAME[] = _T("Pitboss.CivBeyondSwordSave");

static std::string str_extension = std::string(".CivBeyondSwordSave");
static std::string str_pitboss = std::string("\\pitboss\\");
static std::string str_url_prefix1 = std::string("_http_");
static std::string str_url_prefix2 = std::string("_https_");
static std::string str_url_prefix3 = std::string("_url_"); //deprecated syntax. Will be handled like https case.
//static std::string str_tmp_save_name = std::string("Pitboss.CivBeyondSwordSave");

#define MAX_TMP_NAME_LEN 256
char filePath[MAX_TMP_NAME_LEN];
static std::string str_last_cached_file = std::string();
bool flush_last_cached_file = false;

// for curl file handling
struct DownloadFile {
	const char *filename;
	FILE *stream;
};

static size_t my_fwrite(void *buffer, size_t size, size_t nmemb, void *stream)
{
	struct DownloadFile *out=(struct DownloadFile *)stream;
	if(out && !out->stream) {
		/* open file for writing */
		if( 0 != fopen_s( &out->stream, out->filename, "wb")){
			out->stream = NULL;
			return -1; /* failure, can't open file to write */
		}
	}
	return fwrite(buffer, size, nmemb, out->stream);
}
// for curl file handling, end


int gen_temp_file_path( char * const path ){

	unsigned int tmp_len = GetTempPathA( MAX_TMP_NAME_LEN, path);
	if( tmp_len+sizeof(TMP_NAME) <= MAX_TMP_NAME_LEN ){
		memcpy( path+tmp_len, TMP_NAME, sizeof(TMP_NAME) );
		return 0;
	}
	return -1;
}

HANDLE WINAPI MyCreateFileA(
		_In_     LPCTSTR               lpFileName,
		_In_     DWORD                 dwDesiredAccess,
		_In_     DWORD                 dwShareMode,
		_In_opt_ LPSECURITY_ATTRIBUTES lpSecurityAttributes,
		_In_     DWORD                 dwCreationDisposition,
		_In_     DWORD                 dwFlagsAndAttributes,
		_In_opt_ HANDLE                hTemplateFile
		){

	if( dwDesiredAccess != GENERIC_READ ){
		return fpCreateFileA( lpFileName,
				dwDesiredAccess,
				dwShareMode,
				lpSecurityAttributes,
				dwCreationDisposition,
				dwFlagsAndAttributes,
				hTemplateFile );
	}


	// Check if filename maps to pitboss savegame.
  // I've check the strings directly with strncmp to made it lightweight.
	int fnLen = strlen(lpFileName);

	if( fnLen > EXTENSION_LEN &&
			strncmp( lpFileName+fnLen-EXTENSION_LEN, EXTENSION, EXTENSION_LEN) == 0 &&
			strstr( lpFileName, PITBOSS) != NULL
    )
  {
    // Check if this file was already cached to omit multiple downloads.
    if( !str_last_cached_file.empty() &&
        0 == strncmp( lpFileName, str_last_cached_file.c_str(), fnLen)
      )
    {
      // This is the last reading call for the save. Remove cached path
      // to force reloading of savegame with the same url (second login).
      if( flush_last_cached_file == true ){
        str_last_cached_file.clear();
        flush_last_cached_file = false;
      }
      if( 0 == gen_temp_file_path( filePath ) ){
        return fpCreateFileA( filePath,
            dwDesiredAccess,
            dwShareMode,
            lpSecurityAttributes,
            dwCreationDisposition,
            dwFlagsAndAttributes,
            hTemplateFile );
      }
    }


    // Try to download it.
    CURL *curl;
    char *curl_filename_encoded = NULL; // convert special chars
    CURLcode res;
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    // Extract url domain from {...}_http[s]_{server}\{...}
    // and store result in str_url, i.e. "http://localhost".
    std::string str_filename = std::string(lpFileName);
    int protocol(-1);
    size_t urlBegin(std::string::npos);
    size_t urlEnd(std::string::npos);
    std::string str_url = std::string();
    if( std::string::npos != (urlBegin = str_filename.find(str_url_prefix1)) ){
      // HTTP transfer
      protocol = 0;
      str_url.append("http://");
      urlBegin += str_url_prefix1.size();
      urlEnd = str_filename.find('\\', urlBegin);
      str_url.append(str_filename, urlBegin, urlEnd-urlBegin);
    }else if( std::string::npos != (urlBegin = str_filename.find(str_url_prefix2)) ){
      // HTTPS transfer
      protocol = 1;
      str_url.append("https://");
      urlBegin += str_url_prefix2.size();
      urlEnd = str_filename.find('\\', urlBegin);
      str_url.append(str_filename, urlBegin, urlEnd-urlBegin);
    }else if( std::string::npos != (urlBegin = str_filename.find(str_url_prefix3)) ){
      // HTTPS transfer
      protocol = 1;
      str_url.append("https://");
      urlBegin += str_url_prefix3.size();
      urlEnd = str_filename.find('\\', urlBegin);
      str_url.append(str_filename, urlBegin, urlEnd-urlBegin);
    }

    if( curl != NULL && protocol > -1 ){
      // Construct download url.
      // Format: "http://{server}/PBx/Saves/pitboss/auto/Recovery_{nick}.CivBeyondSwordSave

      size_t backslash_pos(str_url.size());
      str_url.append("/");
      str_url.append(str_filename, urlEnd+1, str_filename.size()-urlEnd-1);

      //Replace backslashes by slashes
      while( std::string::npos != (backslash_pos = str_url.find('\\', backslash_pos))){
        str_url[backslash_pos] = '/';
      }

      // Use curl function to encode special chars and space in the filename.
      // filename is the substring after the latest slash.
      size_t slash_pos = str_url.rfind('/');
      if( std::string::npos != slash_pos){
        if( curl_filename_encoded != NULL){
          free(curl_filename_encoded); curl_filename_encoded = NULL;
        }
        curl_filename_encoded = curl_easy_escape(curl, str_url.c_str()+slash_pos+1, 0);
        str_url.replace( slash_pos+1,
            str_url.size()-slash_pos-1,
            curl_filename_encoded);
      }

      // Temp. target path for download
      if( 0 == gen_temp_file_path( filePath ) ){

        // Try https and http
        struct DownloadFile downloadFile={ filePath, NULL };
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, my_fwrite);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &downloadFile);
        curl_easy_setopt(curl, CURLOPT_URL, str_url.c_str());

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
        if(downloadFile.stream){
          fclose(downloadFile.stream);
          downloadFile.stream = NULL;
        }

        if(res == CURLE_OK){
          str_last_cached_file = str_filename;
          curl_global_cleanup();

          return fpCreateFileA( filePath,
              dwDesiredAccess,
              dwShareMode,
              lpSecurityAttributes,
              dwCreationDisposition,
              dwFlagsAndAttributes,
              hTemplateFile );

        }
      }
    }
    curl_global_cleanup();
}

	// Normal case
	return fpCreateFileA( lpFileName,
			dwDesiredAccess,
			dwShareMode,
			lpSecurityAttributes,
			dwCreationDisposition,
			dwFlagsAndAttributes,
			hTemplateFile );
}


DWORD WINAPI MyGetFileAttributesA(
		_In_ LPCTSTR lpFileName
		){
	if( !str_last_cached_file.empty() &&
			0 == strncmp( lpFileName, str_last_cached_file.c_str(), strlen(lpFileName) ) ){
		if( 0 == gen_temp_file_path( filePath ) ){
			flush_last_cached_file = true;
			return fpGetFileAttributesA( filePath );
		}
	}
	return fpGetFileAttributesA( lpFileName );
}


extern "C" BOOL APIENTRY DllMain(HINSTANCE hinstDLL, DWORD dwReason, LPVOID lpvReserved)
{
	switch (dwReason)
	{
		case DLL_PROCESS_ATTACH:
			{
				MH_Initialize();
				LPVOID pfn1 = GetProcAddress(GetModuleHandle("KERNEL32.dll"),"CreateFileA");
				LPVOID pfn2 = GetProcAddress(GetModuleHandle("KERNEL32.dll"),"GetFileAttributesA");
				MH_CreateHook(pfn1, &MyCreateFileA, reinterpret_cast<void**>((LPVOID)&fpCreateFileA));
				MH_CreateHook(pfn2, &MyGetFileAttributesA, reinterpret_cast<void**>((LPVOID)&fpGetFileAttributesA));
				MH_EnableHook(MH_ALL_HOOKS);
			}
			break;
		case DLL_PROCESS_DETACH:
			MH_DisableHook(MH_ALL_HOOKS);
			MH_Uninitialize();
			break;
		case DLL_THREAD_ATTACH:
			break;
		case DLL_THREAD_DETACH:
			break;
	}
	return true;
}
