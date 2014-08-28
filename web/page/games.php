<?php
// set $subdir to ../ if the php file will move to a subdirectory.
 //$subdir = "../";
$subdir = "";

//set the var $htmlHead, if you want add html code between the <head> tags.
 include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->
<?php 
include($subdir."contentmanager/Game.functions.php");

// Add language dict file(s)
$langs[] = "contentmanager.php"; 
$langs[] = "games.php"; 
$tpl->loadLanguage($langs, $lang );


if(isset($_GET['game'])){
	$thtml = gameSingle("Games",$_GET['game']);
	$tpl->loadStr($thtml);
	echo $tpl->out();

	echo translate('<p><a href="'.$subdir.'games.php" dyn>{L_GAMES_DISPLAY_ALL}</a></p>');
}else{
	echo translate('<h2>{L_GAMES}</h2>');
	$nbrOfEntrys = 50;
	if(isset($_GET['page'])){
		$page = $_GET['page'];
		echo gamesListShort("Games",($page-1)*$nbrOfEntrys,$nbrOfEntrys);
	}else
		echo gamesListShort("Games",0,$nbrOfEntrys);
}
echo translate("{L_LOG_NEW_GAME|A|B}");
?>
<br><br><br>
<?php 

include($subdir."php/footer.php");
?>
