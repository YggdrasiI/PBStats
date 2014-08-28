<?php

$loginLevel = 0;
if( isset($_SESSION["loginLevel"]) && $_SESSION["loginLevel"] > 0 ){
	$loginLevel = $_SESSION["loginLevel"];
}

/*
erster Parameter: Einrückung
vorletzter Parameter: Verzeichnistiefe für relative Links.
letzter Parameter: Link ist via Ajax ladbar. Link wird dann um onClick angereichert. Falls Ajax-Funktion nicht klappt, wird dem normalen Link gefolgt.
*/
$links = array(
"civforum" => array("0","{L_MENU_CIVFORUM}","http://www.civforum.de","0",false),
"main" => array("0","{L_MENU_INDEX}","index.php","0",true),
//"news" => array("1","{L_MENU_NEWS}","news.php","0",true),
"games" => array("1","{L_MENU_GAMES}","games.php","0",true),

"create" => array("1","{L_MENU_GAME_CREATE}",
$loginLevel>0?"contentmanager/index.php?contentList=Games&act=add"
:"login.php?from=contentmanager/index.php%3FcontentList=Games%26act=add"
,"0",true),
"change" => array("1","{L_MENU_GAME_MANAGE}",
$loginLevel>0?"contentmanager/index.php?contentList=Games&act=change"
:"login.php?from=contentmanager/index.php%3FcontentList=Games%26act=change"
,"0",true),

//"downloads" => array("1","{L_MENU_DOWNLOADS}","downloads.php","0",true),

"contact" => array("1","{L_MENU_CONTACT}","contact.php","0",true),
);

if( isset($_SESSION["loginLevel"]) && $_SESSION["loginLevel"] > 1 ){
	$links["manager"] = array("1","{L_MENU_MANAGER}","contentmanager/index.php","1",true);
}


$html = '';

$urlx = explode('/',$_SERVER['PHP_SELF']);

//remove extension in the last str.
$pos= strrpos($urlx[count($urlx)-1],'.');
if($pos!==false)
	$urlx[count($urlx)-1] = substr($urlx[count($urlx)-1],0,$pos);

//Login or Logout link
$html .= "<p>";

//$html .= print_r($_SESSION);

if( !isset( $_SESSION["loginName"] ) || $_SESSION["loginName"] === "" ){
	//minor change on the uri argument if user is on the logout page.
	if( isset( $_SESSION["logout"] ) ) {
		$html .= "<a href='".$subdir."login.php"."' static>{L_MENU_LOGIN}</a>";
	}else{
		$html .= "<a href='".addUriVar($subdir."login.php","from",$_SERVER["SCRIPT_NAME"])."' static>{L_MENU_LOGIN}</a>";
	}
	$html .= " <a href='".$subdir."contentmanager/index.php?act=add&contentList=Users&send=Ok"."' static>{L_MENU_REGISTRATION}</a>";

}else{
	$html .= "<a href='".addUriVar($subdir."logout.php","from",$_SERVER["SCRIPT_NAME"])."' static>{L_MENU_LOGOUT} (".$_SESSION["loginName"].")</a>";
	}
$html .= "</p>";

// Menu links
foreach( $links as $group => $url){
	$pos = count($urlx)-$url[3]-1;
	if($group=="civforum") $html .= "<br><br>";
	if($pos>=0)
		$filegroup = $urlx[$pos];
	$html .= '<a style="margin-left:'.(0.5+0.2*$url[0]).'em" name="rfLink" href="'.$subdir.$url[2].'"'.(($filegroup==$group)?' class="active"':'').(($url[4]===false)?' static':'').'>'.$url[1].'</a>'."\r\n";
}

//$uri =  $_SERVER["REQUEST_URI"];/* Keep get variables. Use of request uri can be a security problem */
//$uri = $_SERVER["SCRIPT_NAME"]; /* Lost get and post variables */
$uri = $subdir.'index.php'; //dumbest but secure solution...

$html .= '<div id="flaggen">';
//$html .= '<br>Selected:'.$_SESSION["lang"].'<br>';
$html .= '
	<a href="'.addUriVar($uri,"lang","de").'" static>
	<img width="20%" src="'.$subdir.'style/flaggeGer.gif"></a>
	<a href="'.addUriVar($uri,"lang","en").'" static>
	<img width="20%" src="'.$subdir.'style/flaggeEng.gif"></a>
	<a href="'.addUriVar($uri,"lang","fr").'" static>
	<img width="20%" src="'.$subdir.'style/flaggeFra.gif"></a>
</div>';

$html .= '<div id="fontSizeSelector"><p>
	<span style="font-size:160%;" onclick="resizeText(0.8);">A</span>
	<span style="font-size:200%;" onclick="resizeTextToDefault();">A</span>
	<span style="font-size:240%;" onclick="resizeText(1.2);">A</span>
	</p>
	</div>
	';

$timezone = "Select Timezone";
if( isset( $_COOKIE["timezone"] ) ){
		$timezone = $_COOKIE["timezone"];
}
$html .= '<div id="timezoneSelector"><span onClick="getTimezoneList(this,\''.$timezone.'\');">'.$timezone.'</span></div>';



//Indexseiten Template laden
// Das Template laden
$tpl->loadStr($html);

//Ersetzungen mir vordefinierten Token vornehmen
$tpl->setLanguageTokens($lang);

// Und das fertige Template ausgeben
echo $tpl->out();

?>
