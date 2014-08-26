<?php
/*
Diese Klasse stellt Grundmethoden zum Erstellen, Verändern und Löschen von Einträgen
in Tabellen dar. Diese Grundmethoden müssen bei den abgeleiteten Klassen dann feiner abgestimmt
werden.
 */

include_once($subdir."contentmanager/formularFields.php");

global $tpl; /* this is ness. because dbClass will be included in an function
$tpl isn't in the global scope! */

$langs[] = "contentmanager.php"; 
$tpl->loadLanguage($langs, $lang );

class DbClass{
	protected $pref;
	public $tableTitle;
	public $tableName;
	public $sqlTable;

	protected $paramList, $nbrOfEntries=5, $inputData, $dataset=null;
	protected $formStrings=array();
	public $mode="add";// or change or delete

	function __construct($name, $contentPref){
		$this->pref = $contentPref;
		$this->tableName = &$name; //$this->pref["title"];
		$this->tableTitle = &$this->pref["title"];
		$this->sqlTable = &$this->pref["sqlTable"];

		$this->inputData_fine = false;//currently only used for 'update' and 'delete'

		$this->formStrings = array(
			"add" => array(
				"title" => "{L_CM_ADD_ENTRY|".$this->tableTitle."}",
				"preview" => "{L_PREVIEW}",
				"send" => "{L_CM_ADD}",
			),
			"change" => array(
				"title" => "{L_CM_CHANGE_ENTRY|".$this->tableTitle."}",
				"preview" => "{L_PREVIEW}",
				"send" => "{L_CM_CHANGE}",
			),
			"delete" => array(
				"title" => "{L_CM_DELETE_ENTRY|".$this->tableTitle."}",
				"preview" => "{L_CM_DELETE}",
				"send" => "[should not be displayed]"
			)
		);

		$this->lastInsertId = -1; //save id of last insert command
	}

	/* 
	 * Create a proper table in the database for this
	 * type of class.
	 * ( Optional helper function.)
	 *
	 * Note: Use $this->sqlTable as table name 
	 */
	public function init_sql_table(){
		print "The initialisation of the sql table is 
			not implementet for " . $this->tableName . ".";

		return null;
	}

	/* 
	 * Delete the table in the database for this
	 * type of class.
	 * ( Optional helper function.)
	 *
	 * Note: Use $this->sqlTable as table name 
	 */
	public function drop_sql_table(){
		$ret = true;
		try{
			$db = get_db_handle();
			$statement = $db->prepare('DROP TABLE ' . $this->sqlTable . ';' );
			$result  = $statement->execute();

		}catch(Exception $e){
			$ret = false;
			$html .= 'Exception : '.$e->getMessage();
		}
		return $ret;
	}

	/* Use serverside data to generate unique hash for
	 * a id+tablename combination. If some formulares send
	 * and recive id's of datasets, an attacker could try
	 * to change the affected id to change an other dataset.
	 * A recheck with the cryptId should prevent this.
	 *
	 * Notes: Do not send the cryptId to the client. He can
	 *  eval/estimate the seeds of the hash and matipulate 
	 *  id + cryptId.
	 *  Well, you can attach the cryptId in an environment
	 *  without session support, but this leads to a security
	 *  hole.
	 * 
	 * The function return false if no useable serverside
	 * variables are found. Abort the formular handling in this case. */
	private function genDatasetCryptId($id, $tableName, $formId){
			if( isset($_SESSION) ){
				hash( "md5", $tableName . session_id() . $id . $formId );
			}

			return false;
	}

	private function check_inputData_integrity($inputData){
		$this->inputData_fine = true;

		if( !isset($_SESSION) ) return false;
		if( !array_key_exists("id",$inputData) )  return false;
		if( !array_key_exists("formId",$inputData) )  return false;

		$id = $inputData["id"];
		$formId = $inputData["formId"];
		$cryptId = $_SESSION["cryptId".$formId];

		$this->inputData_fine = $this->inputData_fine && ( $cryptId === $this->genDatasetCryptId($id, $this->tableName, $formId) );
		//echo "CryptId ok:" . $this->inputData_fine . "<br>";
		
		//Check if sended formular data was enriched by variables which has the same name
		//as DummyFields (which was not integrated in the formular)
		//This would be an attack.false
		foreach($this->paramList as $fieldName => $field){
			if(  $field instanceof DummyField 
				&& ( ( isset($_GET) &&  isset($_GET[$field->fieldName] ) )
						|| ( isset($_POST) && isset($_POST[$field->fieldName]) ) ) 
			)
			{
				echo "Problematic param:" . $fieldName . "<br>";
				$this->inputData_fine = false;
			}
		}


		return true;
	}


