<?php

abstract class FormularField{
	public $fieldName, $descrip, $formatFunction, $validInputFunction, $optional, $inclFieldInSqlStatements, $defaultValue;

	function __construct(
		$fieldName,
		$descrip,
		$formatFunction,
		$optional, $inclFieldInSqlStatements,
		$validInputFunction=null,
		$defaultValue=null 
	){
		$this->fieldName = $fieldName;
		$this->descrip = $descrip;
		$this->formatFunction = $formatFunction;
		$this->optional = $optional;
		$this->inclFieldInSqlStatements = $inclFieldInSqlStatements;
		$this->defaultValue = $defaultValue;
		$this->validInputFunction = $validInputFunction;

		$this->invalidClass = "class='invalidFormInput'";
	}

	function fieldDescrip(){
		$html = '';
		if($this->isOptional() ){
			$o = ' ({L_OPTIONAL})';
		}else{
			$o='';
		}
		if( is_string($this->descrip) ){
			$html .= translate("<b>".$this->descrip."</b>".$o);
		}else if( is_object($this->descrip) ){
			$html .= translate($this->descrip->html($this->isOptional()).$o);
		}else{
			$html .= $this->fieldName;
		}
		return $html;
	}

	function isValidInput($input){
		if( $this->validInputFunction == null ){
			if( $this->isOptional() ) return true;
			return false;
		}else{
			return call_user_func($this->validInputFunction, $input);
		}
	}

	function format($str){
		return call_user_func_recursive($str, $this->formatFunction);
	}

	function showField(){
		return ($this->optional>-1);
	}

	function isOptional(){
		return ($this->optional==1);
	}

	function inclSql(){
		return ($this->inclFieldInSqlStatements==1);
	}

	function getDefaultValue(){
		return $this->defaultValue;
	}

	abstract function html($input, $bMarkInvalid );

}

/* Dummy class for fields which will be completly hidden
 * from users. This dummy is required to guarentee that
 * each tablerow has an field repersentation
 * in dbClass->paramFields.
 *
 * Note: Dummy-Field got the optinal-Flag to surpress any valid
 * 	checking on the field values.
 * */
class DummyField extends FormularField{
	function __construct($fieldName, $formatFunction, $validInputFunction=null, $defaultValue=null){
		parent::__construct($fieldName, "", $formatFunction, 1, 1, $validInputFunction, $defaultValue);
	}
	function html($input, $bMarkInvalid){
		return "";
	}
}

class InputField extends FormularField{
	//Kein Konstruktor -> Parent Konstruktor wird aufgerufen.

	function html($input, $bMarkInvalid){
		return $this->fieldDescrip().'<br><input '.($bMarkInvalid?$this->invalidClass:'').' id="'.$this->fieldName.'" name="'.$this->fieldName.'" '.(!is_null($input)?'value="'.$input.'" ':'').'type="text" size="30"></input>'."\n\r";
	}
}

class Textarea extends FormularField{

	function html($input, $bMarkInvalid){
		return $this->fieldDescrip().'<br><textarea '.($bMarkInvalid?$this->invalidClass:'').' id="'.$this->fieldName.'" name="'.$this->fieldName.'" cols="30" rows="10">'.(!is_null($input)?$input:'').'</textarea>'."\n\r";
	}
}

class NmbrInputField extends FormularField{

	function html($input, $bMarkInvalid){
		return $this->fieldDescrip().'<br><input '.($bMarkInvalid?$this->invalidClass:'').' id="'.$this->fieldName.'" name="'.$this->fieldName.'" '.(!is_null($input)?'value="'.$input.'" ':'').' type="text" size="15"></input> (' . translate("{L_NUMBER}") . ')'."\n\r";
	}

}
class Checkbox extends FormularField{

	function html($input, $bMarkInvalid){
		return '<input '.($bMarkInvalid?$this->invalidClass:'').' id="'.$this->fieldName.'" name="'.$this->fieldName.'" value="1" '.(($input=="1")?'checked':'').' type="checkbox"></input>'.$this->fieldDescrip()."\n\r";
	}

