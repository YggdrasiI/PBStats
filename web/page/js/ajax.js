/*

Funktion zum Aufrufen einer HTML/XML Seite per Javascript.
Bei Bedarf werden auch Javascript-Inhalte von der übertragenen Seite aus aufgerufen.

Der Aufruf gestaltet sich wie folgt:

<script language="javascript" type="text/javascript">
 getAXAH('http://www.xyz.com/testseite.html','hierHinein');
   document.getElementById(messageContainer).style.display = "block";
</script>
<div id="hierHinein"></div>

Wenn die einzubindende Seite Javascript enthält, muss in diesem die Kommentare in der form /* Kommentar * / geschrieben werden,
da durch die Eval Function alle Javascriptstatements als eine Zeile behandelt werden.

----------------------------------
(C) 2006 by Lukas Dorn-Fussenegger
(C) 2012 extended by Olaf Schulz

*/

function get(link){
//disabled
//return true;

//remove running timeouts
 try {window.clearTimeout(to);} catch (e) {};
 //fadeElement = document.getElementById('leftFrame');
 //fadeOut(0,'ajaxContent','ajaxInfo');
 getAXAH(link.href,'ajaxContent','ajaxInfo');

//change Linkclasses in the right Frame

rflinks = document.getElementsByName("rfLink");
for(j=0;j<rflinks.length;j++){
	removeClass(rflinks[j],"active");
	//rflinks[j].className = "";
}
 addClass(link,"active");
//link.className = "active";

updateHistory(link.href);


 return false;
}

/* getAXAH('http://www.url.com', 'DivElementWosHineinsoll') */
function getAXAH(url,elementContainer,messageContainer){

 /* Optionen festlegen */
 var showPlatzhalterWhileLoading = true;
 var execJavaScriptAfterTransfer = true;
 var changeStatusbar = false;
 
 /* Statuszeile anpassen. */
 if (changeStatusbar == true) { window.status = 'Ajax:' + url; }

 /* Anzeigen eines Blindtextes während des Ladevorganges, aber nur wenn noch kein Inhalt im Element vorhanden ist... */
 /* Diese Zeilen können bei bedarf entfernt werden */
 if (showPlatzhalterWhileLoading == true) {
   document.getElementById(elementContainer).style.display = "none";
   document.getElementById(messageContainer).innerHTML = document.getElementById(elementContainer).innerHTML;
   document.getElementById(messageContainer).style.display = "block";
   //document.getElementById(messageContainer).innerHTML = "<h2>Lade " + url + " ...</h2>";
   document.getElementById(messageContainer).innerHTML = "";
 }
 
 var theHttpRequest = getNewHttpObject();
 theHttpRequest.onreadystatechange = function() {processAXAH(elementContainer,messageContainer);};
 
 if (url.indexOf('?') == -1) {
  url = url + '?loadViaAjax=1';
 } else {
  url = url + '&loadViaAjax=1';
 }

 theHttpRequest.open("GET", url);

//andere Quelle bietet dies zum Laden ohne Caching (RANDOM-Parameter vermieden)
theHttpRequest.setRequestHeader("Pragma", "no-cache");
theHttpRequest.setRequestHeader("Cache-Control", "must-revalidate");
theHttpRequest.setRequestHeader("If-Modified-Since", document.lastModified);

 //theHttpRequest.send(false);
 theHttpRequest.send(null);
 
 function processAXAH(elementContainer,messageContainer){
  if (theHttpRequest.readyState == 4)
  {
   if (theHttpRequest.status == 200) {

    fadeElement = document.getElementById('leftFrame');
    fadeOut(0,elementContainer,messageContainer);
    document.getElementById(elementContainer).innerHTML = /*"<p>Dyn load...</p>"+*/ theHttpRequest.responseText;
    /* Javascript ausführen wenn eines mitgesendet wurde */
    if (execJavaScriptAfterTransfer == true) { execJS(document.getElementById(elementContainer)); }
   }
   else
   { document.getElementById(elementContainer).innerHTML="Fehler: " + theHttpRequest.statusText; } 
  } /* End If */
 } /* End Function */
 if (changeStatusbar == true) { window.status = ''; }
}

