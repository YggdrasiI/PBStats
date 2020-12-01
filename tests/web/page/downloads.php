<?php
// set $subdir to ../ if the php file will move to a subdirectory.
 //$subdir = "../";
$subdir = "";

//set the var $htmlHead, if you want add html code between the <head> tags.

include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->
<h2>Downloads</h2>
<p><b>!</b> Some files require a registered Account.</p>

<?php 
include($subdir."contentmanager/Download.functions.php");

if( array_key_exists("ab",$_GET))
  $ab = $_GET["ab"];
else
 $ab = 0;

if( array_key_exists("max",$_GET))
 $maxNbr = $_GET["max"];
else
 $maxNbr = 40;

//Display content of one category or
//all categories
if( array_key_exists("catId",$_GET))
	echo downloadListCat($_GET["catId"]);
else
	echo downloadListFull($ab,$maxNbr);
?>
<?php 

include($subdir."php/footer.php");
?>
