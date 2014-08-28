<?php

/*
=========== Sorting functions =======================
 */

//=== Sorting functions
function sortById($a, $b) {
	$s = 0;
	if( $s == 0 ) $s = $a->id - $b->id;
	if( $s == 0 ) $s = $b->score - $a->score;
	if( $s == 0 ) $s = strcmp($a->name, $b->name);
	return $s;
};
function sortByName($a, $b) {
	$s = 0;
	if( $s == 0 ) $s = strcmp($a->name, $b->name);
	if( $s == 0 ) $s = $b->score - $a->score;
	if( $s == 0 ) $s = $a->id - $b->id;
	return $s;
};
function sortByScore($a, $b) {
	$s = 0;
	if( $s == 0 ) $s = $b->score - $a->score;
	if( $s == 0 ) $s = strcmp($a->name, $b->name);
	if( $s == 0 ) $s = $a->id - $b->id;
	return $s;
};
function sortByEndTurn($a, $b) {
	$s = 0;
	if( $s == 0 ) $s = $a->finishedTurn - $b->finishedTurn;
	if( $s == 0 ) $s = $a->id - $b->id;
	if( $s == 0 ) $s = strcmp($a->name, $b->name);
	if( $s == 0 ) $s = $b->score - $a->score;
	return $s;
};
function sortByStatus($a, $b) {
	$s = 0;
	if( $s == 0 ) $s = -strcmp($a->ping, $b->ping);
	if( $s == 0 ) $s = strcmp($a->name, $b->name);
	if( $s == 0 ) $s = $b->score - $a->score;
	if( $s == 0 ) $s = $b->id - $a->id;
	return $s;
};
function sortByLeader($a, $b) {
	$s = 0;
	if( $s == 0 ) $s = strcmp($a->leader, $b->leader);
	if( $s == 0 ) $s = $b->score - $a->score;
	if( $s == 0 ) $s = $b->id - $a->id;
	if( $s == 0 ) $s = strcmp($a->name, $b->name);
	return $s;
};
function sortByCiv($a, $b) {
	$s = 0;
	if( $s == 0 ) $s = strcmp($a->civilization, $b->civilization);
	if( $s == 0 ) $s = $b->score - $a->score;
	if( $s == 0 ) $s = $b->id - $a->id;
	if( $s == 0 ) $s = strcmp($a->name, $b->name);
	return $s;
};

/*
=========== END Sorting functions ====================
 */

//Create sorting link
function sortLink($gameId,$sort, $index){
	global $this_page;
	return "$this_page?game=$gameId&action=list&sort=".($sort==$index?"-$index":"$index");
}

//Create link on log of specific player
function playerLogLink($gameId,$sort, $playerId){
	global $this_page;
	return "$this_page?game=$gameId&action=log&sort=$sort&logId=$playerId";
}

//Convert ping message into player status
function append_status($players){
	foreach( $players as $player ){
		$statusId = 0;
		if( $player->score > 0 ){
			$ping = $player->ping;
			if( $ping[0] === "A" ){ $statusId = 1; }
			elseif( $ping[0] === "D" ){ $statusId = 2; }
			elseif( $ping[1] === "[" ){ $statusId = 3; }
			elseif( $ping[0] === "U" ){ $statusId = 4; }
			else{ $statusId = 5; }
		}
		$player->statusId = $statusId;
	}
	return $players;
}

