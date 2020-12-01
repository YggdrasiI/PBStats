<?php

include_once($subdir.'contentmanager/dbClass.php');

class UserClass extends DbClass{

	function __construct($name, $contentPref){
		parent::__construct($name,$contentPref);

		//$this->defaultPassword = "*****";
		$this->defaultPassword = "";
		$this->bValidUsername = false;

		/* Default Syntax (but constructor arguments can differ):
		 * "[sql column name]" => new [Class of Field](
		 * 		"[form field name]",
		 * 		"[Field Title (or Object)]",
		 * 		"[input format function name]",
		 * 		 bOptional, bSqlField,
		 * 		 ['is valid check' function name],
		 * 		 [defaultValue] 
		 * 		 ),
		 */
		$formFields = array(
			"username" => new InputField(
				"username",
				$this->formularInfo("{L_CM_USERNAME_DESC}","{L_CM_USERNAME}"),
				"formatUsername",
				0, 1,
				"validUsername2"
			),
			"email" => new InputField(
				"email",
				$this->formularInfo("{L_CM_USER_EMAIL_DESC}","{L_CM_USER_EMAIL_TITLE}"),
				"formatEmail",
				0, 1,
				"validEmail"
			),
			"userPassword " => new InputField(
				"userPassword",
				"{L_CM_USER_PASSWORD}",
				"formatShortString",
				0, 0, 
				"validIsNonemptyString",
				$this->defaultPassword 
			),
			"creationTime" => new HiddenDateField(
				"date",
				"{L_CM_USER_DATE}",
				"formatInt",
				0, 1
			), 
			"userPasswordHash" => new DummyField(
				"userPasswordHash",
				"formatIdentity"
			), 
			"humanDetection " => new InputField(
				"humanDetection",
				$this->formularInfo("{L_CM_GAME_HUMAN_DESC}","{L_CM_GAME_HUMAN_TITLE}"),
				"formatShortString",
				0, 0, 
				"isHuman",
				""
			),
			"userRights" => new DummyField(
				"userRights",
				"formatInt",
				null,
				0
			), 
		);

		$this->paramList=$formFields;

	}

	public function init_sql_table(){
		global $db_type;
		$ret = true;
		try{
			$db = get_db_handle();
			$statement = $db->prepare('CREATE TABLE IF NOT EXISTS ' . $this->sqlTable . ' (
				id INTEGER PRIMARY KEY NOT NULL '. ( $db_type==0?'AUTO_INCREMENT':'' ) .',
				userPasswordHash TEXT,
				creationTime INTEGER,
				userRights INTEGER, 
				userName TEXT,
				email TEXT
			);');
			$result = $statement->execute();

			//3. Fill in default users (see php/globalVars.php )

			$dtobj = new DateTime();
			$curTime = $dtobj->getTimestamp ( );

			global $defaultAdmin, $defaultUser, $defaultAdminPassword, $defaultUserPassword, $defaultAdminMail, $defaultUserMail, $adminLevel, $userLevel;
			$adminPasswordHash = crypt($defaultAdminPassword, $defaultAdmin);
			$userPasswordHash = crypt($defaultUserPassword, $defaultUser);

			$statement = $db->prepare('INSERT INTO user (userPasswordHash,userRights,userName,email) VALUES (?, ?, ?, ?);');
			$statement->bindValue(1, $adminPasswordHash, PDO::PARAM_STR);
			$statement->bindValue(2, $adminLevel, PDO::PARAM_INT);
			$statement->bindValue(3, $defaultAdmin, PDO::PARAM_STR);
			$statement->bindValue(4, $defaultAdminMail, PDO::PARAM_STR);
			$statement->execute();
			check_pdo_error($db);

			$statement = $db->prepare('INSERT INTO user (userPasswordHash,userRights,userName,email) VALUES (?, ?, ?, ?);');
			$statement->bindValue(1, $userPasswordHash, PDO::PARAM_STR);
			$statement->bindValue(2, $userLevel, PDO::PARAM_INT);
			$statement->bindValue(3, $defaultUser, PDO::PARAM_STR);
			$statement->bindValue(4, $defaultUserMail, PDO::PARAM_STR);
			$statement->execute();
			check_pdo_error($db);


		}catch(Exception $e){
			$ret = false;
			$html .= 'Exception : '.$e->getMessage();
		}
		return $ret;
	}



	
	function preview(&$inputData){
		global $subdir;

		//include_once($subdir."contentmanager/User.functions.php");
		include_once($subdir."contentmanager/Game.functions.php");

		$dataset = $this->inputToDataset($inputData);

		$dHtml = '<table class="memberlist"><tr><td class="hr pad">';
		$dHtml .= $this->htmlEntry($dataset);
		$dHtml .= '</td></tr></table>';
		//return $dHtml;

		global $tpl,$lang,$langs;

		$tpl->loadStr($dHtml);
		$tpl->loadLanguage($langs, $lang);
		return $tpl->out();

	}