	function isValidInput($input){
		if( $this->validInputFunction == null ){
			return true;
		}else{
			return call_user_func($this->validInputFunction, $input);
		}
	}
}

class DateInputField extends FormularField{

	function html($input, $bMarkInvalid){
		return $this->fieldDescrip().'<br><input '.($bMarkInvalid?$this->invalidClass:'').' id="'.$this->fieldName.'" name="'.$this->fieldName.'" '.(!is_null($input)?'value="'.str_replace(" ", "", formatDate($input)).    '" ':'').' type="text" size="15"></input> (TT.MM.JJJJ)'."\n\r";
	}
}

class HiddenDateField extends FormularField{

	function __construct(
		$fieldName,
		$descrip,
		$formatFunction,
		$optional, $inclFieldInSqlStatements,
		$validInputFunction = "positiveNumber",
		$defaultValue = null 
	){
		parent::__construct($fieldName, $descrip, $formatFunction, $optional, $inclFieldInSqlStatements,
			$validInputFunction, $defaultValue );
	}

	function html($input, $bMarkInvalid){
		if(!is_null($input))
			$timestamp = $input;
		else
			$timestamp = time();
		$now = formatDateTime($timestamp);
		return $this->fieldDescrip().'<br>'.$now.'<input id="'.$this->fieldName.'" name="'.$this->fieldName.'" type="hidden" value="'.$timestamp.'">' ."\n\r";
	}
}

class MultipleInputField extends FormularField{
	//Hier kann $input ein Array von Werten sein
	function  html($input, $bMarkInvalid){
		if(is_null($input) ||$input=="" ){
			return $this->fieldDescrip().'<br><div '.($bMarkInvalid?$this->invalidClass:'').' ><div><input id="'.$this->fieldName.'[0]" name="'.$this->fieldName.'[0]" type="text" size="30"></input>
				<input type="button" value="-" title="Eingabefeld entfernen" onClick="removeField(this.parentNode,\''.$this->fieldName.'\',0)"></input></div></div>'
				.'<br><input type="button" value="+" title="weiteres Eingabefeld hinzufügen" onClick="addField(this,\''.$this->fieldName.'\',0,1)"></input>'."\n\r";

		}else{
			$html = $this->fieldDescrip().'<br><div '.($bMarkInvalid?$this->invalidClass:'').' >';
			$last = 0;
			if(!is_array($input)) $input = array(0=>$input);
			ksort($input);
			foreach( $input as $key=>$val){
				$html .= '<div><input id="'.$this->fieldName.'['.$key.']" name="'.$this->fieldName.'['.$key.']" value="'.$val.'" type="text" size="30"></input>
					<input type="button" value="-" title="Eingabefeld entfernen" onClick="removeField(this.parentNode,\''.$this->fieldName.'\',0)"></input><br></div>';
				$last = $key;
			}

			$html .= '</div><br><input type="button" value="+" title="weiteres Eingabefeld hinzufügen" onClick="addField(this,\''.$this->fieldName.'\',0,'.($last+1).')"></input>'."\n\r";

			return $html;
		}

	}

}

class UploadField extends FormularField{

	function html($input, $bMarkInvalid){
		if(is_null($input) || empty($input)){
			return $this->fieldDescrip().'<br><input '.($bMarkInvalid?$this->invalidClass:'').' id="'.$this->fieldName.'" name="'.$this->fieldName.'" type="file" size="15"></input>'."\n\r";
		}else{
			//print_r($savedFiles); 
			return $this->fieldDescrip().'<div><input type="hidden" id="'.$this->fieldName.'" name="'.$this->fieldName.'" value="'.$input.'"></input>Datei '.$input.'</div>';
		}
	}

}//End Class UploadField 

