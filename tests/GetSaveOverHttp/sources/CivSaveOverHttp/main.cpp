#include <windows.h>
#include <iostream>


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
static const char URL[] = _T("_url_");
static const char HTTPS[] = _T("https://");
static const char HTTP[] = _T(" http");
static const char TMP_NAME[] = _T("Pitboss.CivBeyondSwordSave");

#define MAX_TMP_NAME_LEN 256
char filePath[MAX_TMP_NAME_LEN];
char* last_cached_file = NULL;
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


	// Check if filename maps to pitboss savegame
	// Try to download it.
	int fnLen = strlen(lpFileName);

	if( fnLen > EXTENSION_LEN &&
			strncmp( lpFileName+fnLen-EXTENSION_LEN, EXTENSION, EXTENSION_LEN) == 0 &&
			strstr( lpFileName, PITBOSS) != NULL
		){

		// Check if this file was already cached
		if( last_cached_file != NULL && 0 == strncmp( lpFileName, last_cached_file, fnLen) ){

			// This is the last reading call for the save. Remove cached path
			// to force reloading of savegame with the same url (second login).
			if( flush_last_cached_file == true ){
				free(last_cached_file); last_cached_file = NULL;
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


		CURL *curl;
		char *filename_encoded = NULL; // convert special chars
		CURLcode res;
		curl_global_init(CURL_GLOBAL_DEFAULT);
		curl = curl_easy_init();

		// Extract url from filepath
		const char* _url_substr = strstr( lpFileName, URL);
		if( _url_substr != NULL && curl != NULL ){
			const char* urlBegin = _url_substr + 5;
			const char * urlEnd = strchr( urlBegin, '\\');
			if( urlEnd != NULL ){

				// Construct download url
				//const char url[] = _T("http://{server}/PBx/Saves/pitboss/auto/Recovery_{nick}.CivBeyondSwordSave");
				const unsigned int server_len = (urlEnd-urlBegin);
				const unsigned int filename_len = ( fnLen - ( urlEnd - lpFileName ) - 1 );

				const unsigned int url_len = STRLEN( HTTPS ) // ' http://' or 'https://'
					+ server_len + 1 // '{server}', '/'
					+ filename_len + 1; // 'PBx/Saves/pitboss/[auto/]filename', '\0'

				char* url = (char*) malloc( url_len * sizeof(char) );
				memcpy( url, HTTPS, STRLEN(HTTPS) );
				memcpy( url+STRLEN(HTTPS), urlBegin, server_len );
				url[STRLEN(HTTPS)+server_len] = '/';
				memcpy( url+STRLEN(HTTPS)+server_len+1, urlEnd+1, filename_len );
				url[url_len-1] = '\0'; // redundant but save

				//Replace backslashes by slashes
				char* backslash = (char*) strchr( url+STRLEN(HTTPS)+server_len+2, '\\');
				while( NULL != backslash ){
					*backslash = '/';
					backslash = (char*) strchr( backslash+1, '\\');
				}

				// encode special chars and space after last slash
				char* slash = (char*) strrchr( url+STRLEN(HTTPS)+server_len+2, '/');
				if( NULL != slash ){
					filename_encoded = curl_easy_escape(curl, slash+1, 0);
				}else{
					slash = url + strlen(url) - 1;
				}

				const unsigned int filename_encoded_len = strlen(filename_encoded);
				const unsigned int url_path_len = (slash-url) + 1;

				// Well, not the whole url is encoded, but the filename...
				// +1 for \0
				char* url_encoded = (char*) malloc( (url_path_len+filename_encoded_len+1) * sizeof(char) );
				memcpy( url_encoded, url, url_path_len);
				memcpy( url_encoded+url_path_len, filename_encoded, filename_encoded_len);
				*(url_encoded+url_path_len+filename_encoded_len) = '\0';
				curl_free(filename_encoded);

				// Target path for download
				if( 0 == gen_temp_file_path( filePath ) ){

					// Try https and http
					struct DownloadFile downloadFile={ filePath, NULL };
					curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, my_fwrite);
					curl_easy_setopt(curl, CURLOPT_WRITEDATA, &downloadFile);
					curl_easy_setopt(curl, CURLOPT_URL, url_encoded);

#ifdef SKIP_PEER_VERIFICATION
					curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
#endif
#ifdef SKIP_HOSTNAME_VERIFICATION
					curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
#endif

					/* Perform the request, res will get the return code */
					res = curl_easy_perform(curl);

					/* Check for errors */
					if(res != CURLE_OK){
						// https failed
						fprintf(stderr, "curl_easy_perform() failed: %s\n",
								curl_easy_strerror(res));

						/* always cleanup */
						curl_easy_cleanup(curl);
						if(downloadFile.stream){
							fclose(downloadFile.stream);
							downloadFile.stream = NULL;
						}

						// Try http:// instead of https://
						memcpy( url_encoded, HTTP, STRLEN(HTTP) );

						curl_easy_setopt(curl, CURLOPT_URL, url_encoded+1);
						res = curl_easy_perform(curl);
					}

					/* always cleanup */
					curl_easy_cleanup(curl);
					if(downloadFile.stream){
						fclose(downloadFile.stream);
						downloadFile.stream = NULL;
					}

					if(res == CURLE_OK){

						free(last_cached_file);
						last_cached_file = (char*) malloc( fnLen * sizeof(char) );
						memcpy( last_cached_file, lpFileName, fnLen * sizeof(char) );

						free(url_encoded); url_encoded = NULL;
						free( url ); url = NULL;
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
				free(url_encoded); url_encoded = NULL;
				free( url ); url = NULL;
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
	if( last_cached_file != NULL &&
			0 == strncmp( lpFileName, last_cached_file, strlen(lpFileName) ) ){
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
