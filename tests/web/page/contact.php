<?php
// set $subdir to ../ if the php file will move to a subdirectory.
//$subdir = "../";
$subdir = "";

//set the var $htmlHead, if you want add html code between the <head> tags.
include($subdir."php/header.php");

?>
<!-- Paste/Write content here -->


<?php

/* Very ancient, but mostly enough:
 * The data is stored in one big array.
 */
include($subdir."php/members.php");



function createList($listname,$members){

	global $contactData;

	$html = "<h2>$listname</h2>";

	if( count($members)<1) return $html."<p>-</p>";

	$html .= "<table class='memberlist marginbottom'>";

	//foreach( $contactData as $person => $data){
	foreach( $members as $person){
		$data = $contactData[$person];

		$html .= "<tr>";
		$html .= '<td class="pad" style="padding-right:0.5em;">';
		if(false && hasValue("image",$data)){
			$image = '<img src="'.$data['image'].'" alt="Photo of '.$data['vname'].' '.$data['nname'].'">';
			if(hasValue("link",$data))
				$image = '<a href="'.$data['link'].'">'.$image."</a>";
			$html .= $image;
		}
		$html .= '</td>
			<td>';// class="padX">';
		if(hasValue("function",$data)){
			$html .= "<p><i>".$data['function']."</i></p>";
		}else{ }//$html .= "<p>&nbsp;</p>";}//Da das Sekretariat-Element jetzt alleine in einer Zeile steht, muss keine Zeile frei gelassen werden.
			$html .= "<p><b>".$data['title']." ".$data['vname']." ".$data['nname']."</b></p>";
		$html .= "<p></p><table>";
		//	if(hasValue("division",$data)) $html .= "<tr><td></td><td>".$data['division']."</td></tr>";
		//	if(hasValue("department",$data)) $html .= "<tr><td>&nbsp;&nbsp;</td><td>".$data['department']."<br><br></td></tr>";
		if(hasValue("room",$data)) $html .= "<tr><td>{L_OFFICE}:&nbsp;&nbsp;</td><td> Raum ".$data['room']."</td></tr>";
		if(hasValue("visitAddress",$data)) $html .= "<tr><td>&nbsp;&nbsp;</td><td>".$data['visitAddress']."</td></tr>";
		if(hasValue("mail",$data)) $html .= "<tr><td>{L_MAIL}: </td><td>".getMail($person,1)."</td></tr>";	
		if(hasValue("phone",$data)) $html .= "<tr><td>{L_TEL}:</td><td>".$data['phone']."</td></tr>";
		if(hasValue("fax",$data)) $html .= "<tr><td>{L_FAX}:</td><td>".$data['fax']."</td></tr>";
		if(hasValue("link",$data))
			$html .= "<tr><td></td><td><a href=\"".$data['link']."\">{L_HOMEPAGE}</a><br><br></td></tr>";

		if(hasValue("postalAddress",$data))
			$html .= "<tr><td>{L_ADDRESS}: </td><td>".$data['postalAddress']."</td></tr>";

		$html .= "</table>";
		$html .= "</td>";
		$html .= "</tr>";

	}

	$html .= "</table>";

	return $html;
}

$html = "<table style=\"width:100%\">
	<tr><td style=\"vertical-align:top;\">".
	createList("{L_MENU_CONTACT}",array("webmaster")).
	"</td><td style=\"vertical-align:top;\">".
	"</td></tr>
	</table>";

$tpl->loadStr($html);
$tpl->setLanguageTokens($lang);

echo $tpl->out();

?>

<?php 

include($subdir."php/footer.php");
?>
