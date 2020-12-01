<?php

function downloadCategoriePreview($cat){
	global $subdir,$fileRoot,$subdirWithWriteAccess,$otherReferer;
	$dHtml = '<p>';
	$dHtml .= '<b>'.$cat["title"].'</b>';
	$dHtml .= '<br>Unterverzeichnis(e): '.$fileRoot."[public|private]/".$subdirWithWriteAccess.$cat["subdirectory"];
	$dHtml .= '<br>Beschreibung: '.$cat["description"];
	$dHtml .= '<br>Erstellungsdatum: '.formatDate($cat["date"]);
	if(isset($otherReferer))
		$dHtml .= '<br>'.call_user_func($otherReferer,$cat)."<br><br>";
	$dHtml .= '</p>';

	return $dHtml;
}


// Listet die Kategorie auf. Falls es kein Unterarray des Namens "files" gibt, werden alle Downloads der Kategorie 
// aus der Datenbank geladen.
/* List all cateories. If no subarray ['files'] exists all files of a categorie will be listet.
 * Otherwise, only ['files'] will be printed out. This array requires the
 * same structure as db results. */
function downloadCategorie($categorie){
	global $subdirWithWriteAccess,$subdir,$fileRoot,$implodeTrenner, $tmpdir; 

	$dHtml = '';

	/*Check if argument already contains a array of file. If not
	 *get list from db. */
	if(!array_key_exists("files",$categorie)){
		$categorie["files"] = array();
		try{
			$db = get_db_handle();
			$statement = $db->prepare('SELECT * FROM downloadFiles WHERE categorieId=? ORDER BY filename;');
			if( $statement == null ) throw new Exception("");
			$statement->bindValue(1, $categorie["id"],  PDO::PARAM_INT);
			$result  = $statement->execute();

			//foreach($result as $key=>$file)
			$key = 0;
			if( $result )
			while($file = $statement->fetch(PDO::FETCH_ASSOC))
			{
				$categorie["files"][$key] = $file;
				$key += 1;
			}
		}catch(Exception $e){
			$html .= 'Exception : '.$e->getMessage();
		}
	}

	//print_r($categorie);

	$dHtml .= '<b>'.$categorie['title'].'</b><p>';
	if( isset($categorie['description']) ) $dHtml .= $categorie['description'].'</p><p>';
	if( count($categorie["files"]) > 0 ){
			$dHtml .= '<ul style="margin-top:0px">';
			foreach($categorie['files'] as $file){
				$savePath = $subdir.$fileRoot;

				//Check if other data influence the path, i.e public, subdirectory
				if( array_key_exists("public",$file) && $file["public"]==true ){
					$public = true;
					$savePath .= 'public/';
				}else{
					$public = false;
					$savePath .= 'private/';
				}
				$savePath .= $subdirWithWriteAccess;

				if( array_key_exists("subdirectory",$categorie) )
					$savePath .= $categorie["subdirectory"];

				$isRel = isRelativePath($file["filename"]);
				//echo "Relative path? $isRel, tmpPath: ".$file["tmpPath"].", File exists?: ".($subdir.$tmpdir.hash("md5",$file["tmpPath"].$file["filename"]))."<br>";
				if($isRel==true){
					if( array_key_exists("tmpPath",$file) && is_file($subdir.$tmpdir.hash("md5",$file["tmpPath"].$file["filename"])))
					{
						$savePath = $subdir.$tmpdir;
						$fullFilename = $savePath.hash("md5",$file["tmpPath"].$file["filename"]); 
					}
					else
						$fullFilename = $savePath.$file["filename"]; 
				}else{
					$fullFilename = $file["filename"];
				}

				$isExtern = ( strpos($fullFilename,"://") !== false );

				//$tmpFilename =  $subdir.$tmpdir.$categorieFile;
				if($public|| (isset($_SESSION["loginName"])&&$_SESSION["loginName"]!='' )  ){
					$dHtml .= '<li><a'.(hasValue("description",$file)?' class="info" infotext="'.$file["description"].'"':'').' href="'.$fullFilename.'">';
					if( $isExtern ){
						$dHtml .= $fullFilename;
						$dHtml .= '</a></li>';
					}else{
						$dHtml .= basename($file["filename"]);
						$dHtml .= " Id(" . (isset($file["id"])?$file["id"]:"-1") . ", " . $file["categorieId"] . ")";
						$dHtml .= '</a>'.($isRel==true?' ('.(($public===true)?'':'{L_INTERN}, ').date("d.m.Y - H:i", filemtime($fullFilename)).', '.formatFilesize(filesize($fullFilename)).')':'').'</li>';
					}	
				}else{
					$dHtml .= '<li>(<a href="'.$subdir.'login.php?from='.$_SERVER['SCRIPT_NAME'].'">{L_LOGIN_REQUIRED}</a>)</li>';
				}

			}
			$dHtml .= '</ul>';
	}else{
		$dHtml .= '</p><p>{L_NO_FILES}';
	}
	$dHtml .= '</p>';

	return translate($dHtml);
}

