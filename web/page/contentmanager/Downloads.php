<?php

include_once($subdir."contentmanager/dbClass.php");

class DownloadClass extends DbClass{

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
			"categorieId" => new OptionField(
				"categorieId",
				$this->formularInfo("{L_CM_DOWNLOAD_CATEGORY_DESC}","{L_CM_DOWNLOAD_CATEGORY_TITLE}"),
				null,// No formating
				0, 
				"SELECT id, title FROM downloadCategories ORDER BY title",
				"1"),
			"public" => new Checkbox(
				"public",
				$this->formularInfo("{L_CM_DOWNLOAD_PUBLIC_DESC}","{L_CM_DOWNLOAD_PUBLIC_TITLE}"),
				"formatBoolean",
				0, 1
			),
			"showOnStartpage" => new Checkbox(
				"showOnStartpage",
				$this->formularInfo("{L_CM_DOWNLOAD_SHOW_ON_STARTPAGE_DECS}","{L_CM_DOWNLOAD_SHOW_ON_STARTPAGE_TITLE}"),
				"formatBoolean",
				0, 1
			),
			"filename" => new MultipleUploadField(
			 	"filename",
				$this->formularInfo("Die Dateigröße ist durch die Servereinstellungen auf ".ini_get('upload_max_filesize')." begrenzt. Größere Dateien müssen per ssh übertragen und werden. Weitere Informationen beim Feld „Externe Dateien”...", "Datei(en), " ),
				"formatFilename",
				1, 1
			),
			"filesExtern" => new MultipleInputField(
				"filesExtern",
				$this->formularInfo("Hier können Links auf externe Dateien, (http://..) und Pfade zu Dateien, die manuell per ssh übertragen wurden, angegeben werden. Falls im zweiten Fall die Datei unter public_html/files/private/[Dateiname] zu finden ist, muss [Dateiname] in das Feld eingetragen werden und sich kein Häckchen bei „Datei(en) öffentlich“ befinden.", "Externe Datei(en)" ),
				"formatString",
				1, 0
			),
			"description" => new MultipleInputField(
				"description",
				$this->formularInfo("Die Anzahl der Felder sollte mit der Anzahl der oben angegeben Dateien übereinstimmen. Die Informatioen dieses Feldes sind für alle Besucher einsehbar.","Beschreibung der Datei(en)"),
				"formatHtmlString",
				1, 1
			),
			"creatorUserId" => new DummyField(
				"creatorId",
				"formatInt",
				null,
				$authorId /*redundant*/
			), 
			"date" => new HiddenDateField(
				"date",
				"{L_CM_NEWS_DATE_TITLE}",
				"formatInt",
				0, 1
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
				categorieId INTEGER,
				showOnStartpage INTEGER,
				public INTEGER,
				filename TEXT,
				filesExtern TEXT,
				description TEXT,
				creatorUserId  INTEGER,
				date INTEGER
			);');
			$result  = $statement->execute();

		}catch(Exception $e){
			$ret = false;
			$html .= 'Exception : '.$e->getMessage();
		}

		return $ret;
	}

	/*
	 * Transform input array (subset of $_GET, $_POST and $_FILES + extra stuff )
	 * into an array which looks like the result of a database request. 
	 * This is useful to show the preview of a new entry with the same function as
	 * database enties.
	 */
	function &inputToDataset(&$inputData){

		if( is_array( $inputData["filesExtern"] ) ){
			// Combine both input fields 'files' and 'filesExtern'
			$filenames = array_merge($inputData["filename"],$inputData["filesExtern"]);
		}else{
			$filenames = $inputData["filename"];
		}

		$filenames = array_filter($filenames,"strlen");
		$description = $inputData["description"];


		$dataset = parent::inputToDataset($inputData);

		//Remove some unwanted keys
		unset($dataset["description"]);
		unset($dataset["filename"]);
		unset($dataset["filesExtern"]);

		/* Finally, duplicate dataset for each filename
		 * and return array of datasets */
		reset($description);
		if(is_array($filenames)){
			$ret = array();
			foreach( $filenames as $key=>$fname){
				$ret[$fname] = $dataset;
				$ret[$fname]["filename"] = $fname;
				if(FALSE === ($ret[$fname]["description"] = current($description))  )
					$ret[$fname]["description"] = "";
				else
					next($description);
			}

			print_r($ret);
			return $ret;
		}else{
			echo "ERROR. SHOULD NOT BE REACHABLE...";
		}

		//$dataset["filename"] = $filenames;
		//$dataset["description"] = $description;

		return $dataset;

	}

	/*
	 * Inverse operation of inputToDataset.
	 */
	function datasetToInput(&$dataset){
		$ret = parent::datasetToInput($dataset);

		//Extra setup...
		
		return $ret;
	}

	function preview(&$inputData){
		global $subdir;

		include_once($subdir."contentmanager/Download.functions.php");
		
		$dataset = $this->inputToDataset($inputData);

		/* Note: We transform the preview of a 'downloadable file' into
		 * a preview of a 'download categorie', but shrink the number of
		 * files in this categorie no the list of new files */

		//saveUploadedFile($dataset, $this->paramList["filename"].fieldName, $this->paramList["filename"].formatFunction);

		// Load information about the categorie.
		$categorie = "Unknown categorie";
		$sql = 'SELECT * FROM downloadCategories WHERE id='.$inputData["categorieId"];

		try{
			$db = get_db_handle();

			$result  = $db->query($sql);
			//foreach($result as $row)
			if($row = $result->fetch(PDO::FETCH_ASSOC))
			{
				$categorie = $row;
			}

		}catch(Exception $e){
			$html .= 'Exception : '.$e->getMessage();
		}
		
		if( !is_array( $dataset ) ){
			echo "Error. Dataset has to be array with filename as keys";
			//$dataset = array( 0=>$dataset );
		}
		$categorie["files"] = array();

		$key = 0;
		foreach($dataset as $filename=>$ds){
			$categorie["files"][$key] = $ds;
			$categorie["files"][$key]["filename"] = $filename;
			$categorie["files"][$key]["tmpPath"] = $inputData["formId"];
			$key += 1;
		}

		$dHtml = '<table class="memberlist"><tr><td class="hr pad">';
		$dHtml .= downloadCategorie($categorie);
		$dHtml .= '</td></tr></table>';
		return $dHtml;
	}

	// First argument structure differs between this function and the ..ToDest(...) functions. 
	function moveFileToTmp(&$inputData, $fieldName, $formatFunction, $salt){
		global $maxFileSize, $tmpdir, $subdir;
		//$fieldName = "filename";

		if(is_array($_FILES[$fieldName]['name'])) return $this->moveFilesToTmp($inputData, $fieldName, $formatFunction, $salt);

		if($_FILES[$fieldName]['size']>$maxFileSize){
			echo "The uploaded File was too big.";
			return false;
		}

		$filename = call_user_func_recursive($_FILES[$fieldName]['name'],$formatFunction);
		$targetPath = $subdir.$tmpdir.hash("md5",$salt.$filename);

		if(move_uploaded_file($_FILES[$fieldName]['tmp_name'],$targetPath)){
			//print "File is valid, and was successfully uploaded.";
			$inputData[$fieldName] = $filename; 
			return true;
		}else{
			//print "Possible file upload attack.";
			return false;
		}
	}

	function moveFileToDest(&$dataset, $fieldName, $formatFunction, $salt){
		global $maxFileSize, $tmpdir, $subdir;
		//$fieldName = "filename";

		//if( ! array_key_exists("categorieId",$dataset)) //array of datasets (each for every file)
		if(true)
		{
			return $this->moveFilesToDest($dataset, $fieldName, $formatFunction, $salt);
		}

		if(is_array($_FILES[$fieldName]['name'])) return $this->moveFilesToDest($dataset, $fieldName, $formatFunction, $salt);

		$filename = call_user_func_recursive($_FILES[$fieldName]['name'],$formatFunction);
		$sourcePath = $subdir.$tmpdir.hash("md5",$salt.$filename);
		$destPath = $subdir.$tmpdir.$filename;

		/*
		 * Note: We can not use move_uploaded_file (again) because we moved it already to a
		 * file with random name.
		 */
		//if( system("mv '$sourcePath' '$destPath'") !==FALSE )
		if( rename($sourcePath, $destPath, 0644 ) !== false )
		{
			echo "File is valid, and was successfully uploaded.";
			//chmod($destPath, 0644);
			return true;
		}else{
			//print "Possible file upload attack.";
			echo "Fehler beim Ausführen von \"mv $sourcePath $destPath\"";
			return false;
		}
	}

	/* Notes:
	 *  • First argument is array of inputData
	 *  • First argument here is 'inputData', but 'dataset'
	 *	  for the ..ToDest(...) functions
	 */
	function moveFilesToTmp(&$inputData, $fieldName, $formatFunction, $salt){
		global $maxFileSize, $tmpdir, $subdir;
		$ret = true;

		$filenames = call_user_func_recursive($_FILES[$fieldName]['name'],$formatFunction);
		foreach($_FILES[$fieldName]['name'] as $key=>$name){

			if($_FILES[$fieldName]['size'][$key]>$maxFileSize){
				echo "{L_CM_DOWNLOAD_TOO_BIG|".$_FILES[$fieldName]["name"][$key]."}.";
				$ret = false;
			}

			//	$targetPath = "/[path]/".$subdir.$tmpdir.hash("md5",$salt.$filenames[$key]);
			$targetPath = $subdir.$tmpdir.hash("md5",$salt.$filenames[$key]);
			//echo $_FILES[$fieldName]['tmp_name'][$key]."<br>". $targetPath. " subdir was ".$subdir;

			if(move_uploaded_file($_FILES[$fieldName]['tmp_name'][$key],$targetPath)){
				//echo "File ".$_FILES[$fieldName]["name"][$key]." was uploaded successful.";
				//$inputData[$fieldName][$key] = $filenames[$key]; 
				//$inputData[$name][$fieldName] = $filenames[$key]; //TODO??
			}else{
				//echo "Error during upload of ".$_FILES[$fieldName]["name"][$key]." .";
				//print "Possible file upload attack.";
				$ret =  false;
			}
		}

		return $ret;
	}

	/* Notes:
	 *  • First argument is array of datasets
	 *  • First argument here is 'dataset', but 'inputData'
	 *	  for the ..ToTmp(...) functions
	 */
	function moveFilesToDest(&$dataset, $fieldName, $formatFunction, $salt){
		global $maxFileSize, $tmpdir, $subdir, $fileRoot, $subdirWithWriteAccess;
		$ret = true;

		// Find out subdirectory of this category.
		//reset($inputData);
		$bar = current($dataset);
		$catId = intval( $bar["categorieId"]);
		$sql = 'SELECT subdirectory FROM downloadCategories WHERE id='.$catId;
		$subdirectory = "";
		try{
			$db = get_db_handle();
			$result  = $db->query($sql);
			if($row = $result->fetch(PDO::FETCH_ASSOC))
			{
				$subdirectory = $row["subdirectory"];
			}

		}catch(Exception $e){
			$html .= 'Exception : '.$e->getMessage();
		}

		//$filenames = call_user_func_recursive($_FILES[$fieldName]['name'],$formatFunction);
		//foreach($_FILES[$fieldName]['name'] as $key=>$name)
		foreach($dataset as $filename2=>$ds) /* filename2 is redundant */
		{
			$filename = call_user_func_recursive($ds["filename"],$formatFunction);
			$savePath = $subdir.$fileRoot;
			$currentPath = $subdir.$tmpdir;

			//Check if other data influence the path, i.e public, subdirectory
			if( array_key_exists("public",$ds) && $ds["public"]==true )
				$savePath .= 'public/';
			else
				$savePath .= 'private/';
			$savePath .= $subdirWithWriteAccess.$subdirectory;

			$sourcePath = $subdir.$tmpdir.hash("md5",$salt.$filename);
			$destPath = $savePath.$filename;
			//echo $_FILES[$fieldName]['tmp_name'][$key]."<br>". $targetPath;
			echo "mv '$sourcePath' '$destPath'<br>";
			//					chmod($sourcePath, 0666);
			//if( system("mv '$sourcePath' '$destPath'")!==FALSE)
			if( rename($sourcePath, $destPath ) !== false )
			{
				//echo "File is valid, and was successfully uploaded.";
				//chmod($destPath, 0644);
				//$inputData[$fieldName][$key] = $filenames[$key]; 
				//$inputData[$fieldName2][$fieldName] = $filename; 
				$ds["filename"] = $filename; 
			}else{
				//echo "Beim Hochladen von ".$_FILES[$fieldName]["name"][$key]." ist ein Fehler aufgetreten.";
				//print "Possible file upload attack.";
				$ret =  false;
			}
		}

		return $ret;
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

		/* The move call has to be capsuled.
		 * Post method will be called for the first display of
		 * entries, too. Thus, in this case no $_POST variable exists */
		if( isset($_POST["formId"]) ){
			$this->moveFileToTmp($inputData, $this->paramList["filename"]->fieldName, $this->paramList["filename"]->formatFunction,$_POST["formId"]);
		}

		return $inputData;
	}


	function insert(&$dataset,$mode){

		// Move files from tmp dir to target
		$this->moveFileToDest($dataset, $this->paramList["filename"]->fieldName, $this->paramList["filename"]->formatFunction,$_POST["formId"]);


		if( array_key_exists("categorieId",$dataset)){
			//one file
			return parent::insert($dataset,0);
		}else{
			//multiple files
			return parent::insert($dataset,1);
		}
	}

	function listTable($oR){
		$listName = $this->tableName;
		$oR = create_function('$listElement','return "<li>".basename($listElement["filename"])." <a href=\"delete.php?&contentList='.$listName.'&id=".$listElement["id"]."\" static>Datei löschen</a></li>";');
		return	parent::listTable($oR);
	}

	function htmlListShort($from, $nbrOfEntries, $bUseChangeRestriction = false){
		return downloadListShort($this->tableName, $from, $nbrOfEntries);
	}

	function htmlList($from,$nbrOfEntries){
		echo "Nicht implementiert.";
	}

	function htmlEntryShort($dbEntry){
		echo "Nicht implementiert.";
	}

	function htmlEntry($dbEntry){
		return downloadCategorie($dbEntry);
	}

}//END dbClass



?>
