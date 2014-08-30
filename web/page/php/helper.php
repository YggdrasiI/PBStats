<?php


/*
	============== String Format Functions ==============
 */
/*
	Diese Funktionen sollten aufgerufen werden, wenn Strings einer 
	bestimmten Formatierung bedürfen. Vorallem bei der Verarbeitung von
	Formulardaten/Datenbankabfragen ist dies nützlich. Es muss nur festge-
	halten werden, für welches Feld welche Funktion verwendet werden soll.
	Beispielverwendung in php/neueInhalte.php
 */


function ClearMultipleSpace($string)
{
	//return preg_replace('/s{2,}/sm',' ',$string,PREG_SET_ORDER);
	return trim(preg_replace('/\s\s+/', ' ', $string));
}

// TODO: Should be language specific
function formatDate($timestamp){
	if( $_SESSION["lang"] === "de" ){
		return date("d. M. Y",$timestamp);
	}
	return date("F j, Y",$timestamp);
}

// TODO: Should be language specific
function formatTime($timestamp){
	if( $_SESSION["lang"] === "de" ){
		return date("H:i",$timestamp)." Uhr";
	}
	return date("g:i a",$timestamp);
}

// TODO: Should be language specific
function formatDateTime($timestamp){
	if( $_SESSION["lang"] === "de" ){
		return date("d. m. Y, H:i",$timestamp)." Uhr";
	}else if( $_SESSION["lang"] === "fr" ){
		//setlocale(LC_TIME, "fr_FR"); 
		//return  strftime("le %d %B, %Y, H:i", $timestamp);
		return date("d. B. Y, H:i",$timestamp)." (Todo)";
	}

	return date("F j, Y, g:i a",$timestamp);
}

//do nothing
function formatIdentity($str){
	return $str;
}

/* Cut of after 100 chars */
function formatShortString($str){
	$str = formatString($str);
	$str = substr($str,0,100);
	return $str;
}

/* Just strip slashes. Restrict on 30000 chars. */
function formatString($str){

	$str = (is_array($str) ? array_map('formatString', $str)
		: substr(stripslashes($str),0,30000) );

	return $str;
}

//remove all tags
function formatPureText($str){
	$str = formatString($str);
	$str = strip_tags($str);
	return $str;
}

function formatPhpString($str){
	eval("\$str=\"$str\";");
	echo $str;
	return $str;
}

function formatHtmlString($str){
	global $htmlPurifierConfig;
	$purifier = new HTMLPurifier($htmlPurifierConfig);

	$str = formatString($str);

	//recursion
/*if( is_array($str)){
	 foreach( $str as $key=>$el)
		$str[$key] = formatHtmlString($el);
return $str;
}*/

	//if (get_magic_quotes_gpc())
	//  $str = stripslashes($str);

	$str = $purifier->purify( $str );

	return $str;
}

function formatHtmlStringTextarea($str){
	global $htmlPurifierConfigTextareas;
	$purifier = new HTMLPurifier($htmlPurifierConfigTextareas);

	//$str = formatString($str);
	$str = $purifier->purify( $str );

	return $str;
}

function formatDouble($str){
	return floatval($str);
}

function formatInt($str){
	return intval($str);
}

function formatStrToDate($str){
	$str = explode(".",$str);//englische gleich deutscher reihenfolge?
	$str = array_pad($str,3,0);//auf mind. 3 Einträge verweitern
	$str = strtotime($str[2]."-".$str[1]."-".$str[0]);
	//$str = formatDate($str);
	return $str;
}

// muss auf '/' enden, keine Sonderzeichen
function formatDirPath($str){
	$str = formatShortString($str);
	$str = preg_replace('/[\\<>?"\'\|\*]/', '', $str);
	//keine Versteckten Ordner zulassen
	$str = preg_replace('/\/\./','/',$str);
	$str = ltrim($str,".");

	$str = rtrim($str,"/")."/";
	if($str=="/") $str='';

	return $str;
}

function formatSubdirPath($str){
	$str = formatDirPath($str);
	$str = preg_replace('/\.\.\//','',$str);
	return $str;
}

function formatFilename($str){
	$str = formatString($str);
	//< > ? " : | \ / *
	$str = preg_replace('/[\/\\<>?"\'\|\*]/', '', $str);
	//Punkte kürzen
	$str = preg_replace('/\.\(\.\)+/','.',$str);

	//keine Versteckten Dateien zulassen
	$str = ltrim($str,".");
	return $str;
}

