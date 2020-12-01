<?php
// set $subdir to ../ if the php file will move to a subdirectory.
 //$subdir = "../";
$subdir = "";

//set the var $htmlHead, if you want add html code between the <head> tags.
include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->
<?php
/* The initialisation of tables was moved to
 * the first call of the login page.
 * You can uncomment it here for debugging. */
//init_main_database_tables();

include_once($subdir."contentmanager/News.functions.php");
include_once($subdir."contentmanager/Game.functions.php");
include_once($subdir."contentmanager/Download.functions.php");

$html = '';
$html .= '<table style="width:100%;"><tr><td rowspan="2" style="width:60%;padding-right:1em">';
$html .= '<h2>{L_GAMES}</h2>';
$html .= gamesListShort("Games",0,20);
$html .= '<p><a href="games.php" dyn>{L_GAMES_DISPLAY_ALL}</a></p>';
$html .= '</td><td><h2>{L_NEWS}</h2>';
$html .= newsListShort("News",0,3);
$html .= '<p><a href="news.php" dyn>{L_NEWS_DISPLAY_ALL}</a><p>';
$html .= '</td></tr><tr><td><h2>{L_DOWNLOADS}</h2>';
$html .= downloadListShort("Downloads",0,5);
$html .= '<p><a href="downloads.php" dyn>{L_DOWNLOADS_DISPLAY_ALL}</a></p>';
$html .= '</td></tr></table>';

echo translate($html);

?>


<?php 

include($subdir."php/footer.php");
?>
