// Webserver.cpp : Definiert die exportierten Funktionen für die DLL-Anwendung.

#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <vector>

#include "windows.h"
#include <dirent.h>
#include <microhttpd.h>
#if defined _M_X64
//#pragma comment(lib, "MinHook.x64.lib")
#pragma comment(lib, "libmicrohttpd.lib")
#elif defined _M_IX86
//#pragma comment(lib, "MinHook.x86.lib")
#pragma comment(lib, "libmicrohttpd.lib")
#endif

//#define DEBUG // undef for Nodebug
#include "Webserver.h"

//#include <unistd.h>
#ifndef snprintf
#define snprintf(buf,len, format,...) _snprintf_s(buf, len,len, format, __VA_ARGS__)
#endif

#define PAGE "<html><head><title>File not found</title></head><body>File not found</body></html>"

static std::string Root_folder = "./";
static std::vector<std::string> Allowed_subfolders;
static std::vector<std::string> Allowed_extensions;
static struct MHD_Daemon *d = NULL;

typedef struct { DIR *dir; const std::string *p_path; } foo_t;

static ssize_t
file_reader(void *cls, uint64_t pos, char *buf, size_t max)
{
	FILE *file = (FILE *)cls;

	(void)fseek(file, (long)pos, SEEK_SET);
	return fread(buf, 1, max, file);
}


static void
file_free_callback(void *cls)
{
	FILE *file = (FILE *)cls;
	fclose(file);
}


static void
dir_free_callback(void *cls)
{
	//DIR *dir = (DIR *)cls;
	foo_t *p_foo = (foo_t *)cls;
	if (p_foo->dir != NULL)
		closedir(p_foo->dir);
}


static ssize_t
dir_reader(void *cls, uint64_t pos, char *buf, size_t max)
{
	foo_t *p_foo = (foo_t *)cls;
	//DIR *dir = (DIR *)cls;
	struct dirent *e;

	if (max < 512)
		return 0;
	do
	{
		e = readdir(p_foo->dir);
		if (e == NULL)
			return MHD_CONTENT_READER_END_OF_STREAM;
	} while (e->d_name[0] == '.');
	return snprintf(buf, max,
		//			"<a href=\"%s\">%s</a><br>",
		"<a href=\"/%s/%s\">%s</a><br>",
		(p_foo->p_path ? p_foo->p_path->c_str() : ""),
		e->d_name,
		e->d_name);
}


