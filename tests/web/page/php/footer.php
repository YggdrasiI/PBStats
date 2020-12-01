<?php

//echo '<div id="footer">Letztes Update: '. date("d.m.Y - H:i", filemtime(basename($_SERVER["SCRIPT_FILENAME"]))).'</div>';

/*echo "SESSION-ID:".session_id()."<br>";
echo "SESSION: ";
print_r ($_SESSION);*/
//if( $clientIsSearchEngine) echo "Debug: User was detecdet as search engine.";
// Check if param RANDOM exists. In this case, the site was requested by ajax. Omit
// the html skeleton/frame in header and footer.
if(array_key_exists("loadViaAjax",$_GET) && $_GET["loadViaAjax"]) return;


echo '</div>
</div></div>
</div>';

/*echo '<div id="rightFrame">';
include("headerlinks.php");
echo '</div>';*/


echo'
</body>
</html>';
?>




