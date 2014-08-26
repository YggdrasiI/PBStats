<?php
// set $subdir to ../ if the php file will move to a subdirectory.
//$subdir = "../";
$subdir = "";
include_once("php/header_all_pages.php");

$login=0;

if( isset($_SESSION['loginName']) ){
	//backup language
	if( isset( $_SESSION['lang'] ) ) $userLang = $_SESSION['lang'];

	//Destroy old session
	session_unset();
	session_destroy();
	/*
	if( isset( $_SESSION['loginName'] ) ) unset($_SESSION['loginName']);
	if( isset( $_SESSION['loginId'] ) ) unset($_SESSION['loginId']);
	if( isset( $_SESSION['loginLevel'] ) ) unset($_SESSION['loginLevel']);
	 */

	//Start new session
	session_start();
	$_SESSION['logout'] = 1;
	$_SESSION['lang'] = $userLang;

	/* Note: It's neccessary to send these headers to reset
	 * the saved password on client side. Otherwise the browser
	 * will used the saved login name and password and it's not
	 * possible to login as other user. */
	header('WWW-Authenticate: Basic realm="pbstats authentication."');
	header('HTTP/1.0 401 Unauthorized');
}

if(array_key_exists("from",$_GET)){
	//header("Location: ".$_GET["from"]);
}else{
	//header("Location: index.php");
}

?>

<?php

//set the var $htmlHead, if you want add html code between the <head> tags.
include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->
<?php
//should never be reached due redirection to index page on successful logout.
echo translate("<h2>{L_NOTE}</h2><p>{L_SUCCESSFUL_LOGOUT}</p>");
?>

<?php 

include($subdir."php/footer.php");
?>
