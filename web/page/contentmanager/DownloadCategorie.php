<?php

include_once($subdir.'contentmanager/dbClass.php');

class DownloadCategorieClass extends DbClass{

	function __construct($name, $contentPref){
		parent::__construct($name,$contentPref);

		$this->downloadTableName = $contentPref["sqlTable2"];

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
				"Titel der Kategorie",
				"formatHtmlString",
				0, 1,
				"validIsNonemptyString"
			),
			"subdirectory" => new InputField(
				"subdirectory",
				$this->formularInfo("Es werden die zwei Verzeichnisse files/public/uploads/[Ihre Angabe]/ und files/private/uploads/[Ihre Angabe]/ erstellt. Einer Kategorie können sowohl öffentliche als auch private Dateien zugeordnet werden.","Unterverzeichnis"),
				"formatSubdirPath",
				0, 1,
				"validSubdirPath",
				""
			),
			"description" => new Textarea(
				"description",
				$this->formularInfo("Die Beschreibung steht vor der Liste der Dateien in dieser Kategorie.","Beschreibung der Kategorie"),
				"formatHtmlString",
				1, 1
			),
			"date" => new HiddenDateField(
				"date",
				"{L_CM_NEWS_DATE_TITLE}",
				"formatInt",
				1, 1
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
				subdirectory TEXT,
				description TEXT,
				date INTEGER
			);');
			$result = $statement->execute();

			$dtobj = new DateTime();
			$curTime = $dtobj->getTimestamp ( );

			// Fill in default category 'general'
			$generalDir = "general/";
			$statement = $db->prepare('INSERT INTO downloadCategories (title,subdirectory,description,date) VALUES (?, ?, ?, ?);');
			$statement->bindValue(1, "General", PDO::PARAM_STR);
			$statement->bindValue(2, $generalDir, PDO::PARAM_STR);
			$statement->bindValue(3, "", PDO::PARAM_STR);
			$statement->bindValue(4, $curTime, PDO::PARAM_INT);
			$statement->execute();
			check_pdo_error($db);