function handle_pitboss_action($gameData, $arr_in) {

	$error = null;
	try{
		$address = gethostbyname($gameData["url"]);
		$port = $gameData["port"];
		$host = "";
		$url = "/api/v1/";

	/* gethostbyname return value sucks if hostname in gameData is ip
		if( $address === "?" ){
			$error = array( "return"=>"failed","info" => "Can not resolve hostname.");
			return json_encode($error);
	}*/

		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		if ($socket === false) {
			unset($socket);
			throw new Exception ( "socket_create() failed. Reason: " .
				socket_strerror(socket_last_error()) );
		}

		//$timeout = array('sec'=>0,'usec'=>500000);
		$timeout = array('sec'=>1,'usec'=>0);
		socket_set_option($socket,SOL_SOCKET,SO_RCVTIMEO,$timeout);

		if (!socket_connect ($socket, $address, $port)) {
			throw new Exception ( "socket_connect() failed. Reason: " .
				socket_strerror(socket_last_error()) );
		}

		$request = json_encode( $arr_in );

		$httpQuery = "POST ". $url ." HTTP/1.0\r\n";
		//$httpQuery .= "User-Agent: jsonrpc\r\n";
		$httpQuery .= "Host: ". $host ."\r\n";
		$httpQuery .= "Content-Type: application/json\r\n";
		$httpQuery .= "Content-Length: ". strlen($request) ."\r\n\r\n";
		$httpQuery .= $request ."\r\n";

		if (!socket_send($socket, $httpQuery , strlen($httpQuery), MSG_EOR /*0, MSG_EOF*/)) {
			throw new Exception ( "socket_send() failed. Reason: " .
				socket_strerror(socket_last_error()) );
		}

		//2. Get reply
		$jsonResponse = "";
		$buff = "";
		while ($bytes = socket_recv($socket, $buff, 1024, MSG_WAITALL) > 0) {
			$jsonResponse .= $buff;
		}

		if( strlen($jsonResponse) < 1 ){
			throw new Exception( "socket_recv() failed. Reply string was empty . Error: " .
				socket_strerror(socket_last_error($socket))  );
		}

		// Just for debugging
		if( socket_last_error($socket) ){
			throw new Exception( "socket_recv() failed. Reason: " .
				socket_strerror(socket_last_error($socket)) . "\n" );
		}

		socket_close($socket);
		unset($socket);

		//Cut of header, which ends with \r\n\r\n
		//echo $jsonResponse;
		$jsonResponse = substr($jsonResponse,3+strpos($jsonResponse,"\n\r\n"));

	}catch(Exception $e){
		$error = array('return'=>'failed','info'=>'Socket connection failed. Error: '.$e->getMessage() );
	} /*finally (require >= PHP 5.5) */ if( isset($socket) ) {
		socket_close($socket);
		unset($socket);
	}

	if( $error !== null ){
		return json_encode($error);
	}
	return $jsonResponse;
}

/*
 * This variant use http_put_data()
 * which require the PECL extension.
 * http://php.net/manual/de/http.setup.php
 */
function handle_pitboss_action_variant2($gameData, $arr_in) {

	$error = null;
	try{
		$address = gethostbyname($gameData["url"]);
		$port = $gameData["port"];
		$host = "";
		$url = "/api/v1/";

	/* gethostbyname return value sucks if hostname in gameData is ip
		if( $address === "?" ){
			$error = array( "return"=>"failed","info" => "Can not resolve hostname.");
			return json_encode($error);
	}*/

		$headers = array(
			"Host" => $host,
			"Content-Type" => "application/json",
		);
		$options = array(
			'useragent'      => "PBStats",
			'connecttimeout' => 2, 
			'timeout'        => 2,
			'redirect'       => 5,
			'headers'        => $headers,
		);

		$request = json_encode( $arr_in );

		$jsonResponse = http_put_data($address.$port.$url, $request, $options);

		if( $jsonResponse === FALSE /*|| strlen($jsonResponse) < 1*/ ){
			throw new Exception( "http_put_data() failed." );
		}

		echo $jsonResponse;
		$jsonResponse = substr($jsonResponse,3+strpos($jsonResponse,"\n\r\n"));

	}catch(Exception $e){
		$error = array('return'=>'failed','info'=>'Socket connection failed. Error: '.$e->getMessage() );
	} 

	if( $error !== null ){
		return json_encode($error);
	}
	return $jsonResponse;
}


//Check counter in the cookie to omit multiple calls of same command.
function operation_already_done($val){
	global $operationIds;
	if( $val < 0 ) return true;
	if( count ( array_keys( $operationIds, $val ) ) > 0 ){
		return true;
	}
	return false;
}

function operation_update_ids( $val ){
	global $operationIds;
	if( $val < 0 ) return;

	$keys = array_keys($operationIds);
	$maxIndex = max($keys);
	$c = 10;
	while( count( $operationIds ) > 30 && $c>0 ){
		$c -= 1;
		//Remove old ids
		$minIndex = min($keys);
		unset($operationIds[$minIndex]);
		$keys = array_keys($operationIds);
	}
	$newIndex = $maxIndex + 1;
	$operationIds[$newIndex] = $val; 

	$opString = json_encode( $operationIds );
	$expire=time()+60*60*24*30;
	setcookie("operationIds", $opString, $expire);

}

function operation_new_val(){
	global $operationIds;
	//return (max($operationIds) + 1);
	return ((time()&0x0FFF)<<10)+rand(0,1024);
}

function print_operation_error_msg(){
	return "<h3 class='hr pad' style='color:red'>{L_ERROR}</h3><p>{L_GAME_OPERATION_ALREADY_DONE}</p>";
}

function get_number_of_connected_players($players){
	$c = 0;
	foreach( $players as $player ){
		if( $player->ping[1] === "[" ){
			$c += 1;
		}
	}
	return $c;
}

function get_number_of_living_players($players){
	$c = 0;
	foreach( $players as $player ){
		if( $player->score > 0 ){
			$c++;
		}
	}
	return $c;
}


