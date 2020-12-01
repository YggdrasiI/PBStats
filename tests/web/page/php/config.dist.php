<?php

// Default values for two users.
// This users will be includded into
// the user table at every (re)creation.
$defaultAdmin = "Admin";
$defaultUser = "User";
$defaultAdminPassword = "superverysecret";
$defaultUserPassword = "alittlebitsecret";
$defaultAdminMail = "admin@example.com";
$defaultUserMail = "user@example.com";
$adminLevel = 255;
$userLevel = 1;

// sqlite:
// $db_username = false;
// $db_password = false;
// $db_dsn = "sqlite:/path/to/web/store/pbstats.sqlite";
// MySQL:
$db_username = '';
$db_password = '';
$db_dsn = 'mysql:host=localhost;dbname=XXX';


// Directory for download files
// Need absolute path
$download_folder = "/var/www/civ/files/";

// Relative(!) root dir for above download folder
$fileRoot = "../files/";

// Directiory for tempoary files during a upload process
// (The user sends files at the first stage and has to confirm
// in an second stage. )
$tmpdir = $fileRoot."tmp/";

/* Maximal file size for uploads.
 * Note that the value webserver/php constants restirct 
 * the file size, too.
 */
$maxFileSize = 10000000;//~10MB 
$maxFileSize = min( $maxFileSize, ini_get('upload_max_filesize') );



/* Subdirectory pattern for a folder with write access for
 * the webserver.
 * The paths will be connected to 
 * $fileRoot/[public|private]/$subdirWithWriteAccess 
 *
 * The split into public/private allows you to protect some files (private)
 * with a .htaccess file. As default there is NO difference between public
 * and private files.
 */
$subdirWithWriteAccess = "uploads/";