function getNewHttpObject() { var objType = false; try { objType = new ActiveXObject('Msxml2.XMLHTTP');}
 catch(e) {try { objType = new ActiveXObject('Microsoft.XMLHTTP'); } catch(e) { objType = new XMLHttpRequest(); }}
 return objType; }

function execJS(node) {
 /* Element auf Javascript überprüfen, und falls nötig ausführen */
 var bSaf = (navigator.userAgent.indexOf('Safari') != -1);
 var bOpera = (navigator.userAgent.indexOf('Opera') != -1);
 var bMoz = (navigator.appName == 'Netscape');
 var st = node.getElementsByTagName('script'); var strExec;
   
 for(var i=0;i<st.length; i++) { if (bSaf) { strExec = st[i].innerHTML; } else if (bOpera) { strExec = st[i].text; }
   else if (bMoz) { strExec = st[i].textContent; } else { strExec = st[i].text; } try { eval(strExec); } catch(e) { alert(e);}}}


var fadeElement = null;
var maxSteps = 7;//<10
var waitTime = 10;
function fadeOut(step,elementContainer, messageContainer){ 

  if(step == 9){
	fadeElement.style.backgroundColor = "white";
	fadeElement.style.backgroundImage = "";
  }

  if(step == maxSteps){
	  to = window.setTimeout("fadeIn("+(step)+",'"+elementContainer+"','"+messageContainer+"')", waitTime);
	displayContent(elementContainer, messageContainer);
	return;
  }
  fadeElement.style.backgroundImage = "url(style/w"+(step+1)+"0.png)";

  to = window.setTimeout("fadeOut("+(step+1)+",'"+elementContainer+"','"+messageContainer+"')", waitTime);

}

function fadeIn(step,elementContainer, messageContainer){
  if(step == 9){
	fadeElement.style.backgroundColor = "";
  }
  if(step == 0){
	fadeElement.style.backgroundImage = "";
//	displayContent(elementContainer, messageContainer);
	return;
  }

  fadeElement.style.backgroundImage = "url(style/w"+(step)+"0.png)";
  to = window.setTimeout("fadeIn("+(step-1)+",'"+elementContainer+"','"+messageContainer+"')", waitTime);
}

function displayContent(elementContainer, messageContainer){
   document.getElementById(messageContainer).style.display = "none";
   document.getElementById(elementContainer).style.display = "block";
   document.getElementById('mainBlock').scrollTop=0;
   //window.scrollTo(0, 0);
   if(window.onajaxload!=null) window.onajaxload();
}

var hasToReloadAjaxContent = false;
 hasToReloadAjaxContent = false;

function disableAjaxReload(){
 hasToReloadAjaxContent = false;
}

function updateHistory(file){
hasToReloadAjaxContent = false;
var ifrm = frames[0];
ifrm.document.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"> <html><head><title>HistoryFrame</title> <script src="js/ifrm.js" type="text/javascript"></script> </head><body onload="reload(\''+file+'\')"></body></html>');
ifrm.document.close();

}

function isLocalLink(el){
return false;
	if(el.hasAttribute("static")) return false;
  if(el.hasAttribute("dyn")) return true;
var l = location.href.replace(/^http.*:\/\/([^\/]+)\/([^\/]+)\/.*$/i,"$1/$2").toLowerCase();
var e = el.href.replace(/^http.*:\/\/([^\/]+)\/([^\/]+)\/.*$/i,"$1/$2").toLowerCase();

var phpExtension = el.href.search(/[^\/?]+\.php /i);

  if(l == e && phpExtension!=-1 ) return true;


 return false;
}



function changeVal() {
   var body = document.getElementsByTagName('body')[0];
   body.onclick = function (evt) {
      evt = (evt) ? evt : ((window.event) ? window.event : "");
      var elem = (evt.target) ? evt.target : evt.srcElement;
	while( elem.parentNode!=null){
      		if(elem.tagName=="A"){ 
			if(isLocalLink(elem)){
				return get(elem);
			} else
				break;
		}
		elem = elem.parentNode;
	}
   }    
}

addLoadEvent(disableAjaxReload);
addLoadEvent(changeVal);

