<?php
// set $subdir to ../ if the php file will move to a subdirectory.
//$subdir = "../";
$subdir = "../";

//set the var $htmlHead, if you want add html code between the <head> tags.
include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->

<?php 


include_once($subdir."contentmanager/Downloads.php");

$inputData = array();

?>

<?php

if( array_key_exists("contentList",$_GET)
	&& array_key_exists("loginId",$_SESSION) 
	&& array_key_exists("loginLevel",$_SESSION) 
){
	$list = $_GET["contentList"];
	$userId = $_SESSION["loginId"];
	$userLevel = $_SESSION["loginLevel"];

	//echo $list."<br>";

	//echo isset($contentList);
	$table = $contentTables[$list];
	include_once($subdir.$table["classIncl"]);
	include_once($subdir.$table["phpIncl"]);
	$form = new $table["className"]($list,$table);
	$form->mode="change";

	$change_operation = 2;
	$access = $form->getAccessLevel($userId, $userLevel, $change_operation);

	if( $access > 0 ){
		$bUserWantSendData  = false;
		if(array_key_exists("contentAdd",$_POST)){
			$bUserWantSendData  = true;
			//Collect input of the form in '$inputData' array
			$inputData = $form->post();
			//Valiadate input 
			$bAllInputFieldsOk = $form->isValidInput($inputData);
		}

		if( $bUserWantSendData === true ){
			if( $bAllInputFieldsOk !== true ){
				//Show 'invalid input error message' and the formular.
				echo translate('<h3>{L_ERROR}</h3><p>{L_CM_INVALID_FORMULAR_DATA}</p>');
				$previewHtml = $form->previewContent($inputData);
				echo $previewHtml;

			}elseif( array_key_exists("form".$_POST["formId"],$_SESSION) 
				&& $_SESSION["form".$_POST["formId"]] == 2 )
			{
				/* A formular with this formId was already handled. This ness. to begin
				 * new to omit duplicates.
				 * Show user the 'duplicate error message' and the data
				 */
				$previewHtml = $form->previewContent($inputData);
				echo $previewHtml;

			}
			else{
				$data = $form->getDataset();
				$thtml = $form->update($data,0);
				echo $tpl->insertLaguageToken($thtml,$lang);
			}

		}elseif(array_key_exists("contentSend",$_POST)){
			$inputData = $form->post();
			$previewHtml = $form->previewContent($inputData);
			echo $previewHtml;

		}elseif(array_key_exists("id",$_GET)){
			//$inputData = $form->post();

			//Read and display values from database
			if( $access > 1 ){
				$sql =  'SELECT * FROM '.$form->sqlTable.' WHERE id='.$_GET["id"].' ORDER BY id DESC ';
			}else{
				$sql =  'SELECT * FROM '.$form->sqlTable.' WHERE id='.$_GET["id"].' AND creatorUserId='.$userId.' ORDER BY id DESC ';
			}
			try{
				$db = get_db_handle();

				$result  = $db->query($sql);
				//foreach($result as $res)
				if($row = $result->fetch(PDO::FETCH_ASSOC))
				{
					$dataset = $row;
				}else{
					//No access to dataset
					echo translate("<h3>{L_ERROR}</h3><p>{L_CM_ERROR_ACCESS}</p>");
					return;
				}

			}catch(Exception $e){
				$html .= 'Exception : '.$e->getMessage();
			}
			$inputData = $form->datasetToInput($dataset);

			$thtml = $form->createContentForm(time(), $inputData);
			echo $thtml;
		}else{
			$thtml = $form->listTable(null);
			echo translate($thtml);
		}
	}else{
		echo translate('<h3>{L_ERROR}</h3><p>{L_CM_ERROR_ACCESS}</p>');
	}

}else{
	echo translate('<h3>{L_ERROR}</h3><p>{L_CM_ERROR_GENERAL}</p>');
}



?>

<?php 

include($subdir."php/footer.php");
?>
