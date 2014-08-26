<?php
// set $subdir to ../ if the php file will move to a subdirectory.
//$subdir = "../";
$subdir = "../";

//set the var $htmlHead, if you want add html code between the <head> tags.
include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->

<?php

$userId = isset($_SESSION["loginId"])?$_SESSION["loginId"]:-1;
$userLevel = isset($_SESSION["loginLevel"])?$_SESSION["loginLevel"]:0;
$userName = isset($_SESSION["loginName"])?$_SESSION["loginName"]:"{unknown user}";

if( array_key_exists("contentList",$_GET)
//	&& array_key_exists("loginId",$_SESSION) 
//	&& array_key_exists("loginLevel",$_SESSION) 
){
	$list = $_GET["contentList"];

	$table = $contentTables[$_GET["contentList"]];
	include_once($subdir.$table["classIncl"]);
	include_once($subdir.$table["phpIncl"]);
	$form = new $table["className"]($list,$table);
	$form->mode = "add";

	$add_operation = 1;
	$access = $form->getAccessLevel($userId, $userLevel, $add_operation);

	//echo "Access: $userName, $userId, $userLevel, $access<br>";
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

			}else{
				$data = $form->getDataset();
				$thtml = $form->insert($data,0);
				echo $tpl->insertLaguageToken($thtml,$lang);
			}


		}elseif(array_key_exists("contentSend",$_POST)){
			// Add formular data to database
			$inputData = $form->post();
			$previewHtml = $form->previewContent($inputData);
			echo $previewHtml;

		}else{
			// Begin input collection with a fresh formular
			$inputData = array();
			$thtml = $form->createContentForm(time(), $inputData);
			//echo $tpl->insertLaguageToken($thtml,$lang);
			echo $thtml;
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
