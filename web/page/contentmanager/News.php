<?php

include_once($subdir.'contentmanager/dbClass.php');

class NewsClass extends DbClass{

	function __construct($name, $contentPref){
		parent::__construct($name,$contentPref);

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
			"title" => new InputField(
				"title",
				"{L_CM_NEWS_TITLE_TITLE}",
				"formatHtmlString",
				//"formatShortString",
				0, 1,
				"validIsNonemptyString"
			),
			"short" => new InputField(
				"short",
				$this->formularInfo("{L_CM_NEWS_SHORT_DESC}","{L_CM_NEWS_SHORT_TITLE}"),
				"formatHtmlString",
				1, 1
			),
			"content" => new Textarea(
				"content",
				"{L_CM_NEWS_CONTENT_TITLE}",
				"formatHtmlStringTextarea",
				0, 1,
				"validIsNonemptyString"
			),
			"infolink" => new InputField(
				"infolink",
				$this->formularInfo("{L_CM_NEWS_INFOLINK_DESC}","{L_CM_NEWS_INFOLINK_TITLE}"),
				"formatUrl",
				1, 1
			),
			"author" => new InputField(
				"author",
				$this->formularInfo("{L_CM_NEWS_AUTHOR_DESC}","{L_CM_NEWS_AUTHOR_TITLE}"),
				"formatShortString",
				1, 1, 
				null,
				$author
			),
			"date" => new HiddenDateField(
				"date",
				"{L_CM_NEWS_DATE_TITLE}",
				"formatInt",
				0, 1
			), 
			"creatorUserId" => new DummyField(
				"creatorId",
				"formatInt",
				null,
				$authorId
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
				title TEXT,
				short TEXT,
				content TEXT,
				infolink TEXT,
				author TEXT,
				creatorUserId INTEGER,
				date INTEGER
			);');
			$result = $statement->execute();

		}catch(Exception $e){
			$ret = false;
			echo 'Exception : '.$e->getMessage() ."<br>\n\r";
		}

		return $ret;
	}


	function preview(&$inputData){
		global $subdir;

		include_once($subdir."contentmanager/News.functions.php");

		$dataSet = $this->inputToDataset($inputData);

		$dHtml = '<table class="memberlist"><tr><td class="hr pad">';
		$dHtml .= $this->htmlEntry($inputData);
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
		if( $this->mode === "add" ){
			$inputData["creatorId"] = $authorId;
		}else{
			//Note: loginId of change operation
			// can differ from loginId due creation.
			// Thus, remove field to conserve the given
			// value in the database.
			unset($inputData["creatorId"]);
		}
	}

	function post(){
		$inputData = parent::post();
		return $inputData;
	}


	function htmlListShort($from, $nbrOfEntries, $bUseChangeRestriction = false){
		return newsListShort($this->tableName, $from, $nbrOfEntries);
	}

	function htmlList($from,$nbrOfEntries){
		echo "Nicht implementiert.";
	}

	function htmlEntryShort($dbEntry){
		echo "Nicht implementiert.";
	}

	function htmlEntry($dbEntry){
		return newsPreview($dbEntry);
	}


}//END dbClass



?>
