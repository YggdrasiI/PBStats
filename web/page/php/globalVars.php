<?php

$supportedLanguages = array(
	'en', 'de', 'fr',
	/*'en-US', 'fr-FR', 'de-DE', 'de-AT', 'de-CH',*/
);


/* Indicate type of db, 0 - MySQL, 1 - SQLite */
$db_type = (substr($db_dsn,0,6) === "sqlite") ;




/* == Constants (currently not used) == */
define("CM_NO_ACCESS",    0);
define("CM_USER_ACCESS",  1);
define("CM_ADMIN_ACCESS", 2);

define("CM_OPERATION_LIST",   1);
define("CM_OPERATION_ADD",    2);
define("CM_OPERATION_CHANGE", 3);
define("CM_OPERATION_CREATE", 4);
define("CM_OPERATION_DELETE", 5);

define("CM_ACCESS_LIST_OWN",   1);
define("CM_ACCESS_LIST_ALL",   2);
define("CM_ACCESS_ADD_OWN",    3);
define("CM_ACCESS_CHANGE_OWN", 4);
define("CM_ACCESS_CHANGE_ALL", 5);
define("CM_ACCESS_DELETE_OWN", 6);
define("CM_ACCESS_DELETE_ALL", 7);
//define("", );

define("PLAYER_STATUS_ELIMINATED", 0);
define("PLAYER_STATUS_AI", 1);
define("PLAYER_STATUS_OFFLINE", 2);
define("PLAYER_STATUS_ONLINE", 3);
define("PLAYER_STATUS_UNCLAIMED", 4);
define("PLAYER_STATUS_UNKNOWN", 5);


/* == END Constants == */


$status_strings = array(
0 => "Eliminated",
1 => "AI",
2 => "Offline",
3 => "Online",
4 => "Unclaimed",
5 => "?",
);




//Zeichen, mit dem Arrays verbunden/getrennt werden
// Character with seperates array fields in string variables.
$implodeTrenner = "§";


//Bibliothek für die Eingabebearbeitung
// Library for input parsing of pure text, html text, links, etc.
require_once $subdir.'php/htmlpurifier/library/HTMLPurifier.auto.php';
$htmlPurifierConfig = HTMLPurifier_Config::createDefault();
$htmlPurifierConfig->set('Cache.DefinitionImpl', null);//->set('Core.DefinitionCache', null);
$htmlPurifierConfig->set('HTML.Doctype', 'HTML 4.01 Strict');

$htmlPurifierConfigTextareas = HTMLPurifier_Config::createDefault();
$htmlPurifierConfigTextareas->set('Cache.DefinitionImpl', null);
$htmlPurifierConfigTextareas->set('HTML.Doctype', 'HTML 4.01 Strict');
$htmlPurifierConfigTextareas->set('AutoFormat.AutoParagraph', true);



/*
 * Collection of formular classes which connect given sql/sqlite database
 * tables with html forms to fill, edit & delete them.
 * Most initialisation stuff will be done into the constructor of
 * the form classes.
 * The functions are split into two files:
 *   • classIncl: This part is required to create a form. 
 *     (In combination with functions from the second file.)
 *   • phpIncl: Contains the functions to print out the content of some
 *   		sql tables.
 *   The split was done to prevent the unness. loading of the
 *	 whole class at each page.
 *
 * The access array describe which userLevel will be required for some
 * operations on the database. (Sorry, this restriction part is programmed badly
 * and with lack of some useful constant definitions. )
 *
 */
$contentTables = array(
	"News" => array(
		"title" => "{L_NEWS}",
		"className" => "NewsClass",
		"sqlTable" => "news",
		"classIncl" => "contentmanager/News.php",
		"phpIncl" => "contentmanager/News.functions.php",
		"access" => array (
			"viewOwn" => 0,
			"viewAll" => 0,
			"createOwn" => 2,
			"editOwn" => 2,
			"editAll" => 2,
			"delOwn" => 2,
			"delAll" => 2,
		),
	),

	"Downloads" => array(
		"title" =>"{L_DOWNLOADS}",
		"className" => "DownloadClass",
		"sqlTable" => "downloadFiles",
		"classIncl" => "contentmanager/Downloads.php",
		"phpIncl" => "contentmanager/Download.functions.php",
		"access" => array (
			"viewOwn" => 0,
			"viewAll" => 0,
			"createOwn" => 2,
			"editOwn" => 2,
			"editAll" => 2,
			"delOwn" => 2,
			"delAll" => 2,
		),
	),

	"DownloadCategories" => array(
		"title" =>"{L_DOWNLOAD_CATEGORIES}",
		"className" => "DownloadCategorieClass",
		"sqlTable" => "downloadCategories",
		"sqlTable2" => "downloadFiles",
		"classIncl" => "contentmanager/DownloadCategorie.php",
		"phpIncl" => "contentmanager/Download.functions.php",
		"access" => array (
			"viewOwn" => 2,
			"viewAll" => 2,
			"createOwn" => 2,
			"editOwn" => 2,
			"editAll" => 2,
			"delOwn" => 2,
			"delAll" => 2,
		),
	),

	"Games" => array(
		"title" => "{L_GAMES}",
		"className" => "GameClass",
		"sqlTable" => "games",
		"classIncl" => "contentmanager/Game.php",
		"phpIncl" => "contentmanager/Game.functions.php",
		"access" => array (
			"viewOwn" => 0,
			"viewAll" => 0,
			"createOwn" => 1,
			"editOwn" => 1,
			"editAll" => 2,
			"delOwn" => 1,
			"delAll" => 2,
		),
	),

	"Users" => array(
		"title" => "{L_USER}",
		"className" => "UserClass",
		"sqlTable" => "user",
		"classIncl" => "contentmanager/User.php",
		"phpIncl" => "contentmanager/Game.functions.php",
		"access" => array (
			"viewOwn" => 0,
			"viewAll" => 2,
			"createOwn" => 0,
			"editOwn" => 1,
			"editAll" => 2,
			"delOwn" => 2,
			"delAll" => 2,
		),
	),

);



?>