	function preview(&$inputData){
		return print_r($inputData,true);
	}

	/* Some data should not be influencable
	 * by the user. Use this function to
	 * insert the values for this fields.
	 * Set the 'optional value' of a form
	 * field to -1 to hide it in the formular.
	 *
	 * Override this function in subclasses.
	 */
	function fillInProtected(&$inputData){
	}

	function editingInput(&$inputData){

		foreach($this->paramList as $fieldName => $field){

			if(array_key_exists($field->fieldName,$inputData)){
				$inputData[$field->fieldName] =  $field->format($inputData[$field->fieldName]);
			}else{
				/* Checkboxes without selection are not set in $_GET/$_POST. 
				 * Set checkboxes to 'unselected value'.
				 */
				if( $field instanceof Checkbox ){
					$inputData[$field->fieldName] = $field->format("");
				}
			}
		}
	}

	function formularInfo($infotext,$basetext){
		return new Infofield($infotext,$basetext,"formularInfo");
	}

	/* Default method to display a form for the creation of new enties.
	 * Can be overridden of child classes.
	 */
	function createContentForm($formId, &$inputData){
		global $maxFileSize;

		$bFormWasSend = (array_key_exists("formId",$_POST) && $_POST["formId"] == $formId );
		$bAllInputFieldsOk = true;

		$html = translate('<h3>'.$this->formStr("title").'</h3>');

		$html .= '<form action="'.$_SERVER["PHP_SELF"].'?contentList='.$this->tableName.'" method="post" enctype="multipart/form-data">
			<input type="hidden" name="formId" value="'.$formId.'"></input>
			';
		foreach($this->paramList as $fieldName => $field){
			if( $field->showField() ){
				$tmp = (array_key_exists($field->fieldName,$inputData)?
					$inputData[$field->fieldName]
					:
					$field->getDefaultValue()
				);
				$bValid = $field->isValidInput($tmp);
				$bShowAsInvalid = ( !$bValid && $bFormWasSend );
				$bAllInputFieldsOk = ($bAllInputFieldsOk && $bValid);
				$html .= '<p>'.$field->html($tmp, $bShowAsInvalid ).'</p>';
			}
		}

		$html .= '<p> <input type="hidden" name="MAX_FILE_SIZE" value="'.$maxFileSize.'"><input type="submit" value="'.translate($this->formStr("preview")).'" name="contentSend"></input>';

		$id = -1;
		if(array_key_exists("id",$inputData)){
			$id = $inputData["id"];
		}
		$html .= '<input type="hidden" name="id" value="'.$id.'">';

		//store cryptId in session (or attach to form (insecure))
		$_SESSION["cryptId".$formId] = $this->genDatasetCryptId($id,$this->tableName,$formId);

		//Send button requires at least one preview of the formular.
		//if(array_key_exists("formId",$_POST) && $_POST["formId"] == $formId )
		if( $bFormWasSend && $bAllInputFieldsOk )
		{
			$html .= '<input type="submit" value="'.translate($this->formStr("send")).'" name="contentAdd"></input>';
		}
		$html .= '</p></form>';

		return $html;
	}

	function formStr($field){
		return $this->formStrings[$this->mode][$field];
	}

	function setInputData(&$inputData){
		$this->inputData = $inputData;
	}

	function getDataset(){
		if($this->dataset==null){
			//echo "Convert input array into dataset array<br>";
			$this->dataset = &$this->inputToDataset($this->inputData);
		}
		//print_r($this->dataset);
		return $this->dataset;
	}

	/*
	 * Transform input array (subset of $_GET, $_POST and $_FILES + extra stuff )
	 * into an array which looks like the result of a database request. 
	 * This is useful to show the preview of a new entry with the same function as
	 * database enties.
	 */
	function &inputToDataset(&$inputData){
		global $implodeTrenner;

		$ret = array();

		foreach($this->paramList as $fieldName => $field){
			if( isset($inputData[$field->fieldName]) ){
				if( is_array( $inputData[$field->fieldName]) )
					$ret[$fieldName] = implode($implodeTrenner, $inputData[$field->fieldName]);
				else
					$ret[$fieldName] = $inputData[$field->fieldName];
			}
		}

		return $ret;
	}