class MultipleUploadField extends FormularField{
	//$input kann Array sein
	function html($input, $bMarkInvalid){
		$html = '';
		if(is_null($input) || empty($input)){
			$html .= $this->fieldDescrip().'<br><div '.($bMarkInvalid?$this->invalidClass:'').' ><div><input id="'.$this->fieldName.'[0]" name="'.$this->fieldName.'[0]" type="file" size="15"></input>
				<input type="button" value="-" title="Dateifeld entfernen" onClick="removeField(this.parentNode,\''.$this->fieldName.'\',0)"></input></div></div>'
				.'<br><input type="button" value="+" title="weitere Datei hinzufügen" onClick="addField(this,\''.$this->fieldName.'\',0,1)"></input>'."\n\r";
		}else{
			if(!is_array($input)) $input = array(0=>$input);
			ksort($input);

			$html .= $this->fieldDescrip().'<br><div '.($bMarkInvalid?$this->invalidClass:'').' >';
			$last = 0;
			foreach( $input as $key=>$val){
				$html .= '<div id="div_'.$this->fieldName.'"><input id="'.$this->fieldName.'['.$key.']" name="'.$this->fieldName.'['.$key.']" value="'.$val.'" type="hidden" size="15"></input>
					Datei '.$val.'
					<input type="button" value="-" title="Datei entfernen" onClick="removeField(this.parentNode,\''.$this->fieldName.'\'),-1"></input><br></div>';
				$last = $key;
			}

			$html .= '<br><div><div><input id="'.$this->fieldName.'['.($last+1).']" name="'.$this->fieldName.'['.($last+1).']" type="file" size="15"></input>
				<input type="button" value="-" title="Dateifeld entfernen" onClick="removeField(this.parentNode,\''.$this->fieldName.'\','.($last+1).')"></input></div></div>'
				.'<br><input type="button" value="+" title="weitere Datei hinzufügen" onClick="addField(this,\''.$this->fieldName.'\','.($last+1).','.($last+2).')"></input>'."\n\r";

		}
		return $html;
	}

}

class OptionField extends FormularField{
	var $sql,$defaultId;
	//Eigener Konstruktor
	function OptionField($fieldName, $descrip, $formatFunction, $optional, $sql, $defaultId){
		parent::__construct($fieldName, $descrip, $formatFunction, $optional, 1, "positiveNumber", 1);
		$this->sql = $sql;
		$this->defaultId = $defaultId;
	}

	function html($input, $bMarkInvalid){
		$html = '';
		if(!is_null($input))
			$selectedElement = $input;
		else
			$selectedElement = $this->defaultId;
		$html .= $this->fieldDescrip().'<br><select '.($bMarkInvalid?$this->invalidClass:'').'  id="'.$this->fieldName.'" name="'.$this->fieldName.'" size="1">'."\n\r";

		try{
			$db = get_db_handle();

			$result = $db->query($this->sql);
			if( $result )
			while($entry = $result->fetch(PDO::FETCH_ASSOC))
			{
				$html .= '<option value="'.$entry["id"].'"'.($entry["id"]==$selectedElement?" selected":"").'>'.$entry["title"].'</option>'."\n\r";
			}

		}catch(Exception $e){
			$html .= 'Exception : '.$e->getMessage();
		}
		$html .= '</select>';


		return $html;

	}
}



/*
Darstellung von Infofeldern (drei Arten)
 */
class Infofield{

	function Infofield($infotext, $basetext, $cssClass){
		$this->infotext=$infotext;
		$this->basetext=$basetext;
		$this->cssClass=$cssClass;
	}

	function html($optional){
		if(!is_null($this->infotext))
			return '<span class="'.$this->cssClass.'" infotext="'.$this->infotext.'"><b>'.$this->basetext.'</b></span>';
		//return '<b><div class="'.$this->cssClass.'" infotext="'.$this->infotext.'">'.$this->basetext.'</div></b>';
		else
			return '<div class="'.$this->cssClass.'"><b>'.$this->basetext.'</b></div>';
	}

}


?>
