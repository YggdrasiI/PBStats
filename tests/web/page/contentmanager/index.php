<?php
// set $subdir to ../ if the php file will move to a subdirectory.
//$subdir = "../";
$subdir = "../";

//Location-Weiche (Auf die Session kann hier noch nicht zugegriffen werden.)
if(array_key_exists("act",$_GET)){
	if($_GET["act"] == "add"){
		header("Location: add.php?".$_SERVER["QUERY_STRING"]);
	}elseif($_GET["act"] == "change"){
		header("Location: change.php?".$_SERVER["QUERY_STRING"]);
	}
}

//set the var $htmlHead, if you want add html code between the <head> tags.
include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->

<?php 

$langs[] = "contentmanager.php"; 
$tpl->loadLanguage($langs, $lang );

function selectContentList(){
	global $contentTables;
	$html = '<h3>{L_CM_SELECT_TABLE_TITLE}</h3>
		<p>{L_CM_SELECT_TABLE_DESC}</p>
		<form action="'.$_SERVER["PHP_SELF"].'" method="GET">
		<select id="contentList" name="contentList" size="'.count($contentTables).'" value="" style="vertical-align:top" >';

	foreach($contentTables as $listName => $list){
		$html .= '<option label="'.$listName.'">'.$listName.'</option>';
	}

	$html .= '</select>';
	$options = array(
		'<option value="add">{L_CM_ADD}</option>',
		'<option value="change">{L_CM_CHANGE}</option>',
	);

	if( isset($_SESSION["loginLevel"]) && $_SESSION["loginLevel"] > 1 ){
		$options[] = '<option value="create">{L_CM_CREATE}</option>';
		$options[] = '<option value="recreate">{L_CM_RECREATE}</option>';
	}
	$html .= '<select name="act" size="'.count($options).'" style="vertical-align:top" >\n';
	foreach( $options as $htmlOpt ){
		$html .= $htmlOpt;
	}
	$html .= '</select>';
	$html .= '<input type="submit" value="{L_CONFIRM}" name="send"></input>';

	$html .= '</form>';

	//return $html;
	global $tpl,$lang;
	return $tpl->insertLaguageToken($html,$lang);
}

function createTableConfirm($tableName, $bRecreate){
	$html = '<h3>{L_WARNING}</h3>';
	if( $bRecreate )
		$html .= '<p>{L_CM_RECREATE_TABLE|'.$tableName.'}</p>';
	else
		$html .= '<p>{L_CM_CREATE_TABLE|'.$tableName.'}</p>';

	$html .= '<form action="'.$_SERVER["PHP_SELF"].'" method="GET">';
	$html .= '<input type="hidden" value="'.$tableName.'" name="contentList"></input>';
	$html .= '<input type="hidden" value="'.($bRecreate?"recreate":"create").'" name="act"></input>';
	$html .= '<input type="hidden" value="yes" name="confirm"></input>';
	$html .= '<input type="submit" value="{L_CONFIRM}" name="send"></input>';

	$html .= '</form>';

	echo translate($html);

}

function createTable($tableName, $bRecreate){
	$html = '';

	if( array_key_exists("loginId",$_SESSION) 
		&& array_key_exists("loginLevel",$_SESSION) 
	){
		$userId = $_SESSION["loginId"];
		$userLevel = $_SESSION["loginLevel"];
		$userName = $_SESSION["loginName"] ;

		if( $userLevel >= CM_ADMIN_ACCESS ){

			global $contentTables, $subdir;
			$table = $contentTables[$tableName];
			include_once($subdir.$table["classIncl"]);
			include_once($subdir.$table["phpIncl"]);
			$form = new $table["className"]($tableName,$table);

			if( $bRecreate ) {
				if ( $form->drop_sql_table() === false ){
					//print "Error. Deletion of table " . $tableName . " failed.<br>"; 
					$html .= "<h3>{L_ERROR}</h3><p>{L_CM_ERROR_DB}<p>";
				}else{
					if( $form->init_sql_table() === false ){
						$html .= "<h3>{L_ERROR}</h3><p>{L_CM_ERROR_TABLE_CREATION}<p>";
					}else{
						$html .= "<h3>{L_NOTE}</h3><p>{L_CM_RECREATE_SUCCESS|".$tableName."}<p>";
					}
				}

			}elseif( $form->init_sql_table() === false ){
				$html .= "<h3>{L_ERROR}</h3><p>{L_CM_ERROR_TABLE_CREATION}<p>";
			}else{
				$html .= "<h3>{L_NOTE}</h3><p>{L_CM_CREATE_SUCCESS}<p>";
			}
		}else{
				$html .= "<h3>{L_ERROR}</h3><p>{L_CM_ERROR_ACCESS}<p>";
		}
	}

	return translate($html);
}

?>

<?php

$act = "listTables";
if(array_key_exists("act",$_GET)){
	if( isset($_SESSION["loginLevel"]) && $_SESSION["loginLevel"] > 1 ){
		if($_GET["act"] == "create"){
			if(array_key_exists("confirm",$_GET)
				&& $_GET["confirm"] === "yes"
			){
				echo createTable($_GET["contentList"], false);
				echo selectContentList();
			}else{
				createTableConfirm($_GET["contentList"], false);
			}

		}elseif($_GET["act"] == "recreate"){
			if(array_key_exists("confirm",$_GET)
				&& $_GET["confirm"] === "yes"
			){
				echo createTable($_GET["contentList"], true);
				echo selectContentList();
			}else{
				createTableConfirm($_GET["contentList"], true);
			}
		}
	}
}else{
	echo selectContentList();
}

?>


<?php 

include($subdir."php/footer.php");
?>