	/*
	 * Inverse operation of inputToDataset.
	 */
	function datasetToInput(&$dataset){
		global $implodeTrenner;
		//return $dataset;
		//
		$ret = array();
		foreach($this->paramList as $fieldName => $field){
			if( isset( $dataset[$fieldName] ) ){
				$ret[$field->fieldName] = $dataset[$fieldName];
			}else{
				//echo "Add default value for $fieldName<br>";
				$ret[$field->fieldName] = $field->getDefaultValue();
			}
		}

		// Add always id property
		if( isset( $dataset["id"] ) ){
			$ret["id"] = $dataset["id"];
		}

		return $ret;
	}

	function previewContent(&$inputData){
		global $maxFileSize, $tmpdir, $implodeTrenner, $subdir;

		//include_once($subdir.'contentmanager/contentGenerators.php');

		$html ='';

		if( array_key_exists("form".$inputData["formId"],$_SESSION) 
			&& $_SESSION["form".$inputData["formId"]] == 2 )
		{
			$html .='<h3>{L_WARNING}</h3><p>{L_CM_ALREADY_SEND}</p>';
		}else{
			$_SESSION["form".$inputData["formId"]] = 1;
		}

		// Preview of full entry
		$html .= '<h3>{L_PREVIEW}</h3><div class="formPreview">';
		$html .= $this->preview($inputData);
		$html .= '</div>';

		//Substitute language templates
		global $tpl, $lang;
		$html = $tpl->insertLaguageToken($html,$lang);

		$html .= $this->createContentForm($inputData["formId"], $inputData);
		return $html;
	}

	/*
	 *	$mode = 0, submit for $data 
	 *	$mode > 0, submit for $data[0],$data[1],…
	 */
	function insert(&$dataset,$mode){
		$html = '';
		if( $mode >0){
			foreach($dataset as $d)
				$html .= $this->insert2($d);

			return $html;
		}else
			return $this->insert2($dataset);

	}

	protected function insert2(&$dataset){
		$html = '';

		$columnNames = array();
		$placeholders = array();
		$preparedValues = array();
		foreach( $dataset as $columnName => $value )
		{
			// The dataset could be expanded by 
			// some extra fields, but check the 
			// conditions for the public fields
			// in the param list.
			if( isset($this->paramList[$columnName]) ){
				$field = $this->paramList[$columnName];
				if( !$field->inclSql() ) continue;
			}

			$columnNames[]  = $columnName;
			$preparedValues[] = $value;
			$placeholders[] = '?';
		}
		$sql = "INSERT INTO " . $this->sqlTable . " (" . implode(',', $columnNames) . ") VALUES (" . implode(',', $placeholders) . ");";

		$this->lastInsertId = -1;

		try{
			$db = get_db_handle();
			$statement = $db->prepare($sql);
			$result  = $statement->execute($preparedValues);
			if( $result ){
				//Mark form for this id as processed. (To omit multiple sending of data.)
				$_SESSION["form".$_POST["formId"]] = 2;
				$this->lastInsertId = $db->lastInsertId();

				$html .= '<p>{L_CM_ADD_SUCCESS|'.$this->tableTitle.'}</p>
					<p><a href="'.$_SERVER["SCRIPT_NAME"].'?contentList='.$this->tableName.'">
			{L_CM_ADD_FURTHER_ENTRY|'.$this->tableTitle.'}</a></p>
			<p><a href="index.php">{L_CM_OTHER_LIST}</a></p>';	

			}else{
				$html .= "{L_CM_ERROR_DB}<br>Can not exectue prepared sql statement";
			}

		}catch(Exception $e){
			$html .= "{L_CM_ERROR_DB}<br>Exception message:".$e->getMessage();
		}

		return $html;
	}

