function addLoadEvent(func,addToOnajaxload) {
	//Falls die Methode auch ausgeführt weden soll,
	//wenn ein Teil der Seite mit Ajax neu geladen wurde,
	//ist addToOnajaxload auf true zu setzen.
	var oldonload = window.onload;
	if (typeof window.onload != 'function') {
		window.onload = func;
	} else {
		window.onload = function() {
			oldonload();
			func();
		}
	}

	if(arguments.length>1 && addToOnajaxload==true){
		var oldajaxonload = window.onajaxload;
		if (typeof window.onajaxload != 'function') {
			window.onajaxload = func;
		} else {
			window.onajaxload = function() {
				oldajaxonload();
				func();
			}
		}
	}

}




function hasClass(ele,cls) {
	return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}
function addClass(ele,cls) {
	if (!this.hasClass(ele,cls)) ele.className += " "+cls;
}
function removeClass(ele,cls) {
	if (hasClass(ele,cls)) {
		var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
		ele.className=ele.className.replace(reg,' ');
	}
}


//Für die Suche außerhalb von document
function getElementById(el,id){
	if(el.id==id) return el;
	if(el.getAttribute("id")==id) return el;
	var c;
	for(var i=0;i<el.childNodes.length;i++)
		if(el.childNodes[i].nodeType==1){
			c = getElementById(el.childNodes[i],id);	
			if(c!=null)return c;
		}
	return null;
}


// Kopiert das Elternelement für das berechnete Formularfeld und setzt eine
// andere ID für das Neue Feld. Danach wird der Event vom Button überschrieben,
//  so dass beim nächsten Mal eine andere Id verwendet wird.
// Erwartet Ids der Form 'str_nr' und erzeugt 'str_nr2'
function addField(button,groupName,oldNr,newNr){
	var oldId = groupName+"["+oldNr+"]";
	var newId = groupName+"["+newNr+"]";
	var el = document.getElementById(oldId);

	var parent2 = el.parentNode.cloneNode(true);
	//alert(el+"\n"+parent2);
	var el2 = getElementById(parent2,oldId);

	//alert(el2);return;

	el2.id = newId;
	el2.name = newId;
	el2.value = "";//clear input field
	//	el.parentNode.parentNode.appendChild(document.createElement("br"));
	el.parentNode.parentNode.appendChild(parent2);
	//	button.parentNode.insertBefore( document.createElement("br") ,button);
	//	button.parentNode.insertBefore( clone ,button);

	button.onclick=function(){addField(button,groupName,oldNr,(newNr+1))};
}

//Entfernt das übergebene Element (div-Tag) incl. Inputfeld, wenn die Nr. nicht 0 ist.
//Letzteres soll minimale Anzahl Felder begrenzen.
function removeField(div,groupName,notThisNr){
	//var el = document.getElementById(groupName+"_"+nr);
	//button.parentNode.removeChild(button);
	if( getElementById(div,groupName+"["+notThisNr+"]")==null)
		div.parentNode.removeChild(div);
}

//Wie addField, nur dass hier kein Feld zum kopieren exisiert und der HTML-Code als Parameter übergeben werden muss
function createField(button,groupName,newNr,parentEl,html){
	parentEl.innerHTML = parentEl.innerHTML + html;
	button.onclick=function(){addField(button,groupName,newNr,(newNr+1))};
}

function resizeText(multiplier) {
	if (document.body.style.fontSize == "") {
		document.body.style.fontSize = "1.0em";
	}
	document.body.style.fontSize = parseFloat(document.body.style.fontSize)*(multiplier) + "em";
	document.cookie="fontsize=" + document.body.style.fontSize; 
}
function resizeTextToDefault() {
	//document.body.style.removeProperty('fontSize');
	document.body.style.fontSize = "1.0em";
	document.cookie="fontsize="; 
}
