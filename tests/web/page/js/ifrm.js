function reload(file){
if(parent.hasToReloadAjaxContent == true)
 parent.getAXAH(file,'ajaxContent','ajaxInfo');
parent.hasToReloadAjaxContent = true;
}
