<?php

// set $subdir to ../ if the php file will move to a subdirectory.
//$subdir = "../";
$subdir = "";

include_once("php/header_all_pages.php");

$login=0;

if( !isset($_SERVER['PHP_AUTH_USER']) ){
	header('WWW-Authenticate: Basic realm="pbstats authentication."');
	header('HTTP/1.0 401 Unauthorized');
	//echo 'Login was aborted.';
	//$_SESSION("");
	//exit();
}else{
	//echo "<p>Hallo {$_SERVER['PHP_AUTH_USER']}.</p>";
	//echo "<p>Sie gaben {$_SERVER['PHP_AUTH_PW']} als Passwort ein.</p>";
	if ($_SERVER['PHP_AUTH_USER'] !== ""){

		$userName = $_SERVER['PHP_AUTH_USER'];
		$userPassword = $_SERVER['PHP_AUTH_PW'];
		//lookup into database here if password are not managed due .htaccess.
		$userId = check_login_id($userName, $userPassword); 
		if( $userId != null ){
			$login = 1;
			//Note: Guarantee that session was started.
			$_SESSION["loginName"] = $userName;
			$_SESSION["loginId"] = $userId;
			if(array_key_exists("from",$_GET)){
				header("Location: ".$_GET["from"]);
			}else{
				header("Location: index.php");
			}
		}else{	
			header('WWW-Authenticate: Basic realm="pbstats authentication. (FAILED Login to '.$userName.')"');
			header('HTTP/1.0 401 Unauthorized');
		}
	}else{
		header('WWW-Authenticate: Basic realm="pbstats authentication. (Empty User)"');
		header('HTTP/1.0 401 Unauthorized');
	}
}
//delete sensible content
unset($_SERVER['PHP_AUTH_USER']);
unset($_SERVER['PHP_AUTH_PW']);
?>

<?php

//set the var $htmlHead, if you want add html code between the <head> tags.
include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->
<?php
if( $login == 1 ){
	//should never be reached due redirection to index page on successful login.
	echo "Logged in as $userName";
}else{
	echo "Login failed.";
	if( array_key_exists("HTTP_REFERER",$_SERVER) 
		/* && array_key_exists("from",$_GET)*/ )
	{
		echo "<a href='".$_SERVER["SCRIPT_NAME"]."?from=".
			$_SERVER["HTTP_REFERER"]."'>Retry</a>";
	}else{
		echo "<a href='".$_SERVER["SCRIPT_NAME"]."'>Retry</a>";
	}
}
?>

<?php 

include($subdir."php/footer.php");
?>