	function post(){

		$inputData = $_POST;
		if(is_array($_GET)) $inputData = array_merge($inputData,$_GET);
		if(is_array($_FILES)){
			foreach($_FILES as $fieldName=>$file){
				if(!array_key_exists($fieldName,$inputData))
					$inputData[$fieldName] = array();
				elseif( !is_array($inputData[$fieldName]))
					$inputData[$fieldName] = array(0=>$inputData[$fieldName]);

				//add nonempty fields 
				foreach($file["name"] as $n)
					if(trim($n)!="")
						$inputData[$fieldName][] = $n;

			}
		}

		//Add DummyFields
		$this->fillInProtected($inputData);

		//Apply parsing function on input
		$this->editingInput($inputData);

		//Check if id was not manipulated
		$this->check_inputData_integrity($inputData); 

		//Store inputData array
		$this->setInputData($inputData);


		return $inputData;
	}


	function update(&$dataset,$mode){
		//dataset + id needed
		global $implodeTrenner;
		$html = '';

		//Check if id was not manipulated
		if( $this->inputData_fine !== true )
		{
			return $html."<p>{L_CM_ERROR_PARAMS}</p>";
		}

		$sqlAssigns = array();
		$preparedValues = array();
		foreach( $dataset as $columnName => $value )
		{
			// The dataset could be expanded by 
			// some extra fields, but check the 
			// conditions for the public fields
			// in the param list.
			if( isset($this->paramList[$columnName]) ){
				$field = $this->paramList[$columnName];
				if( !$field->inclSql() ) continue;
			}

			$sqlAssigns[] = $columnName . " = ?";
			$preparedValues[] = $value;
		}
		$sql = "UPDATE " . $this->sqlTable . " SET " . implode(',', $sqlAssigns) . " WHERE id = ?";

		$preparedValues[] = $this->inputData["id"];

		//Check if user has admin rights. Otherwise reduce editable entries
		//on the entries with 'creatorUserId == loginId'.
		$creatorIdRestriction = " AND creatorUserId=-1 ";
		if( array_key_exists("loginId",$_SESSION) && array_key_exists("loginLevel",$_SESSION) )
		{
			$userId = $_SESSION["loginId"];
			$userLevel = $_SESSION["loginLevel"];
			$change_operation = 2;
			$access = $this->getAccessLevel($userId, $userLevel, $change_operation);
			if( $access <= 1){
				$sql .= " AND creatorUserId = ? ";
				$preparedValues[] = $userId;
			}
		}

		try{
			$db = get_db_handle();
			$statement = $db->prepare($sql);
			$result  = $statement->execute($preparedValues);
			echo "Sql command: $sql";
			if( $result ){
				$html .= '<p>{L_CM_CHANGE_SUCCESS|'.$this->tableTitle.'}</p>
					  <p><a href="'.$_SERVER["SCRIPT_NAME"].'?contentList='.$this->tableName.'">
					  {L_CM_CHANGE_FURTHER_ENTRY|'.$this->tableTitle.'}</a></p>
					  <p><a href="index.php">{L_CM_OTHER_LIST}</a></p>';
				$_SESSION["form".$_POST["formId"]] = 2;
			}
		}catch(Exception $e){
			$html .= "{L_CM_ERROR_DB}<br>Exception message:".$e->getMessage();
		}
		return $html;
	}

	function delete(&$dataset,$mode){
		$html = '';

		//Check if id was not manipulated
		if( $this->inputData_fine !== true )
		{
			return $html."<p>{L_CM_ERROR_PARAMS}</p>";
		}

		$sql = 'DELETE FROM '.$this->sqlTable.' WHERE id='.$this->inputData["id"];

		echo $sql;
		if(pdo_db_exec($sql)){
			$html .= '<p>{L_CM_DELETE_SUCCESS|'.$this->tableTitle.'}</p>
				<p><a href="'.$_SERVER["SCRIPT_NAME"].'?contentList='.$this->tableName.'">
		{L_CM_DELETE_FURTHER_ENTRY|'.$this->tableTitle.'}</a></p>
				<p><a href="index.php">{L_CM_OTHER_LIST}</a></p>';	
			$_SESSION["form".$_POST["formId"]] = 2;
		}else{
			$html .= "{L_CM_ERROR_DB}";
		}	
		return $html;
	}