	function isValidInput(&$inputData){
		return (parent::isValidInput($inputData)
		//	&& !$this->validUsername($inputData["username"])
		);
	}

	function fillInProtected(&$inputData){

		if( $inputData["userPassword"] !== $this->defaultPassword ){
			$inputData["userPasswordHash"] = crypt($inputData["userPassword"], $inputData["username"]);
		}else{
			$inputData["userPasswordHash"] = crypt("", $inputData["username"]);
		}

		if( $this->mode === "add" ){
			$inputData["userRights"] = 1; //Default user
		}else{
			//Remove key to prevent update of userRights.
			unset($inputData["userRights"]);
		}

	}

	function post(){
		$inputData = parent::post();

		global $bValidUsername;
		$bValidUsername = $this->validUsername($inputData["username"]);
		if( !$bValidUsername )
		{
			echo translate("<h3>{L_WARNING}</h3><p>{L_CM_USERNAME_ALREADY_USED}</p>");
		}
		$bHuman = isHuman($inputData["humanDetection"]);
		if( !$bHuman )
		{
			echo translate("<h3>{L_WARNING}</h3><p>{L_CM_GAME_NOTE_HUMAN}</p>");
		}
		return $inputData;
	}


	function insert(&$dataset,$mode){

		$dHtml = parent::insert($dataset,$mode);

		//Postprocessing: I.e. send registration email
		//Well, I'm no friend of such mails...
		

		return $dHtml;
	}

	function htmlListShort($from,$nbrOfEntries, $bUseChangeRestriction = false ){
		return "";
	}

	function htmlList($from,$nbrOfEntries){
		echo "Nicht implementiert.";
	}

	function htmlEntryShort($dbEntry){
		echo "Nicht implementiert.";
	}

	function htmlEntry($dbEntry){
		global $otherReferer, $subdir;
		$dHtml = '<h2 style="display:inline">{L_MENU_REGISTRATION}</h2><p>';

		if(hasValue('username',$dbEntry)){
			$dHtml .= "{L_CM_USERNAME}: ". $dbEntry['username'] . "</p><p>";
		}else{
			$dHtml .= "{L_CM_USERNAME}: {L_INVALID}</p><p>";
		}
		if(hasValue('email',$dbEntry)){
			$dHtml .= "{L_CM_USER_EMAIL_TITLE}: ". $dbEntry['email'] . "</p><p>";
		}else{
			$dHtml .= "{L_CM_USER_EMAIL_TITLE}: {L_INVALID}</p><p>";
		}

		return $dHtml;
	}

	function validUsername($username){
		if( strlen($username) < 3 || strlen($username)>20 ){
			return false;
		}
		try{
			$db = get_db_handle();
			$statement = $db->prepare('SELECT id FROM ' . $this->sqlTable . ' WHERE username=? ;' );
			if( $statement == null ) throw new Exception("Can not prepare statement");
			$statement->bindValue(1, $username,  PDO::PARAM_STR);
			$result  = $statement->execute();
			if( $result && ($user = $statement->fetch(PDO::FETCH_ASSOC)) )
			{
				return false;
			}
		}catch(Exception $e){
			echo 'Exception : '.$e->getMessage();
			return false;
		}

		return true;
	}

}//END dbClass


// Check answer of simple human detection question.
function isHuman($humanDetection){
	$str = trim(strtolower($humanDetection));
	$bHuman = ( $str == "sid" || $str == "sid meier" || $str == "meier" );
	return $bHuman;
}

//check if username is already in usage.
//Just lookup global value, which was set by validUsername
function validUsername2($username){
	global $bValidUsername;
	return $bValidUsername;
}

//Remove space, special chars, etc.
function formatUsername($username){
	//$username = preg_filter(array('/[^a-zA-Z0-9_-]/'),array(''),$username);
	$username = preg_replace(array('/[^a-zA-Z0-9_-]/'),array(''),$username);
	return $username;
}

?>
