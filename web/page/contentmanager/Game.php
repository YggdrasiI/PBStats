<?php

include_once($subdir.'contentmanager/dbClass.php');

class GameClass extends DbClass{

	function __construct($name, $contentPref){
		parent::__construct($name,$contentPref);

		$this->defaultPassword = "*****";

		$author = '';
		$authorId = -1;
		if( isset($_SESSION["loginName"]) ){
			$author = $_SESSION["loginName"];
			$authorId = $_SESSION["loginId"];
		}

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
			"name" => new InputField(
				"gameName",
				"{L_CM_GAME_NAME}",
				"formatShortString",
				0, 1,
				"validIsNonemptyString"
			),
			"url" => new InputField(
				"gameUrl",
				"{L_CM_GAME_URL}",
				"formatUrl",
				0, 1,
				"validIsNonemptyString"
			),
			"port" => new NmbrInputField(
				"gamePort",
				$this->formularInfo("{L_CM_GAME_PORT_DESC}","{L_CM_GAME_PORT_TITLE}"),
				"formatInt",
				0, 1, 
				"positiveNumber",
				13373
			), 
			"urlUpdate" => new Checkbox(
				"urlUpdate",
				$this->formularInfo("{L_CM_GAME_URL_UPDATE_DESC}","{L_CM_GAME_URL_UPDATE_TITLE}"),
				"formatBoolean",
				0, 1,
				null,
				1
			),
			"managePassword " => new InputField(
				"managePassword",
				$this->formularInfo("{L_CM_GAME_MANAGE_PASSWORD_DESC}","{L_CM_GAME_MANAGE_PASSWORD_TITLE}"),
				"formatShortString",
				1, 0, 
				null,
				$this->defaultPassword 
			),
			"description" => new Textarea(
				"gameDescription",
				"{L_CM_GAME_DESCRIPTION}","formatHtmlStringTextarea",
				1, 1
			),
			"infolink" => new InputField(
				"infolink",
				"{L_CM_GAME_INFOLINK}","formatUrl",
				1, 1
			),
			"creationTime" => new HiddenDateField(
				"date",
				"{L_CM_GAME_DATE}",
				"formatInt",
				0, 1
			), 
			"creatorUserId" => new DummyField(
				"creatorId",
				"formatInt",
				null,
				$authorId 
			), 
			"managePasswordHash" => new DummyField(
				"managePasswordHash",
				"formatIdentity"
			), 
			"status" => new DummyField(
				"status",
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
				managePasswordHash TEXT, creationTime INTEGER,
				creatorUserId INTEGER,
				name TEXT, url TEXT, port INTEGER,
				urlUpdate INTEGER,
				description TEXT,
				infolink TEXT,
				status INTEGER,
				date INTEGER,
				sqlPrefix TEXT,
				privateNotes TEXT
			);');
			$result = $statement->execute();

		}catch(Exception $e){
			$ret = false;
			$html .= 'Exception : '.$e->getMessage();
		}

		return $ret;
	}

	function preview(&$inputData){
		global $subdir;

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

	function fillInProtected(&$inputData){
		$authorId = -1;
		if( isset($_SESSION["loginId"]) ){
			$authorId = $_SESSION["loginId"];
		}

		if( $inputData["managePassword"] !== $this->defaultPassword ){
			$inputData["managePasswordHash"] = hashGamePassword( $inputData["managePassword"] );
		}else{
			$inputData["managePasswordHash"] = hashGamePassword( "" );
			//unset Key to prevent change of stored password during update
			if( $this->mode === "change" ){
				unset($inputData["managePasswordHash"]);
			}
		}

		//Note: loginId of change operation
		// can differ from loginId due creation.
		// Thus, remove field to conserve the given
		// value in the database.
		if( $this->mode === "add" ){
			$inputData["creatorId"] = $authorId;
			$inputData["status"] = 0;//game offline

			/* currently exact copy!!
			 *( Todo: Check hash on pitboss side and switch
			 * here to hash storage */
		}else{
			unset($inputData["creatorId"]);
			unset($inputData["status"]);
		}
	}

	function post(){
		$inputData = parent::post();
		return $inputData;
	}


	function insert(&$dataset,$mode){

		$dHtml = parent::insert($dataset,$mode);

		return $dHtml;
	}

	function htmlListShort($from,$nbrOfEntries, $bUseChangeRestriction = false ){
		return gamesListShort($this->tableName,$from,$nbrOfEntries, $bUseChangeRestriction );
	}

	function htmlList($from,$nbrOfEntries){
		echo "Nicht implementiert.";
	}

	function htmlEntryShort($dbEntry){
		echo "Nicht implementiert.";
	}

	function htmlEntry($dbEntry){
		return gamePreview($dbEntry);
	}


}//END dbClass



?>
