<?php

function newsPreview($news){
	if(!array_key_exists("id",$news))$news["id"] = "-1";
	return newsFull($news);
}

function newsShort($news){
	global $otherReferer, $subdir;
	$dHtml = '<h4>'.$news['title'].'</h4><p>';
	if(hasValue('short',$news)) $dHtml .= $news['short'].'<br>';
	$dHtml .= (isset($otherReferer)?call_user_func($otherReferer,$news):'<a href="'.$subdir.'news.php?news='.$news['id'].'">{L_MORE}</a>');
	$dHtml .= '</p>';

	return translate($dHtml);
}

function newsFull($news){
	global $otherReferer, $subdir;
	$dHtml = '<h2 style="display:inline"><a href="'.(isset($otherReferer)?call_user_func($otherReferer,$news):$subdir.'news.php?news='.$news["id"]).'">'.$news['title'].'</a></h2>'.(hasValue('date',$news)?' ('.formatDate($news['date']).')':'').'<p>';
	if(hasValue('content',$news)) $dHtml .= $news['content'];
	if(hasValue('author',$news)) $dHtml .= ' (<i>'.$news['author'].'</i>)';
	if(hasValue('infolink',$news)) $dHtml .= '</p><p><a href="'.(isRelativePath($news['infolink'])?$subdir:"").$news['infolink'].'">{L_FURTHER_INFO}</a>';

	$dHtml .= '</p>';

	return translate($dHtml);
}


function newsListFull($listName, $ab, $maxNbr){
	global $contentTables;

	if(!is_numeric($maxNbr)|| !is_numeric($ab)) return "Fehlerhafte Eingabeparameter.";
	if(! array_key_exists($listName,$contentTables)) return "Fehlerhafte Eingabeparameter.";
	$list = $contentTables[$listName];

	$dHtml = '<table class="memberlist" style="width:100%">';
	$sql = 'SELECT * FROM '.$list["sqlTable"].' ORDER BY date DESC LIMIT '.$ab.', '.$maxNbr.'; ';

	try{
		$db = get_db_handle();

		$result  = $db->query($sql);
		if( $result )
		while($news = $result->fetch(PDO::FETCH_ASSOC))
		{
			$dHtml .= '<tr><td class="hr pad">'.newsFull($news).'</td></tr>';
		}

	}catch(Exception $e){
		$dHtml .= 'Exception : '.$e->getMessage();
	}

	$dHtml .= '</table>';

	return $dHtml;
}

function newsListShort($listName, $ab, $maxNbr){
	global $contentTables;

	if(!is_numeric($maxNbr)|| !is_numeric($ab)) return "Fehlerhafte Eingabeparameter.";
	if(! array_key_exists($listName,$contentTables)) return "Fehlerhafte Eingabeparameter.";
	$list = $contentTables[$listName];

	$first=true;
	$dHtml = '<table class="memberlist" style="width:100%;">';
	$sql = 'SELECT * FROM '.$list["sqlTable"].' ORDER BY date DESC LIMIT '.$ab.', '.$maxNbr.'; ';
	try{
		$db = get_db_handle();

		$result  = $db->query($sql);
		if( $result )
		while($news = $result->fetch(PDO::FETCH_ASSOC))
		{
			$dHtml .= '<tr><td class="hr'.(!$first?' pad':'').'">'.newsShort($news).'</td></tr>';
			$first=false;
		}

	}catch(Exception $e){
		$dHtml .= 'Exception : '.$e->getMessage();
	}

	$dHtml .= '</table>';
	//$dHtml .= '<p><a href="news.php" dyn>All News</a></p>';

	return $dHtml;
}

function newsSingle($listName,$id){
	global $contentTables;
	if(!is_numeric($id)) return "Fehlerhafte Eingabeparameter.";
	$dHtml = '';

	$list=$contentTables[$listName];
	$sql =  'SELECT * FROM '.$list["sqlTable"].' WHERE id='.$id.' ORDER BY date DESC ';
	//echo $sql;
	try{
		$db = get_db_handle();

		$result  = $db->query($sql);
		if( $result )
		while($news = $result->fetch(PDO::FETCH_ASSOC))
		{
			$dHtml .= '<tr><td class="hr pad">'.newsFull($news).'</td></tr>';
		}

	}catch(Exception $e){
		$dHtml .= 'Exception : '.$e->getMessage();
	}
	$dHtml .= '<p><a href="news.php" dyn>Alle Meldungen</a></p>';

	return $dHtml;
}

?>
