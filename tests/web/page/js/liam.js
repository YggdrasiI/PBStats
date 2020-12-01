/*
 * Tiny mail adresses mask/unmask algo.
 * This script make the "liam"-Links clickable.
 * */

function addLiamOnClick(){

	liam = document.getElementsByName("liam");
	for(i=0;i<liam.length;i++){
		liam[i].onclick=openLiam;
	}

}

//Add liamEvent after the page or ajax content was loaded.
addLoadEvent(addLiamOnClick,true);

function openLiam(evt){

	evt = (evt) ? evt : ((window.event) ? window.event : "");
	var elem = (evt.target) ? evt.target : evt.srcElement;

	while(elem.getAttribute("class")!="liam" && elem.parentNode!=null)
		elem = elem.parentNode;

	if(elem.parentNode==null) return;

	liam = getText(elem);
	liam = String.fromCharCode(109, 97, 105, 108, 116, 111, 58)+liam;
	var sub = (elem.hasAttribute("sub"))?elem.getAttribute("sub"):'';
	var msg = (elem.hasAttribute("msg"))?elem.getAttribute("msg"):'';
	var mailto_link = liam+'?subject='+sub+'&body='+msg;

//	window.location.href = mailto_link;
	win = window.open(mailto_link,'emailWindow');
	if (win && win.open &&!win.closed) win.close();
	 

}

function getText(el){
	pre=el.getAttribute("pre");
	if( pre!==null){
		return pre+String.fromCharCode(64)+el.getAttribute("suf");
	}else
		return getTextRecursive(el,0,0);

}

function getTextRecursive(el,depth,cNbr){
	if( el.nodeType==3) return el.nodeValue;
	var s="";
	for(var i=0;i<el.childNodes.length;i++){
		if(el.childNodes[i].nodeType==3 || el.childNodes[i].nodeType==1)
			s = s+getTextRecursive(el.childNodes[i],depth+1,i);
		if(depth==0&&i==0)
			s = s+String.fromCharCode(64);
	}
	return s;
}