function formatBoolean($str){
	if ($str=="1") return 1;//TRUE;
	return 0;//FALSE;
}

function formatEmail($str){
	$str = formatShortString($str);
	$sanitized_str = filter_var($str, FILTER_SANITIZE_EMAIL);
	return	$sanitized_str;
}

function formatUrl($str){
	$str = formatString($str);
	$str = substr($str,0,200);
	$sanitized_str = filter_var($str, FILTER_SANITIZE_EMAIL);
	if (filter_var($sanitized_str, FILTER_VALIDATE_EMAIL)) 
		return 'mailto:'.$sanitized_str;

	return filter_var($str, FILTER_SANITIZE_URL);
}

/*
=========== END String Format Functions =============
 */

/*
=========== Input Validation Functions =============
 */

//true for float/ints > 0
function positiveNumber($input) {
	return (intval($input) > 0);
}

function allIsValid($input) {
	return True;
}

// directory name + "/".
// Note that "/" will be added by the matching format function 'formatSubdirPath'
function validSubdirPath($input) {
	return (strtr($input,array("/"=>"") ) === substr($input,0,-1) );
}

function validIsNonemptyString($input) {
	return ( strlen(strval($input))>0 );
}

function validEmail($input){
	$str = formatString($input);
	//$sanitized_str = filter_var($str, FILTER_SANITIZE_EMAIL);
	if (filter_var($str, FILTER_VALIDATE_EMAIL)) 
		return True;
	return False;
}
/*
=========== END Input Validation Functions ============
 */


/*
=========== General Functions =============
 */

function call_user_func_recursive($input, $funcName){
	if(is_null($funcName)) return $input;
	return (is_array($input) ? array_map($funcName,$input) //array_map("call_user_func_recursive", $input, $funcName)
		: call_user_func($funcName,$input));
}


function sessionUriToken($questionMark){
	if(SID!="")
		return ($questionMark?"&amp;":"?").SID;
	return "";
	//return session_name()."=".session_id();
}

// Extend Url with session variable, if no cookies allowed
// and client wasn't identified as crawler.
$clientIsSearchEngine;

function exUrl($url){
	global $clientIsSearchEngine;
	if(!isset($clientIsSearchEngine))//bei Suchmaschinen keine Sessionid anhängen
		$clientIsSearchEngine = checkIfSearchEngine();
	if($clientIsSearchEngine)
		return $url;

	//$foo = explode("/",ltrim($_SERVER["REQUEST_URI"],"/"));
	$internLinks = $_SERVER["SERVER_NAME"];
	//externe Links
	if( (strpos($url,"://")!==FALSE) && strpos($url,$internLinks)===FALSE) return $url;

	if(strpos($url,"?") !==false)
		return $url.sessionUriToken(true);
	else
		return $url.sessionUriToken(false);
}

function checkIfSearchEngine(){
	//$userAgent =strtolower($_SERVER['HTTP_USER_AGENT']); 

	$crawlers = 'xxfirefox|Google|msnbot|Rambler|Yahoo|AbachoBOT|accoona|' .
		'AcioRobot|ASPSeek|CocoCrawler|Dumbot|FAST-WebCrawler|' .
		'GeonaBot|Gigabot|Lycos|MSRBOT|Scooter|AltaVista|IDBot|eStyle|Scrubby';
	return (preg_match("/$crawlers/i", $_SERVER['HTTP_USER_AGENT']) > 0);
}

function isRelativePath($url){
	if( substr($url,0,4) == "www.") return false;
	if( strpos($url,"://") === FALSE) return true;
	return false;
}

function addUriVar($url,$var,$value){
	if(strpos($url,"?") === false)
		$url .= "?".$var."=".$value;
	else
		$url .= "&".$var."=".$value;
	return $url;
}

function getMail($member,$type)
{
	global $contactData;
	if(!is_array($contactData))
		include_once($subdir.'content/members.php');

	if($type==0)
		$html = '<span class="liam" name="liam" pre="'.$contactData[$member]["mail"][0].'" suf="'.$contactData[$member]["mail"][1].'">'.trim($contactData[$member]["title"].' '.$contactData[$member]["vname"].' '.$contactData[$member]["nname"]).'</span>';
	elseif($type==1)
		$html = '<span class="liam" name="liam"><span>'.$contactData[$member]["mail"][0].'</span>'.$contactData[$member]["mail"][1].'</span>';
	else
		$html = "";

	return ClearMultipleSpace($html);
	//return $html;
}