			// Create general-directories
			global $subdir,$fileRoot,$subdirWithWriteAccess;
			$publicPathNew = $subdir.$fileRoot."public/".$subdirWithWriteAccess.$generalDir;
			$privatePathNew = $subdir.$fileRoot."private/".$subdirWithWriteAccess.$generalDir;
			if(!is_dir($publicPathNew)) mkdir($publicPathNew,0755, true);
			if(!is_dir($privatePathNew)) mkdir($privatePathNew,0755, true);

		}catch(Exception $e){
			$ret = false;
			$html .= 'Exception : '.$e->getMessage();
		}

		return $ret;
	}

	function preview(&$inputData){
		global $subdir;

		include_once($subdir."contentmanager/Download.functions.php");

		$dataSet = $this->inputToDataset($inputData);

		$dHtml = '<table class="memberlist"><tr><td class="hr pad">';
		$dHtml .= $this->htmlEntry($inputData);
		$dHtml .= '</td></tr></table>';
		return $dHtml;
	}

	function fillInProtected(&$inputData){
	}

	function post(){
		$inputData = parent::post();
		return $inputData;
	}

	function insert(&$dataset,$mode){
		$html = parent::insert($dataset,$mode);

		/* Create folders. Guarantee that the input was
		 * passed during 'editingInput' to make sure that input was filtered.
		 */
		global $subdir,$fileRoot,$download_folder,$subdirWithWriteAccess;
		//realtive paths
		//$publicPathNew = $subdir.$fileRoot."public/".$subdirWithWriteAccess.$dataset["subdirectory"];
		//$privatePathNew = $subdir.$fileRoot."private/".$subdirWithWriteAccess.$dataset["subdirectory"];
		
		//absolute paths
		$publicPathNew = $download_folder."public/".$subdirWithWriteAccess.$dataset["subdirectory"];
		$privatePathNew = $download_folder."private/".$subdirWithWriteAccess.$dataset["subdirectory"];

		//echo " Create $publicPathNew <br>\n\r";
		//echo " Create $privatePathNew <br>\n\r";
		if(!is_dir($publicPathNew)) mkdir($publicPathNew,0755, true);
		if(!is_dir($privatePathNew)) mkdir($privatePathNew,0755, true);

		return $html;
	}

	function update(&$dataset,$mode){
		global $subdir,$fileRoot,$subdirWithWriteAccess;
		//Auslesen des alten Verzeichnisses
		if(!is_numeric($this->inputData["id"])){
			echo "Fehlerhafter Eingabeparameter: id";
			return;
		}

		$html = '';
		$sql = 'SELECT subdirectory FROM downloadCategories WHERE id='.$this->inputData["id"].' ';
		try{
			$db = get_db_handle();
			$result = $db->query($sql);
			if($row = $result->fetch(PDO::FETCH_ASSOC))
			{
				$oldSubdir = $row["subdirectory"];
			}
		}catch(Exception $e){
			$html .= 'Exception : '.$e->getMessage();
		}

		$html .= parent::update($dataset,$mode);


		//Verschieben der Verzeichnisse
		$publicPathOld = $subdir.$fileRoot."public/".$subdirWithWriteAccess.$oldSubdir;
		$privatePathOld = $subdir.$fileRoot."private/".$subdirWithWriteAccess.$oldSubdir;
		$publicPathNew = $subdir.$fileRoot."public/".$subdirWithWriteAccess.$dataset["subdirectory"];
		$privatePathNew = $subdir.$fileRoot."private/".$subdirWithWriteAccess.$dataset["subdirectory"];

		if( is_dir($publicPathOld) )
		{
			//exec('mv "'.$publicPathOld.'" "'.$publicPathNew.'"');
			rename($publicPathOld,$publicPathNew);
			//echo "<p>Verzeichnis $publicPathOld nach $publicPathNew verschoben.</p>";
		}
		if( is_dir($privatePathOld) ) 
		{
			//exec('mv "'.$privatePathOld.'" "'.$privatePathNew.'"');
			rename($privatePathOld,$privatePathNew);
			//echo "<p>Verzeichnis $privatePathOld nach $privatePathNew verschoben.</p>";
		}

		//Anlegen, falls noch nicht vorhanden
		if(!is_dir($publicPathNew)) mkdir($publicPathNew,0755, true);
		if(!is_dir($privatePathNew)) mkdir($privatePathNew,0755, true);

		return $html;
	}


	function delete(&$dataset,$mode){
		/* Remove all download entries with this category id */
		//$sql = 'DELETE FROM '. $this->downloadTableName .' WHERE categorieId='.$this->inputData["id"];

		$bOk = false;
		try{
			$db = get_db_handle();

			$statement = $db->prepare('DELETE FROM '. $this->downloadTableName .' WHERE categorieId = ? ;');
			$statement->bindValue(1, $this->inputData["id"], PDO::PARAM_INT);
			$statement->execute();

			$bOk = true;
		}catch(Exception $e){
			$html .= 'Exception : '.$e->getMessage();
		}

		if( $bOk ){
			return parent::delete($dataset,$mode);
		}else{
			return "{L_CM_ERROR_DB}";
		}
	}

	function createContentForm($formId, &$inputData){
		$html = '';
		if( $this->mode === "delete" ){
			$html .= '<p class="fontColorWarn" >Deletion of Categorie remove all download entries of this
				categorie, but will not erase files from the filesystem.</p>';
		}
		return $html . parent::createContentForm($formId, $inputData);
	}


	function htmlListShort($from,$nbrOfEntries){
		$html = '';

		$sql = 'SELECT * FROM downloadCategories ORDER BY title LIMIT '.$from.', '.$nbrOfEntries.' ';

		try{
			$db = get_mdb_handle();

			$result = $db->query($sql);
			if( $result )
			while($row = $result->fetch(PDO::FETCH_ASSOC))
			{
				$html .= $this->htmlEntry($row);
			}

		}catch(Exception $e){
			$html .= 'Exception : '.$e->getMessage();
		}


		return $html;
	}

	function htmlList($from,$nbrOfEntries){
		echo "Nicht implementiert.";
	}

	function htmlEntryShort($dbEntry){
		echo "Nicht implementiert.";
	}

	function htmlEntry($dbEntry){
		return downloadCategoriePreview($dbEntry);
	}

}//END dbClass



?>