function downloadList($sql){
	global $implodeTrenner,$fileRoot,$subdirWithWriteAccess;
	$dHtml = '<table class="memberlist">';
	try{
		$db = get_db_handle();

		$statement  = $db->prepare($sql);
		$result = $statement->execute();

		$c = 0;
		if($result)
		while($categorie = $statement->fetch(PDO::FETCH_ASSOC) ){
			$dHtml .= '<tr><td class="hr pad">'.downloadCategorie($categorie).'</td></tr>';
			$c += 1;
		}

		if( $c == 0 ){
			$dHtml .= '<tr><td class="hr pad">—</td></tr>';
		}

	}catch(Exception $e){
		$html .= 'Exception : '.$e->getMessage();
	}

	$dHtml .= '</table>';
	return $dHtml;
}

function downloadListCat($catId){
	if(!is_numeric($catId)) return "Fehlerhafte Eingabeparameter.";
	$sql = 'SELECT * FROM downloadCategories WHERE id='.$catId.';';
	$html = downloadList($sql);
	return $html;
}


function downloadListFull($ab, $maxNbr){
	if(!is_numeric($maxNbr)|| !is_numeric($ab)) return "Fehlerhafte Eingabeparameter.";
	$sql = 'SELECT * FROM downloadCategories ORDER BY title LIMIT '.$ab.', '.$maxNbr.' ';
	$dHtml = downloadList($sql);


	//Find out number of downloads
	$sql = "SELECT COUNT(id) AS count FROM downloadCategories";
	try{
		$db = get_db_handle();

		$result = $db->query($sql);
		if( $result && $row = $result->fetch(PDO::FETCH_ASSOC) ){
			$downloadSize = $row["count"];
		}else{
			$downloadSize = 0;
		}

		$sth = NULL;
	}catch(Exception $e){
		$dHtml .= 'Exception : '.$e->getMessage();
		$downloadSize = 1000;
	}

	return $dHtml;
}

function downloadListShort($listName, $ab,$maxNbr){
	global $contentTables, $implodeTrenner, $fileRoot, $subdirWithWriteAccess, $subdir, $otherReferer;
	$dHtml = '';
	if(!is_numeric($maxNbr)|| !is_numeric($ab)) return "Fehlerhafte Eingabeparameter.";
	$list = $contentTables[$listName];

	$dHtml .= '<ul>';
	
	try{
		$db = get_db_handle();

		$statement = $db->prepare('SELECT * FROM '.$list["sqlTable"].' WHERE showOnStartpage=1 ORDER BY date DESC LIMIT ?, ? ;');
		if( $statement == null ) throw new Exception("");
		$statement->bindValue(1, $ab,  PDO::PARAM_INT);
		$statement->bindValue(2, $maxNbr, PDO::PARAM_INT);
		$result  = $statement->execute();

		if( $result )
		while($download = $statement->fetch(PDO::FETCH_ASSOC)){
			if(isRelativePath($download["filename"])){
				$path = $subdir.$fileRoot.(($download['public']==true)?'public/':'private/').$subdirWithWriteAccess.$download["filename"];
			}else{
				$path = $download["filename"];
			}

			if(isset($otherReferer))
				$dHtml .= call_user_func($otherReferer,$download);
			else
				$dHtml .= '<li><a '.(hasValue("description",$download)?'class="infoLeft" infotext="'.$download["description"].'"':'').' href="'.$path.'">'.basename($download["filename"]).'</a></li>';
		}

	}catch(Exception $e){
		$dHtml .= 'Exception : '.$e->getMessage();
	}
	$dHtml .= '</ul>';


	return $dHtml;
}



function saveFilename($str){//String or array
	return str_replace(array('\\\\',"/"),array("",""),$str);
}


