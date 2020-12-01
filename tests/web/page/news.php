<?php
// set $subdir to ../ if the php file will move to a subdirectory.
 //$subdir = "../";
$subdir = "";

//set the var $htmlHead, if you want add html code between the <head> tags.
 include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->
<?php 
include($subdir."contentmanager/News.functions.php");

// Add language dict file(s)
$langs[] = "contentmanager.php"; 
$tpl->loadLanguage($langs, $lang );


if(isset($_GET['news'])){
	$thtml = newsSingle("News",$_GET['news']);
	$tpl->loadStr($thtml);
	echo $tpl->out();
}else{
	$nbrOfEntrys = 20;
	if(isset($_GET['page'])){
		$page = $_GET['page'];
		echo newsListFull("News",($page-1)*$nbrOfEntrys,$nbrOfEntrys);
	}else
		echo newsListFull("News",0,$nbrOfEntrys);
}
?>
<br><br><br>
<?php 

include($subdir."php/footer.php");
?>
