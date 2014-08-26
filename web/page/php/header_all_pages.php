<?php 
/*
 * • Default initialisation/setup for every page.
 * • Produce no outbut, but contains some header-location switches.
 * • Should be included on every page, but in most case indirect 
 * 		over header.php. Only call it directly if header.php 
 * 		will be not included.
 */

include_once($subdir.'php/config.php');
include_once($subdir.'php/globalVars.php');
include_once($subdir.'php/helper.php');
include_once($subdir.'php/pbModFunctions.php');

// Als erstes die Session starten. Falls die (Start)Seite mit F5 geladen wurde, aber eigentlich ein anderer Inhalt angezeigt werden sollte,
//wird dies über die Session-Variablen gemanaged.

// Check if user looks like a search bot.
$clientIsSearchEngine = checkIfSearchEngine();
if(!$clientIsSearchEngine){
	ini_set('session.use_trans_sid', true);
	ini_set('session.use_only_cookies', false);
	ini_set("display_errors","true");
	error_reporting(E_ALL);
	session_start();

	// Store language in session variable
	if (isset ($_GET["lang"]))
		$_SESSION["lang"] = $_GET["lang"];
	elseif( !isset($_SESSION["lang"])){
		include_once($subdir."php/default_language.php");
		if( isset($_SERVER['HTTP_ACCEPT_LANGUAGE'] ) ){
			$_SESSION["lang"] = prefered_language($supportedLanguages, @$_SERVER['HTTP_ACCEPT_LANGUAGE']);
		}else{
			$_SESSION["lang"] = $supportedLanguages[0];
		}
	}

}

//Falls Cookies nicht erlaubt sind, aber eine neue Session initialisiert wurde, soll die gleiche Seite mit dem Sessionparameter neu geladen werden.
//Dann wird später beim Drücken von F5 keine neue Session angelegt.
//Falls die Sessionid in einem Cookie gespeichert wird, ist das nicht notwendig.
//Suchmaschinen müssen ausgeschlossen werden, da dort keine Session initialisiert ist.
if( !$clientIsSearchEngine &&  !array_key_exists("previousSessionLoad",$_SESSION) && SID!="" && !isset($_COOKIE)){
	$url = $_SERVER["REQUEST_URI"];
	if(strpos($url,"?") === false)
		$url .= "?".SID;
	else
		$url .= "&".SID;

	$_SESSION["previousSessionLoad"]="1";
/*echo "Location: $url";
echo '<br>$_Cookie? '.isset($_COOKIE);
echo '<br>$_Cookie["PHPSESSID"]? '.array_key_exists("PHPSESSID",$_COOKIE);//der schlüssel exisiert noch nicht!!
exit();*/
	header("Location: ".$url);
}
//$tmpSID = SID;
//echo "Test ".(defined(SID)==true?'Ja':'Nein');


// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
/* == Include template System == */
include_once($subdir."templates/template.class.php");

/* == Init language template class == */
global $tpl;
$tpl = new Template($_SESSION["lang"]);

/* $lang is a global array which stores all language specific
 * tokens. The array can be extend by the call of
 * $tpl->loadLanguage($langs, $lang) where $langs contains
 * a list of language files.
 * As default $langs only contains 'menu.php' for the right
 * menu links.
 */
$lang = array();
$langs[] = "menu.php"; 

/* Load given langs files. 
 * ( Multiple calls of loadLanguage only load new
 * entries of langs )
 */
$tpl->loadLanguage($langs, $lang);

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



?>
