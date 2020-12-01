<?php

//Helper to shorting code
function translate($html){
	global $tpl, $lang;
	return $tpl->insertLaguageToken($html,$lang);
}

class Template
{


	protected  $language = 'de';

/**
 Konstruktor, dem die gewählte Sprache (de,en) uebergeben werden muss.

 */
	function __construct($language) {
		global $lang; // prepare complete disbanding of global var $lang
		$this->language = $language."/";
		$this->lang = &$lang;
	}

	/**
	 * Der Ordner in dem sich die Template-Dateien befinden.
	 *
	 * @access public
	 * @var    string
	 */
	protected $templateDir = "templates/";

	/**
	 * Der Ordner in dem sich die Sprach-Dateien befinden
	 *
	 * @access public
	 * @var    string
	 */
	protected $languageDir = "languages/";

	/**
	 * Der linke Delimter für einen Standard-Platzhalter
	 *
	 * @access public
	 * @var    string
	 */
	protected $leftDelimiter = '{$';

	/**
	 * Der rechte Delimter für einen Standard-Platzhalter
	 *
	 * @access public
	 * @var    string
	 */
	protected $rightDelimiter = '}';

	/**
	 * Der linke Delimter für eine Funktion
	 *
	 * @access public
	 * @var    string
	 */
	protected $leftDelimiterF = '{';

	/**
	 * Der rechte Delimter für eine Funktion
	 *
	 * @access public
	 * @var    string
	 */
	protected $rightDelimiterF = '}';

	/**
	 * Der linke Delimter für ein Kommentar
	 * Sonderzeichen müssen escaped werden, weil der Delimter in einem RegExp
	 * verwendet wird.
	 *
	 * @access public
	 * @var    string
	 */
	protected $leftDelimiterC = '\{\*';

	/**
	 * Der rechte Delimter für ein Kommentar
	 * Sonderzeichen müssen escaped werden, weil der Delimter in einem RegExp
	 * verwendet wird.
	 *
	 * @access public
	 * @var    string
	 */
	protected $rightDelimiterC = '\*\}';

	/**
	 * Der linke Delimter für eine Sprachvariable
	 * Sonderzeichen müssen escaped werden, weil der Delimter in einem RegExp
	 * verwendet wird.
	 *
	 * @access public
	 * @var    string
	 */
	protected $leftDelimiterL = '\{L_';

	/**
	 * Der rechte Delimter für eine Sprachvariable
	 * Sonderzeichen müssen escaped werden, weil der Delimter in einem RegExp
	 * verwendet wird.
	 *
	 * @access public
	 * @var    string
	 */
	protected $rightDelimiterL = '\}';

	protected $argumentDelimiterL = '\|';
	protected $argumentDelimiterLunescaped = '|';

	/**
	 * Der komplette Pfad der Templatedatei.
	 *
	 * @access protected
	 * @var    string
	 */
	protected $templateFile = "";

	/**
	 * Der komplette Pfad der Sprachdatei.
	 *
	 * @access protected
	 * @var    string
	 */
	protected $languageFiles = array();

	/**
	 * Der Dateiname der Templatedatei
	 *
	 * @access protected
	 * @var    string
	 */
	protected $templateName = "";

	/**
	 * Der Inhalt des Templates.
	 *
	 * @access protected
	 * @var    string
	 */
	protected $template = "";

	/**
	 * Use $lang - Array for lookup
	 * of token.
	 */
	protected function replaceToken($token, &$lang){
		//$token = strtolower($token);//already done
		if( array_key_exists($token,$lang) ){
			return $lang[$token];
		}else{
			//return $token ;
			//return $this->leftDelimiterL . $token . $this->rightDelimiterL  ;
			return "{L_" . $token . "}";
		}	
	}

	/**
	 * Ein paar Eigenschaften ihre Werte zuweisen
	 *
	 * @access    public
	 * @return    boolean
	 */
	public function template($tpl_dir = "", $lang_dir = "") 
	{
		// Template Ordner ändern
		if (!empty($tpl_dir)) {
			$this->templateDir = $tpl_dir;
		}

		// Language Ordner ändern
		if (!empty($lang_dir)) {
			$this->languageDir = $lang_dir;
		}

		return true;
	}


	/**
	 * Die Templatedatei öffnen
	 *
	 * @access    public
	 * @param     string $file Dateiname des Templates
	 * @return    boolean
	 */
	public function load($file)
	{
		// Die Eigenschaften zuweisen
		$this->templateName = $file;
		$this->templateFile = $this->templateDir.$file;

		// Wenn ein Dateiname übergeben wurde, versuchen, die Datei zu öffnen
		if(!empty($this->templateFile)) {
			if($fp = @fopen($this->templateFile, "r")) {
				// Den Inhalt des Templates einlesen
				$this->template = fread($fp, filesize($this->templateFile)); 
				fclose ($fp); 
			} else {
				return false;
			}
		}

		// Die methode replaceFuntions() aufrufen
		$this->replaceFunctions();

		return true;
	}


	/** Template-String direkt übergeben (zur Laufzeit generiert)
	 */
	public function loadStr($str)
	{
		$this->template = $str;

		// Die methode replaceFuntions() aufrufen
		//$this->replaceFunctions();

		return true;

	}


