$(document).ready(function() {
	var theme = 'metro';
	
	init_home_issue_container_height();
	
	function init_home_issue_container_height()
    {
     	var container_height=$(".web-app-view-body-default").css("height");
     	if(container_height)
     		{
     		  var height1=container_height.replace("px","");
     		$(".issue-item-panel-body").css("height",(height1-50)+"px");
     		$(".issue-item-panel").parent().css("width","100%");
     		
     		}
    }
	
});