	//+++ for change.php
	function listTable($oR){
		global $contentTables,$subdir;
		$list = $contentTables[$this->tableName];
		include_once($subdir.$list["phpIncl"]);


		$nbrOfEntries = $this->nbrOfEntries;
		if(isset($_GET['page'])){
			$page = $_GET['page'];
		}else
			$page = 1;

		$dHtml = '<h2>'.$this->tableTitle.'</h2>';
		global $otherReferer;
		$listName = $this->tableName;
		global $otherReferer;

		if($oR!=null)
			$otherReferer = $oR;
		else
			$otherReferer = create_function('$listElement','return "<a href=\"change.php?&contentList='.$listName.'&id=".$listElement["id"]."\" static>{L_CM_ENTRY_CHANGE}</a><br><a href=\"delete.php?&contentList='.$listName.'&id=".$listElement["id"]."\" static>{L_CM_ENTRY_DELETE}</a>";');

		$dHtml .= $this->htmlListShort(($page-1)*$nbrOfEntries,$nbrOfEntries, true);
		unset($otherReferer);

		$anzahl = $this->nbrOfEntries;	
		$sql = 'SELECT Count(*) AS nEntries FROM '.$this->sqlTable;
		try{
			$db = get_db_handle();
			$result  = $db->query($sql);
			//foreach($result as $row)
			if($row = $result->fetch(PDO::FETCH_ASSOC))
			{
				$anzahl = $row["nEntries"];
			}

		}catch(Exception $e){
			$html .= 'Exception : '.$e->getMessage();
		}

		$lastPage = ceil($anzahl/$this->nbrOfEntries);

		$navLinks = '';
		$navLinks .= '<span class="nav">';
		if($page>1) $navLinks .= '<span class="info" infotext="{L_FIRST_N_ENTRIES_DESC|'.$nbrOfEntries.'}">
			<a href="'.$_SERVER["SCRIPT_NAME"].'?contentList='.$this->tableName.'&act=change&page='.(1).'">
		{L_FIRST_N_ENTRIES}</a></span>';
		if($page>1) $navLinks .= '<span class="info" infotext="{L_PREV_N_ENTRIES_DESC|'.$nbrOfEntries.'}">
			<a href="'.$_SERVER["SCRIPT_NAME"].'?contentList='.$this->tableName.'&act=change&page='.($page-1).'">
		{L_PREV_N_ENTRIES}</a></span>';
		$navLinks .= " ";
		if($page<$lastPage) $navLinks .= '<span class="info" infotext="{L_NEXT_N_ENTRIES_DESC|'.$nbrOfEntries.'}">
			<a href="'.$_SERVER["SCRIPT_NAME"].'?contentList='.$this->tableName.'&act=change&page='.($page+1).'">
		{L_NEXT_N_ENTRIES}</a></span>';
		if($page<$lastPage) $navLinks .= '<span class="info" infotext="{L_LAST_N_ENTRIES_DESC|'.$nbrOfEntries.'}">
			<a href="'.$_SERVER["SCRIPT_NAME"].'?contentList='.$this->tableName.'&act=change&page='.($lastPage).'">
		{L_LAST_N_ENTRIES}</a></span>';

		$navLinks .= '</span>';

		$dHtml .= $navLinks;

		return $dHtml;
	}

	function isValidInput(&$inputData){
		$bAllInputFieldsOk = true;

		foreach($this->paramList as $fieldName => $field){
			//if( $field->showField() )
			if( true )
			{
				$tmp = (array_key_exists($field->fieldName,$inputData)?
					$inputData[$field->fieldName]
					:
					$field->getDefaultValue()
				);
				$bValid = $field->isValidInput($tmp);
				$bAllInputFieldsOk = ($bAllInputFieldsOk && $bValid);
			}
		}

		return $bAllInputFieldsOk;
	}

	/*
	 * bUseChangeRestriction: Only list entries which can be
	 * changed by the user.
	 */
	function htmlListShort($from,$nbrOfEntries, $bUseChangeRestriction = false ){
		echo "Nicht implementiert.";
	}

	function htmlList($from,$nbrOfEntries){
		echo "Nicht implementiert.";
	}

	function htmlEntryShort($dbEntry){
		echo "Nicht implementiert.";
	}

	function htmlEntry($dbEntry){
		echo "Nicht implementiert.";
	}

	/* Create an "WHERE [id]=..." string to restrict access
	 * This differs for each sql table layout
	 *
	 * Operationtypes:
	 * 	0 - VIEW,
	 * 	1 - INSERT,
	 * 	2 - UPDATE,
	 * 	3 - DELETE
	 *
	 * */
	function getAccessLevel($userId, $userLevel,$operationType){
		//$field = "creatorUserId";
		$access = &$this->pref["access"];
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

}//END dbClass



?>