function hasValue($key,$array){
	//echo "$key: ".$array[$key]."<br>";
	if( array_key_exists($key,$array)){
		if( !is_array($array[$key]) && trim($array[$key])!='') return true;
		elseif( is_array($array[$key]) && count($array[$key])>0) return hasValue(key($array[$key]),$array[$key]);// key() muss nicht unbedingt den ersten Schlüssel liefern.
	}
	return false;
}

function formatFilesize($dsize) {
	if (strlen($dsize) >= 10) {
		$dsize = number_format($dsize / 1073741824,1,",",".");
		return "$dsize GB";
	}elseif (strlen($dsize) >= 7) {
		$dsize = number_format($dsize / 1048576,1,",",".");
		return "$dsize MB";
	} else {
		$dsize = number_format($dsize / 1024,1,",",".");
		return "$dsize KB";
	}
}

/* Returns dateTime object which was set to 
 * the local time of the user. The local time will 
 * be detected by javascript+cookie */
function localDateTime($time="now"){
	$date = new DateTime($time);
	if( isset( $_COOKIE["timezone"] ) ){
		$date->setTimezone(new DateTimeZone($_COOKIE["timezone"]) );
	}
	return $date;	
}


/*
	=========== END General Functions =============
 */

/*
========== Database Functions ========================
 */
function get_db_handle(){
	global $db_dsn;
	global $db_username;
	global $db_password;

	static $db = false;
	if ($db === false) {
		try{
			$db = new PDO($db_dsn, $db_username, $db_password);

			$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

		} catch (PDOException $e) {
			// TODO error handling
			echo('Connection to database failed: ' . $e->getMessage());
			throw $e;
		}
	}
	return $db;
}

function get_game_data($gameId){
	$ret = null;
	try{
		$db = get_db_handle();

		$statement = $db->prepare('SELECT * FROM games WHERE id=? ;');
		if( $statement == null ) throw new Exception("Wrong sql statement");
		$statement->bindValue(1, $gameId,  PDO::PARAM_INT);
		$result = $statement->execute();
		if( $result && $res = $statement->fetch(PDO::FETCH_ASSOC) )
		{
			$ret = $res;
		}
	}catch(Exception $e){
		echo 'get_game_data(id) failed. Exception : '.$e->getMessage();
		$ret = null;
	}
	return $ret;
}

function check_pdo_error($db) {
	if( $db->errorCode() != "00000" ){
		echo "<p>PDO error: ". $db->errorCode() . "</p>";
	}
}

function init_main_database_tables(){
	echo "init_main_database_tables</br>\n";
	//-1. Check if intialisation was already done (just check first table)
	$db = get_db_handle();
	
	// Portable way to detect if table exists
	/*
	$result = $db->query("SELECT 1 FROM gamesPlayerRelation");
	if ($result) {
		echo "MAIN Database was already initialised. Delete db file to force clean recreation.\n</p><p>";
	}*/

	//1. Create tables
	/*
	$db->exec('CREATE TABLE IF NOT EXISTS gamesPlayerRelation (id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
		gameId INTEGER, userId INTEGER,
		userRights INTEGER
	);');
	check_pdo_error($db);
	 */

	//2. Use init functions of classes in $contentTables
	//   for initialisation of some tables.
	global $subdir, $contentTables;
	echo "Init ".count($contentTables) ." content tables.<br>";
	foreach( $contentTables as $list => $contentTable ){
		echo "Init table $list <br>";
			include_once($subdir.$contentTable["classIncl"]);
			$form = new $contentTable["className"]($list,$contentTable);
			if( $form->init_sql_table() === false ){
				print "Error. Creation of table " . $list . " failed.<br>"; 
			}
	}

}