function display_game_action_links($gameId){
	global $this_page;
	$dHtml = '';
	$dHtml .= "<div class='linkContainer'>\n";
	$dHtml .= "<h3>Administration</h3>\n";
	$dHtml .= "<a href='$this_page?game=$gameId&action=setWebserverpassword'> Enter Game Administration Password </a><br>\n";
	$dHtml .= "<a href='$this_page?game=$gameId&action=admin'> Admin Menu </a><br>\n";
	$dHtml .= "<a href='$this_page?game=$gameId&action=save'> Save Menu </a><br>\n";
	$dHtml .= "<a href='$this_page?game=$gameId&action=restart'> Restart Menu </a><br>\n";
	$dHtml .= "</div>\n";

	return $dHtml;
}


function display_game_log($gameData){

	$gameId = $gameData["id"];

	$dHtml = '';

	$dHtml .= "<div class='logContainer'>";
	$dHtml .= "<h3>Game Log</h3>";
	$dHtml .= "<table class='log'><thead><tr><td>Time</td><td>Player</td><td>Event</td></tr></thead>\n";

	$db = get_db_handle();
	if( $db != null ){
		$bRestrictOnUser = isset($_GET["logId"]);
		if( $bRestrictOnUser ){
			$where="WHERE gameId=? AND (playerId=? OR playerId=-1)";
		}else{
			$where="WHERE gameId=?";
		}
		$sql = "SELECT timestamp,playerName,message,messageType FROM log $where ORDER BY id DESC LIMIT 200";
		$statement = $db->prepare($sql);
		$statement->bindValue(1, $gameId,  PDO::PARAM_INT);
		if( $bRestrictOnUser ){
			$statement->bindValue(2, intval($_GET["logId"]),  PDO::PARAM_INT);
		}
		$result = $statement->execute();

		check_pdo_error($db);
		$localDate = localDateTime();

		while( $result && $res = $statement->fetch(PDO::FETCH_ASSOC) )
		{
			$localDate->setTimestamp($res["timestamp"]);
			$dHtml .= "<tr class='".$res["messageType"]."'><td>" .	$localDate->format("d M H:i") . "</td><td>"
				. $res["playerName"] . "</td><td>" . translate($res["message"]) . "</td></tr>\n";
		}
	}
	$dHtml .= "</table>";
	$dHtml .= "</div>\n";

	return $dHtml;
}

