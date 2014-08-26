<?php
// set $subdir to ../ if the php file will move to a subdirectory.
 //$subdir = "../";
$subdir = "";

//set the var $htmlHead, if you want add html code between the <head> tags.
 include($subdir."php/header_all_pages.php");

?>
<!-- Paste/Write content here -->
<?php 
include($subdir."contentmanager/Game.functions.php");

/*
 * Debug function to analyse input
 */
function logWrite($str){
	$filename = "../files/log.txt";
	if (!$handle = fopen( $filename, "w")) {
		print "Kann die Datei $filename nicht öffnen";
		exit;
	}

	// Schreibe $somecontent in die geöffnete Datei.
	if (!fwrite($handle, $str)) {
		print "Kann in die Datei $filename nicht schreiben";
		exit;
	}
	print "Fertig, in Datei $filename wurde $str geschrieben";
	fclose($handle);
}
/**/


if( isset( $_POST["action"] ) && $_POST["action"] === "update" ){


	//Save gamestatus in database
	$gameId = $_POST["id"];
	$infos = json_decode($_POST["info"]);
	if( $infos->return === "ok" ){

		//Read game config from db
		$gameData = get_game_data($gameId);


		$pwHashLocal = $gameData["managePasswordHash"];
		//$pwHashRemote = $infos->pwHash;//wrong
		$pwHashRemote = $_POST["pwHash"];

		/*
			logWrite("message". print_r($_POST,1) 
			. $pwHashLocal." , ". $pwHashRemote
			. strlen($pwHashLocal)." , ".strlen($pwHashRemote) );
		 */

		if( $pwHashLocal == $pwHashRemote ){

			$newGameStatus = $infos->info;
			$newGameStatus->players = append_status($newGameStatus->players);

			$dtobj = new DateTime();
			$curTime = $dtobj->getTimestamp ( );
			$cachedStatus = get_cached_game_status($gameId);
			$oldGameStatus = json_decode($cachedStatus["jsonStatus"]);

			if( $oldGameStatus != null ){
				$oldGameStatus->players = append_status($oldGameStatus->players);
				update_game_log($gameId, $curTime, $newGameStatus, $oldGameStatus );
			}

			set_cached_game_status($gameId,$newGameStatus);

			//Update saved ip if difference detected
			if( intval($gameData["urlUpdate"]) > 0 ){
					$newIp = filter_var($_SERVER['REMOTE_ADDR'], FILTER_VALIDATE_IP);
					$oldIp = $gameData["url"];

					if( $newIp !== $oldIp ){
						$gameTableName = $contentTables["Games"]["sqlTable"];
						$sql = "UPDATE " . $gameTableName . " SET url = ?, port = ? WHERE id = ?";
						$preparedValues = array($newIp, $gameData["port"], $gameData["id"] );
						$db = get_db_handle();
						try{
							$statement = $db->prepare($sql);
							$result  = $statement->execute($preparedValues);
						}catch(Exception $e){
							echo 'Exception : '.$e->getMessage();
						}
						unset($db);
					}
			}


			echo "</head><body>ok</body></html>";
		}else{
			echo "</head><body>wrong hash</body></html>";
		}
	}else{
		echo "</head><body>wrong intput</body></html>";
	}
}else{
	echo "</head><body>wrong arguments";

	$gameData = get_game_data(1);
	$newIp = filter_var($_SERVER['REMOTE_ADDR'], FILTER_VALIDATE_IP);
	$oldIp = "Bla"; 

	if( $newIp !== $oldIp ){
		$gameTableName = $contentTables["Games"]["sqlTable"];
		$sql = "UPDATE " . $gameTableName . " SET url = ?, port = ? WHERE id = ?";
		$preparedValues = array($newIp, $gameData["port"], $gameData["id"] );
		$db = get_db_handle();
		try{
			$statement = $db->prepare($sql);
			$result  = $statement->execute($preparedValues);
		}catch(Exception $e){
			echo 'Exception : '.$e->getMessage();
		}
		unset($db);
	}
	/*
	$gameId = 1;
	$gameData = get_game_data($gameId);
	$pwHashLocal = $gameData["managePasswordHash"];
	echo "$pwHashLocal";
	//echo hash('md5', 'hello');	
	 */

	echo "</body></html>";
}

?>