static int
ahc_echo(void *cls,
	struct MHD_Connection *connection,
	const char *url,
	const char *method,
	const char *version,
	const char *upload_data,
	size_t *upload_data_size, void **ptr)
{
	static int aptr;
	struct MHD_Response *response;
	int ret(MHD_NO);
	//DIR *dir(NULL);
	static foo_t foo = { NULL, NULL };
	struct stat buf;
	char emsg[1024];
	FILE *file(NULL);
	int fd(-1);

	if (0 != strcmp(method, MHD_HTTP_METHOD_GET))
		return MHD_NO;              /* unexpected method */

	if (&aptr != *ptr)
	{
		/* do never respond on first call */
		*ptr = &aptr;
		return MHD_YES;
	}
	*ptr = NULL;                  /* reset when done */

								  // Requisted url
	fprintf(stdout, "File: %s\n", url);

	// Check if save filename
	bool file_extension_allowed(false);

	//for( auto extension: Allowed_extensions){
	for (std::vector<std::string>::const_iterator i = Allowed_extensions.begin();
		i != Allowed_extensions.end(); ++i) {

		const char *pos_extension = strstr(url, (*i).c_str()); // case not ignored...
		if (pos_extension != NULL &&
			strlen(url) == (*i).length() + (pos_extension - url)) {
			// url ends with this extension.
			file_extension_allowed = true;
			break;
		}
	}

	if (file_extension_allowed) {

		//file = fopen (&url[1], "rb");

		std::string path(Root_folder);
		path.append(&url[1]);
		file = fopen(path.c_str(), "rb");

		if (NULL != file)
		{
			fd = fileno(file);
			if (-1 == fd)
			{
				(void)fclose(file);
				return MHD_NO; /* internal error */
			}
			if ((0 != fstat(fd, &buf)) ||
				(!S_ISREG(buf.st_mode)))
			{
				/* not a regular file, refuse to serve */
				fclose(file);
				file = NULL;
			}
		}
	}

	if (NULL == file)
	{
		// Check if folder url matches allowed pattern...
		foo.dir = NULL; foo.p_path = NULL;
		std::string str_url(&url[1]);
		if (str_url.back() == '/') { str_url.pop_back(); }
		for (std::vector<std::string>::const_iterator i = Allowed_subfolders.begin();
			i != Allowed_subfolders.end(); ++i) {

			fprintf(stdout, "Compare '%s' '%s'...\n", (*i).c_str(), str_url.c_str());
			if ((*i).compare(str_url) == 0) {
				std::string path(Root_folder);
				path.append(*i);
				fprintf(stdout, "Opening '%s'...\n", path.c_str());
				foo.dir = opendir(path.c_str());
				foo.p_path = std::addressof(*i);
				break;
			}
		}
#ifdef DEBUG
		if (NULL == foo.dir)
#else
		if( 1 )
#endif
		{
			/* most likely cause: more concurrent requests than
			available file descriptors / 2 */
#ifdef DEBUG
			snprintf(emsg,
				sizeof(emsg),
				"Failed to open directory `%s' (%s): %s\n",
				&url[1],
				Root_folder.c_str(),
				strerror(errno));
#else
			snprintf(emsg,
				sizeof(emsg),
				"Failed to open directory `%s': %s\n",
				&url[1],
				strerror(errno));
#endif
			response = MHD_create_response_from_buffer(strlen(emsg),
				emsg,
				MHD_RESPMEM_MUST_COPY);
			if (NULL == response)
				return MHD_NO;
			ret = MHD_queue_response(connection,
				MHD_HTTP_SERVICE_UNAVAILABLE,
				response);
			MHD_destroy_response(response);
		}
		else
		{
			response = MHD_create_response_from_callback(MHD_SIZE_UNKNOWN,
				32 * 1024,
				&dir_reader,
				&foo,
				&dir_free_callback);
			if (NULL == response)
			{
				closedir(foo.dir);
				return MHD_NO;
			}
			ret = MHD_queue_response(connection, MHD_HTTP_OK, response);
			MHD_destroy_response(response);
		}
	}
	else
	{
		// Serve file...
		response = MHD_create_response_from_callback(buf.st_size, 32 * 1024,     /* 32k page size */
			&file_reader,
			file,
			&file_free_callback);
		if (NULL == response)
		{
			fclose(file);
			return MHD_NO;
		}
		ret = MHD_queue_response(connection, MHD_HTTP_OK, response);
		MHD_destroy_response(response);
	}
	return ret;
}


int startServer(int port=8080)
{
	if (NULL != d) {
		// Server is already running...
		return 2;
	}

	Allowed_subfolders = std::vector<std::string>();
	Allowed_subfolders.push_back("multi");
	Allowed_subfolders.push_back("multi/auto");
	Allowed_subfolders.push_back("pitboss");
	Allowed_subfolders.push_back("pitboss/auto");

	Allowed_extensions = std::vector<std::string>();
	Allowed_extensions.push_back(".CivSavedSave");
	Allowed_extensions.push_back(".CivWarlordsSave");
	Allowed_extensions.push_back(".CivBeyondSwordSave");

	d = MHD_start_daemon(
			MHD_USE_THREAD_PER_CONNECTION |
#ifdef DEBUG
			MHD_USE_DEBUG |
#endif
//			MHD_USE_DUAL_STACK |
//			MHD_USE_POLL_INTERNALLY |
			MHD_USE_PIPE_FOR_SHUTDOWN, 
			port, NULL, NULL, &ahc_echo, PAGE, MHD_OPTION_END);


	if (NULL == d) {
		// Can not start server...
		return 1;
	}

	// Wait on keystroke
	//(void) getc (stdin);
	//MHD_stop_daemon (d);

	return 0;
}

int stopServer() {
	if (d != NULL) {
		MHD_stop_daemon(d);
	}
	return 0;
}

void setRootFolder(std::string root) {
	//Update static variable...
	Root_folder = root;
}

