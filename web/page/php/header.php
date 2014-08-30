<?php

//ueberfluessig...
if(! isset($subdir)) $subdir="";
if(! isset($htmlHead)) $htmlHead="";
if(! isset($htmlTitle)) $htmlTitle="PB Stats";

include_once($subdir."php/header_all_pages.php");


//Teste, ob der Parameter loadViaAjax existiert. In diesem Fall wurde die Seite über Ajax angefordert und es muss auf das HTML-Gerüst verzichtet werden. 
if(array_key_exists("loadViaAjax",$_GET)) {
	if(is_array($_SESSION))
		$_SESSION["lastAjaxSite"] = $_SERVER["REQUEST_URI"];
	return;
}else{
	if( !$clientIsSearchEngine && array_key_exists("lastAjaxSite",$_SESSION)){
		$url = $_SESSION["lastAjaxSite"];
		$url = preg_replace('/loadViaAjax=1/','',$url);
		header("Location: ".$url);
		unset($_SESSION["lastAjaxSite"]);
		//	echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="refresh" content="0; URL="'.$_SESSION["lastAjaxSite"].'"><title></title></head><body>Redirecting.</body></html>';
		exit();
	}
	unset($_SESSION["lastAjaxSite"]);
}

echo'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
	<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<!--<meta name="author" content="None">
	<meta name="publisher" content="www.civforum.de">
	<meta name="Content-Language" content="de">
	<meta name="language" content="german">-->
	<meta name="keywords" content="civ civlization civlisation 4 civ4 bts beyond the sword mod pitboss civstats">
	<meta name="description" content="Übersichtseite für Civ4-Pitboss-Spiele">
	<meta name="content-language" content="english">
	<meta name="page-topic" content="">
	<meta name="distribution" content="global">
	<meta name="robots" content="all">
	<meta name="robots" content="index">
	<meta name="robots" content="follow">
	<meta name="generator" content="vim">';


echo '<title>'.$htmlTitle.'</title>
	<link rel=stylesheet type="text/css" href="'.$subdir.'style/style.css" media="screen, projection, tv">
	<link rel=stylesheet type="text/css" href="'.$subdir.'style/style.css" media="handheld">
	<link rel=stylesheet type="text/css" href="'.$subdir.'style/pbmod.css" media="screen, projection, tv,handheld">
	<!--<link rel=stylesheet type="text/css" href="'.$subdir.'style/print.css" media="print">-->
	<script src="'.$subdir.'js/helpers.js" type="text/javascript"></script>
<script src="'.$subdir.'js/liam.js" type="text/javascript"></script>
<script src="'.$subdir.'js/timezone.js" type="text/javascript"></script>
<script src="'.$subdir.'js/ajax.js" type="text/javascript"></script>'.
$htmlHead.'</head>
<body class="backgroundImage" '.(hasValue("fontsize",$_COOKIE)?'style="font-size:'.$_COOKIE["fontsize"].'"':'').' >';

//rechte Navigationsleiste
echo '<div id="rightFrame">';
include("headerlinks.php");

//iframe für die History, die durch reines Ajax-Laden nicht aktualisiert wird
//todo: in request_uri könnten sonderzeichen enthalten sein, die einer Umwandlung bedürfen
function curPageURL() {
	$pageURL = 'http';
	if(array_key_exists("HTTPS",$_SERVER) && $_SERVER["HTTPS"] == "on") {$pageURL .= "s";}
	$pageURL .= "://";
	if($_SERVER["SERVER_PORT"] != "80") {
		$pageURL .= $_SERVER["SERVER_NAME"].":".intval($_SERVER["SERVER_PORT"]).$_SERVER["REQUEST_URI"];
	} else {
		$pageURL .= $_SERVER["SERVER_NAME"].$_SERVER["REQUEST_URI"];
	}
	return $pageURL;
}

echo '<iframe src="'.$subdir.'ifrm.php?startpage='. htmlspecialchars(curPageURL()) .'" width="100" height="20" name="historyFrm" frameborder="0" srcolling="0" id="historyFrm" style="display:none">Keine IFrame-Unterstützung.</iframe>';

echo '</div>';


echo '
	<div id="leftFrame">
	<div id="header" class="backgroundColor3x">

	<div id="headerCenter">
	<div id="headerCenterBottom">
	<div id="headerCenterCIV4"> ⊶⊷</div>
	<div id="headerCenterText">
	<h1><a href="'.$subdir.'index.php'.'" dyn>Display and<br>Manage Pitboss Games</a></h1></div>
	</div>
	<div id="logo"></div>
	</div>
	<!--<div id="logo"></div>-->
	</div>

	<!--<div id="leftBlock"></div>-->
	<div id="mainBlock" class="backgroundColorT">
	<div id="centerBlock">
	<div id="ajaxInfo"></div><div id="ajaxContent">';

?>