function init_game_database_tables(){
	echo "init_game_database_tables</br>\n";
	global $db_type;

	if( $db_type == 0 ){
		//MySql variant
		$db = get_db_handle();

		//1. Create tables
		$db->exec('CREATE TABLE IF NOT EXISTS statusCache (
			id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
			gameId INTEGER,
			timestamp INTEGER,
			jsonStatus TEXT,
			KEY `gameId` (`gameId`),
		CONSTRAINT `statusCache_ibfk_1` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`) );');
		check_pdo_error($db);
		$db->exec('CREATE TABLE IF NOT EXISTS log (
			id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
			gameId INTEGER,
			timestamp INTEGER,
			playerName TEXT,
			playerId INTEGER,
			message TEXT,
			messageType TEXT,
			KEY `playerId` (`playerId`),
		KEY `gameId` (`gameId`),
		CONSTRAINT `log_ibfk_1` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`));');
		check_pdo_error($db);
	}else{
		// SQLite variant, use own db file for each game
		$db = get_db_handle();
		$db->exec('CREATE TABLE IF NOT EXISTS statusCache (
			id INTEGER PRIMARY KEY NOT NULL,
			gameId INTEGER,
			timestamp INTEGER,
			jsonStatus TEXT);');
		check_pdo_error($db);
		$db->exec('CREATE TABLE IF NOT EXISTS log (
			id INTEGER PRIMARY KEY NOT NULL,
			gameId INTEGER,
			timestamp INTEGER,
			playerName TEXT,
			playerId INTEGER,
			message TEXT,
			messageType TEXT );');
		check_pdo_error($db);
	}


}