	/**
	 * Die Standard-Platzhalter ersetzen
	 *
	 * @access    public
	 * @param     string $replace      Name of var which should be replaced
	 * @param     string $replacement  Text with which to replace the var
	 * @return    boolean
	 */
	public function assign($replace, $replacement)
	{
		$this->template = str_replace($this->leftDelimiter.$replace.$this->rightDelimiter, $replacement, $this->template);
		return  true;
	}



	/**
	 * Die Sprachdateien öffnen
	 *
	 * @access    public
	 * @param     array $files  Dateinamen der Sprachdateien
	 * @return    boolean
	 */
	public function loadLanguage(&$files,&$lang)
	{
		global $subdir;
		if( $this->language === "none/" ) return;

		// Versuchen, alle Sprachdateien einzubinden
		//        for ($i=0;$i<count($this->languageFiles);$i++) {
		foreach ($files as $lFile){
			// wenn die Datei schon geladen wurde, ignorieren
			if( in_array($lFile,$this->languageFiles) )
				continue;
			// wenn die Datei $this->languageDir.$this->languageFiles[$i] nicht existiert
			if (!file_exists($subdir.$this->languageDir.$this->language.$lFile)) {
				//return false;
				echo "Warning. Can not load '".$subdir.$this->languageDir.$this->language.$lFile."'.<br>";
			}else{
				include($subdir.$this->languageDir.$this->language.$lFile);
			}
			$this->languageFiles[] = $lFile;

			//Alternative: 
			//include_once($subdir.$this->languageDir.$this->language.$lFile);
		}

		return ;
	}


	/**
	 * Die Sprachvariablen ersetzen
	 *
	 * @access    protected
	 * @param     string $lang
	 * @return    boolean
	 */
	public function setLanguageTokens(&$lang)
	{
		if( $this->language === "none/" ) return;

		$this->template = $this->insertLaguageToken($this->template,$lang);
		return true;

	}


	/**
	 * Die Funktionen ersetzen
	 *
	 * @access    protected
	 * @return    boolean
	 */
	protected function replaceFunctions()
	{
		// Includes ersetzen ( {include file="..."} )
		while(preg_match("/".$this->leftDelimiterF."include file=\"(.*)\.(.*)\"".$this->rightDelimiterF."/isUe", $this->template)) {
			$this->template = preg_replace("/".$this->leftDelimiterF."include file=\"(.*)\.(.*)\"".$this->rightDelimiterF."/isUe", "file_get_contents(\$this->templateDir.'\\1'.'.'.'\\2')", $this->template);
		}


		// Kommentare löschen
		$this->template = preg_replace("/".$this->leftDelimiterC."(.*)".$this->rightDelimiterC."/isUe", "", $this->template);

		return  true;
	}  

	/**
	 * Das fertige Template ausgeben
	 *
	 * @access    public
	 * @return    boolean
	 */
	public function out()
	{
		//echo $this->template;
		//return true;
		return $this->template;
	}

	/*Callback for preg_replace calls.
	 * Will replace {L_word} with $lang["word"].
	 * */
	public function preg_callback1($treffer) {
		$key = strtolower($treffer[1]);
		return $this->replaceToken($key,$this->lang);
	}

	/*Callback for preg_replace calls.
	 * Will replace {L_word|X} with 
	 * vsprintf($lang["word"],X)
	 * X can be be one or more arguments.
	 *
	 * Example:
	 * {L_units|3|Shakka} and  $lang[units] = "%s units was gifted to %s."
	 * will be transformed to "3 units was gifted to Shakka.".
	 * */
	public function preg_callback2($treffer) {
		$key = strtolower( $treffer[1] );
		$args = explode( $this->argumentDelimiterLunescaped, $treffer[2] ); 
		return vsprintf( $this->replaceToken($key,$this->lang), $args );
	}

	/**
	 * Convert. Use loaded language files
	 * and return tranlated file.
	 * Nesting could be problematic due non-recursion.
	 */
	public function insertLaguageToken($html, &$lang)
	{
		if( $this->language === "none/" ) return $html;
		$html2 = &$html;

		// simple replace width preg_replace

		//0. Replace innerst tokens without arguments {L_[NAME]}
		$html2 = preg_replace_callback(
			"/".$this->leftDelimiterL."([^".$this->rightDelimiterL.$this->argumentDelimiterL."]*)"
			. $this->rightDelimiterL."/isU",
			array($this,'preg_callback1'),
			$html2
		);

		//1. Replace tokens with arguments {L_[NAME],s1,s2,...}
		$html2 = preg_replace_callback(
			"/".$this->leftDelimiterL."([^".$this->rightDelimiterL.$this->argumentDelimiterL."]*)"
			. $this->argumentDelimiterL."([^".$this->rightDelimiterL."]*)".$this->rightDelimiterL."/isU",
			array($this,'preg_callback2'),
			$html2
		);

		//2. Replace tokens without arguments {L_[NAME]} (same as 0.)
		/*
		$html2 = preg_replace_callback(
			"/".$this->leftDelimiterL."([^".$this->rightDelimiterL.$this->argumentDelimiterL."]*)"
			. $this->rightDelimiterL."/isU",
			array($this,'preg_callback1'),
			$html2
		);
		 */

		return $html2;
	}
}
?> 