function downloadCategorieSubmit($listName,$data){
	global $fileRoot, $subdirWithWriteAccess, $subdir;

	$html = '';
	$publicPath = $subdir.$fileRoot."public/".$subdirWithWriteAccess.$data["subdirectory"];
	$privatePath = $subdir.$fileRoot."private/".$subdirWithWriteAccess.$data["subdirectory"];
	//echo "$publicPath<br>$privatePath";
	if(!is_dir($publicPath)){
		mkdir($publicPath,0755, true);
		$html .= '<p><i>{L_CM_DOWNLOAD_NEW_DIR_YES|'.$publicPath.'}</i></p>';
	}else{
		$html .= '<p><i>{L_CM_DOWNLOAD_NEW_DIR_EXISTS|'.$publicPath.'}</i></p>';
	}

	if(!is_dir($privatePath)){
		mkdir($privatePath,0750, true);
		$html .= '<p><i>{L_CM_DOWNLOAD_NEW_DIR_YES|'.$privatePath.'}</i></p>';
	}else{
		$html .= '<p><i>{L_CM_DOWNLOAD_NEW_DIR_EXISTS|'.$privatePath.'}</i></p>';
	}

	return $html.defaultSubmit($listName,$data);
}

function downloadFileSubmit($listName,$data){
	global $contentTables, $maxFileSize, $tmpdir, $fileRoot, $subdirWithWriteAccess, $implodeTrenner, $inputData, $subdir;

	//$sql = 'SELECT subdirectory FROM downloadCategories WHERE id='.$data["categorieId"];
	$subdirectory = "";
	try{
		$db = get_db_handle();

		$statement = $db->prepare('SELECT subdirectory FROM downloadCategories WHERE id=? ;');
		if( $statement == null ) throw new Exception("");
		$statement->bindValue(1, $data["categorieId"],  PDO::PARAM_INT);
		$result  = $statement->execute();

		if($row = $statement->fetch(PDO::FETCH_ASSOC)){
			$subdirectory = $row["subdirectory"];
		}
		$db = NULL;
	}catch(Exception $e){
		$html .= 'Exception : '.$e->getMessage();
	}
	$html = '';

	// Transfer uploaded files from tmp dir to disired path if ness.
	// On this stage, the subdirectory variable will be checked if well formed.
	foreach( $contentTables[$listName]["fields"] as $fieldName => $field){
		if($field[0]==7){
			moveFileToFinalPosition($data[$fieldName],$data,$subdirectory);
		}
		if($field[0]==8){
			foreach( $data[$fieldName] as $key=>$filename)
				moveFileToFinalPosition($filename,$data,$subdirectory);
		}
	}

	// Remove empty array enties ("" == false)
	$data["filesExtern"] = array_filter($data["filesExtern"]);
	// Combine both input fields 'files' and 'filesExtern'
	$filenames = array_merge($data["filename"],$data["filesExtern"]);
	$description = $data["description"];

	unset($data["description"]);
	unset($data["filename"]);
	//unset($data["filesExtern"]);

	reset($description);
	//Create array for all files and spread given data on each file
	foreach($filenames as $filename){
		$data["filename"] = $filename;
		if(FALSE === ($data["description"] = current($description))  )
			$data["description"] = "";
		else
			next($description);

		defaultSubmit($listName,$data);
	}

	$html .= 'Die Daten wurden erfolgreich in „'.$listName.'“ gespeichert.<br><br><a href="'.$_SERVER["SCRIPT_NAME"].'?contentList='.$listName.'">Weiteren Eintrag</a> in „'.$listName.'“ erstellen.<br><a href="'.$_SERVER["SCRIPT_NAME"].'">Andere Liste</a> auswählen.';	

	return $html;
}

function moveFileToFinalPosition($filename,$data,$subdirectory){
	global $fileRoot, $subdirWithWriteAccess, $tmpdir, $subdir;

	$savePath = $subdir.$fileRoot;
	$currentPath = $subdir.$tmpdir;
	//Check if other data influence the path, i.e public, subdirectory
	if( array_key_exists("public",$data) && $data["public"]==true )
		$savePath .= 'public/';
	else
		$savePath .= 'private/';

	$savePath .= $subdirWithWriteAccess.$subdirectory;

	/*
	 * Note: We can not use move_uploaded_file (again) because we moved it already to a
	 * file with random name.
	 */
	//exec('mv '.$currentPath.$filename.' '.$savePath.$filename);
	rename($currentPath.$filename, $savePath.$filename, 0644 );

}
?>