function trim_database_tables($gameId){

	$db = get_db_handle();
	//$sql = "DELETE FROM statusCache WHERE id<(SELECT MAX(id) FROM statusCache) - 100 AND gameId == $gameId";
	//$sql = "DELETE FROM log WHERE id<(SELECT MAX(id) FROM log)-2000 AND gameId == $gameId";

	/* Note for SQLite:
	 * Q: I deleted a lot of data but the database file did not get any smaller. Is this a bug?
	 * A: No. When you delete information from an SQLite database, the unused disk space is added
	 * to an internal "free-list" and is reused the next time you insert data. The disk space is not lost.
	 * But neither is it returned to the operating system.
	 * If you delete a lot of data and want to shrink the database file, run the VACUUM command.
	 */

	try{
		$statement = $db->prepare('DELETE FROM statusCache WHERE gameId = ? AND
			id<(SELECT id from statusCache WHERE gameId = ? ORDER BY id DESC LIMIT 1 OFFSET 10); ');
		if( $statement == null ) throw new Exception("Wrong sql statement");
		$statement->bindValue(1, $gameId,  PDO::PARAM_INT);
		$statement->bindValue(2, $gameId,  PDO::PARAM_INT);
		$result = $statement->execute();

		$statement = $db->prepare('DELETE FROM log WHERE gameId = ? AND
			id<(SELECT id from log WHERE gameId = ? ORDER BY id DESC LIMIT 1 OFFSET 2000); ');
		if( $statement == null ) throw new Exception("Wrong sql statement");
		$statement->bindValue(1, $gameId,  PDO::PARAM_INT);
		$statement->bindValue(2, $gameId,  PDO::PARAM_INT);
		$result = $statement->execute();

	}catch(Exception $e){
		echo 'Trim of database failed. Exception : '.$e->getMessage();
	}
	unset($db);

}

function pdo_db_exec($sql){
	try{
		$db = get_db_handle();
		echo $sql;
		$db->exec($sql);
	}catch(Exception $e){
		echo 'Exception : ' . check_pdo_error($db)."<br>".$e->getMessage();
		return false;
	}
	return true;
}




function get_cached_game_status($gameId){
	$db = get_db_handle();
	$ret = null;
	if( $db == null ) return null;

	//init_game_database_tables($gameId);
	try{
		$statement = $db->prepare('SELECT id,timestamp,jsonStatus FROM statusCache WHERE id=(SELECT MAX(id) FROM statusCache WHERE gameId = ? ) AND gameId = ? ;');
		if( $statement == null ) throw new Exception("Wrong sql statement");
		$statement->bindValue(1, $gameId,  PDO::PARAM_INT);
		$statement->bindValue(2, $gameId,  PDO::PARAM_INT);
		$result = $statement->execute();
		if( $result && $res = $statement->fetch(PDO::FETCH_ASSOC) )
		{
			$ret = $res;
		}
	}catch(Exception $e){
		echo 'get_cached_game_status() failed. Exception : '.$e->getMessage();
		$ret = null;
	}

	//Trim big caches and log
	//FIXME: This method is not reliable. Trim could only be operate on a
	//	subset of all game ids.
	if( isset($ret["id"]) &&  $ret["id"] % 101 == 0 ){
		trim_database_tables($gameId);
	}

	return $ret;
}

function set_cached_game_status($gameId, $gameStatus){
	$db = get_db_handle();
	if( $db == null ) return -1;

	$dtobj = new DateTime();
	$curTime = $dtobj->getTimestamp ( );

	global $db_type;
	if( $db_type == 1 ){
		$db->query("PRAGMA synchronous = OFF");
	}
	$statement = $db->prepare('INSERT INTO statusCache (gameId, timestamp, jsonStatus) VALUES (?, ?, ?);');
	$statement->bindValue(1, $gameId, PDO::PARAM_STR);
	$statement->bindValue(2, $curTime, PDO::PARAM_INT);
	$statement->bindValue(3, json_encode($gameStatus), PDO::PARAM_STR);
	$statement->execute();
	check_pdo_error($db);
	return 0;
}

function update_game_log($gameId, $timestamp, $newStatus, $oldStatus){
	if( $newStatus == null || $oldStatus == null ) return;

	$newPlayers = $newStatus->players;
	$oldPlayers = $oldStatus->players;
	usort($newPlayers, 'sortById');
	usort($oldPlayers, 'sortById');

	function comparePlayer($newP, $oldP)
	{
		global $newRound;
		$changes = array();
		if( $newP->name !== $oldP->name ){
			$changes[count($changes)] = array(
				"type" => "name",
				"name" => $oldP->name,
				"id" => $newP->id,
				//"msg" =>	"Changed name to ".$newP->name,
				"msg" =>	"{L_LOG_PLAYER_CHANGE_NAME|".$newP->name."}",
			);
		}
		if( $newP->score != $oldP->score ){
			$changes[count($changes)] = array(
				"type" => "score",
				"name" => $newP->name,
				"id" => $newP->id,
				//"msg" =>	"Score ".($newP>$oldP?"increased":"decreased")." to ".$newP->score,
				"msg" =>	"{L_LOG_PLAYER_SCORE_".($newP>$oldP?"INCREASED":"DECREASED")."|".$newP->score."}",
			);
		}
		if( $newP->statusId != 1 /*a.k.a. player is no AI*/ &&
			( ( $newP->finishedTurn > $oldP->finishedTurn ) ||
			$oldP->finishedTurn == 0 && $newRound && $newP->statusId == 3 )
		){
			$changes[count($changes)] = array(
				"type" => "turn",
				"name" => $newP->name,
				"id" => $newP->id,
				//"msg" =>	"Finished turn",
				"msg" =>	"{L_LOG_PLAYER_FINISHED_TURN}",
			);
		}
		if( $newP->statusId != $oldP->statusId ){
			$msg = null;
			$type = null;
			//	"msg" =>	"Score ".($newP>$oldP?"increased":"decreased")."to ".$newP->score;
			switch( $newP->statusId ){
			case 0:
				$msg = "{L_LOG_ELIMINATED}";
				$type = "eliminated";
				break;
			case 1:
				$msg = "{L_LOG_SWITCHED_TO_AI}";
				$type = "ai";
				break;
			case 2:
				$msg = "{L_LOG_LOGGED_OUT}";
				$type = "login";
				break;
			case 3:
				$msg = ($oldP->statusId == 2?"{L_LOG_LOGGED_IN}":"{L_LOG_CLAIMED_BY_HUMAN}");
				$type = "login";
				break;
			}
			if( $msg != null ){
				$changes[count($changes)] = array(
					"type" => $type,
					"name" => $newP->name,
					"id" => $newP->id,
					"msg" => $msg,
				);
			}
		}

		return $changes;
	};

	global $newRound;
	$newRound = ( $newStatus->gameTurn != $oldStatus->gameTurn );

	/*Check if the name of the game or number of players was changed
	 * This indicates the loading of an other game. Try to omit the
	 * creation of wrong log messages in this case.
	 */
	if( $newStatus->gameName !== $oldStatus->gameName || 
		count($newPlayers) != count($oldPlayers)
	){
		$logMsgs = array ( array (
			array(
				"type" => "game",
				"name" => "",
				"id" => -1,
				//"msg" =>	"New game was loaded.",
				"msg" =>	"{L_LOG_NEW_GAME|". $newStatus->gameDate ."|" . $newStatus->gameTurn . "}",
			)
		) );
	}else{
		$logMsgs = array_map("comparePlayer", $newPlayers, $oldPlayers);

		if( $newRound ){
			if($newStatus->gameTurn > $oldStatus->gameTurn ){
				$newTurn = array (
					array(
						"type" => "turnNew",
						"name" => "",
						"id" => -1,
						//"msg" => "A new turn has begun. It is now ". $newStatus->gameDate . ".",
						"msg" =>	"{L_LOG_NEW_TURN|". $newStatus->gameDate ."|" . $newStatus->gameTurn . "}"
					) );
			}else{
				$newTurn = array (
					array(
						"type" => "turnOld",
						"name" => "",
						"id" => -1,
						//"msg" => "An earlier turn was loaded. It is now ". $newStatus->gameDate . ".",
						"msg" =>	"{L_LOG_OLD_TURN|". $newStatus->gameDate ."|" . $newStatus->gameTurn . "}"
					) );

			}

			$logMsgs[count($logMsgs)] = $newTurn;
		}
	}


	$db = get_db_handle();
	if( $db != null ){
//		$db->query("PRAGMA synchronous = OFF");
		$statement = $db->prepare('INSERT INTO log (gameId, timestamp, playerName, playerId, message, messageType) VALUES (?,?,?,?,?,?);');
		foreach( $logMsgs as $a ){
			foreach( $a as $logMsg ){
				//echo "Send log message";
				$statement->bindValue(1, $gameId, PDO::PARAM_INT);
				$statement->bindValue(2, $timestamp, PDO::PARAM_INT);
				$statement->bindValue(3, $logMsg["name"], PDO::PARAM_STR);
				$statement->bindValue(4, $logMsg["id"], PDO::PARAM_INT);
				$statement->bindValue(5, $logMsg["msg"], PDO::PARAM_STR);
				$statement->bindValue(6, $logMsg["type"], PDO::PARAM_STR);
				$statement->execute();
				check_pdo_error($db);
			}
		}
	}

}
/*
========== END Database Functions ============
 */

/*
========== Login Functions ========================
 */
function check_login_id($userName, $userPassword){

	$userPasswordHash = crypt($userPassword, $userName);

	$db = get_db_handle();
	if( $db == null ) return false;
	//this sql statement do not permit mulitple usage of the same
	//username.
	$sql = "SELECT id,userRights FROM user WHERE userName = ? AND userPasswordHash = ?";
	$statement  = $db->prepare($sql);
	$statement->bindValue(1, $userName, PDO::PARAM_STR);
	$statement->bindValue(2, $userPasswordHash, PDO::PARAM_STR);
	$result = $statement->execute();
	if ($user = $statement->fetch(PDO::FETCH_ASSOC) ){
		$_SESSION["loginName"]=$userName;
		$_SESSION["loginId"]=$user['id'];
		$_SESSION["loginLevel"]=$user['userRights'];
		return $user['id'];
	}

	return null;
}
/*
========== End Login Functions ========================
 */

/*
 * Get access level without init the class for
 * the content form. (Well, this made the other method
 * in dbClass.php redundant...)
 */
function getAccessLevel($tableName, $userId, $userLevel,$operationType){
	global $contentTables;
	//$access = &$this->pref["access"];
	$access = $contentTables[$tableName]["access"];
	switch($operationType){
	case 0:
		if( $userLevel - $access["viewAll"] >= 0 ) return 2;
		if( $userLevel - $access["viewOwn"] >= 0 ) return 1;
		return -1;
		break;
	case 1:
		if( $userLevel - $access["createOwn"] >= 0 ) return 2;
		return -1;
		break;
	case 2:
		if( $userLevel - $access["editAll"] >= 0 ) return 2;
		if( $userLevel - $access["editOwn"] >= 0 ) return 1;
		return -1;
		break;
	case 3:
		if( $userLevel - $access["delAll"] >= 0 ) return 2;
		if( $userLevel - $access["delOwn"] >= 0 ) return 1;
		return -1;
		break;
	default: 
		return -1;
	}
}


?>