function display_game_info($gameData){
	global $status_strings;

	$gameId = $gameData["id"];

	$dHtml = '';
	$dtobj = new DateTime();
	$curTime = $dtobj->getTimestamp ( );
	$cachedStatus = get_cached_game_status($gameId);

	$gameStatus = null;
	$timeDiff = 0;
	if( $cachedStatus != null){
		$timeDiff = $curTime - $cachedStatus["timestamp"];
	}

	//try cache, otherwise request new data
	if( $cachedStatus != null && $timeDiff < 12 ){
		$gameStatus = json_decode($cachedStatus["jsonStatus"]);
	}else{
		$action_info = array('action'=>'info');
		$infos = json_decode(handle_pitboss_action($gameData, $action_info));

		if( $infos->return !== "ok" ){
			$dHtml .= "<p>{L_GAME_STATUS_ERROR}";
			if( isset($infos->info ) ){
				$dHtml .= print_r($infos->info, 1);
				$dHtml .= "</p><p>";
			}
			if( $cachedStatus != null ){
				$dHtml .= "</p><p>{L_GAME_CONNECTION_ERROR1}\n";
				$gameStatus = json_decode($cachedStatus["jsonStatus"]);
			}else{
				$dHtml .= "</p><p>{L_GAME_CONNECTION_ERROR2}\n";
			}
			$dHtml .= "</p>";
		}else{
			$gameStatus = $infos->info;	
			$players = append_status($gameStatus->players);

			//Compare current status with last status to track changes in the log
			if( $cachedStatus != null ){
				$oldGameStatus =	json_decode($cachedStatus["jsonStatus"]);
				$oldGameStatus->players = append_status($oldGameStatus->players);
				update_game_log($gameId, $curTime, $gameStatus, $oldGameStatus );
			}

			//Save gamestatus in database
			set_cached_game_status($gameId,$gameStatus);
		}
	}

	if( $gameStatus != null ){
		$dHtml .= "<div class='statusContainer'>";
		$dHtml .= "<h3>{L_GAME_STATUS}</h3>\n";
		$dHtml .= "<div class='status'>";
		$dHtml .= "<p>{L_GAME_NAME}: " . $gameStatus->gameName . "</p>\n";
		$dHtml .= "<p>{L_GAME_TURN}: " . $gameStatus->gameTurn . "</p>\n";
		$dHtml .= "<p>{L_GAME_DATE}: " . $gameStatus->gameDate . "</p>\n";
		if( $gameStatus->turnTimer != 0 ){
			$seconds = intval($gameStatus->turnTimerValue)/4;
			$seconds -= $timeDiff;
			$timerString =	gmdate("H:i:s", $seconds);
			$timerLimit = $gameStatus->turnTimerMax;
			$dHtml .= "<p>{L_GAME_TIMER}: <b>" . $timerString . "</b> from $timerLimit hours left.</p>\n";
		}else{
			//$dHtml .= "<p>Timer: Not set</p>";
		}
		$dHtml .= "<p>{L_GAME_PAUSED}: " . ($gameStatus->bPaused==1?"{L_YES}":"{L_NO}") . "</p>\n";
		$dHtml .= "<p>{L_GAME_COMMENT}: {$gameData['description']}</p>\n";
		$dHtml .= "</div></div>\n";


		$players = $gameStatus->players;	
		$players = append_status($players);

		$sort = 3;
		if( isset($_GET["sort"]) ){
			$sort = intval($_GET["sort"]);
		}
		switch ( abs($sort) ){
		case 1:
			usort($players, 'sortById');
			break;
		case 2:
			usort($players, 'sortByName');
			break;
		case 3:
			usort($players, 'sortByScore');
			break;
		case 4:
			usort($players, 'sortByEndTurn');
			break;
		case 5:
			usort($players, 'sortByStatus');
			break;
		case 6:
			usort($players, 'sortByLeader');
			break;
		case 7:
			usort($players, 'sortByCiv');
			break;
		default:
			usort($players, 'sortByScore');
		}
		if( $sort < 0 ){
			$players = array_reverse($players);
		}

		//Table Header
		$dHtml .= "<div class='playerContainer'>\n";
		$dHtml .= "<h3>{L_GAME_PLAYERS}</h3>\n";
		$dHtml .= "<table class='players' style='margin-left:6em'><tr>\n
			<td><a href='".sortLink($gameId,$sort,4)."' style='margin-left:-6em;'>{L_GAME_END_TURN}</a></td>\n
			<td><a href='".sortLink($gameId,$sort,1)."'>Id</a></td>\n
			<td><a href='".sortLink($gameId,$sort,2)."'>{L_GAME_PLAYER}</a></td>\n
			<td><a href='".sortLink($gameId,$sort,6)."'>{L_GAME_LEADER}</a></td>
			<td><a href='".sortLink($gameId,$sort,7)."'>{L_GAME_CIVILIZATION}</a></td>\n
			<td><a href='".sortLink($gameId,$sort,3)."'>{L_GAME_SCORE}</a></td>\n
			<td><a href='".sortLink($gameId,$sort,5)."'>{L_GAME_PLAYER_STATUS}</a></td>\n
			";
		$dHtml .= "</tr>\n";

		foreach( $players as $player ){
			$rgb = $player->color;
			$color = explode(",",$rgb);

			$invertTextcolor = false; 
			if( count($color)>2 && ($color[0]+$color[1]+$color[2])>380 ){
				$invertTextcolor = true;
			}

			//Reduce saturation
			/*
			$grey = array_sum($color)/floatval(count($color));
			$color[0] = ($color[0]+$grey)/2.0;
			$color[1] = ($color[1]+$grey)/2.0;
			$color[2] = ($color[2]+$grey)/2.0;
			 */
			//Reduce hue
			$color[0] = $color[0]*0.4;
			$color[1] = $color[1]*0.4;
			$color[2] = $color[2]*0.4;
			$rgbMod = intval($color[0]).",".intval($color[1]) . "," . intval($color[2]);

			$invertTextcolorMod = false; 
			if( count($color)>2 && ($color[0]+$color[1]+$color[2])>380 ){
				$invertTextcolorMod = true;
			}

			$dHtml .= "<tr style='".($invertTextcolorMod?"color:rgb(0,0,0);":"")."background-color:rgb(".$rgbMod.")'>\n";
			$dHtml .= "<td>".($player->finishedTurn==1?"*":"")."</td>\n";
			$dHtml .= "<td style='".($invertTextcolor?"color:rgb(0,0,0);":"")."background-color:rgb(".$rgb.")'>".$player->id."</td>\n";
			$dHtml .= "<td><a href='".playerLogLink($gameId,$sort,$player->id)."'>".$player->name."</a></td>\n";
			$dHtml .= "<td>".$player->leader."</td><td>".$player->civilization."</td>\n";
			$dHtml .= "<td>".$player->score."</td>\n";
			$dHtml .= "<td>".$status_strings[$player->statusId]."</td>\n";
			$dHtml .= "</tr>\n";
		}
		$dHtml .= "</table>";
		$dHtml .= "</div>\n";
	}

	return $dHtml;
}
?>
