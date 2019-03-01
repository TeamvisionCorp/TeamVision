$(document).ready(function() {
	var theme = 'metro';
	var rootUri = window.location.href;
	var window_height=$(window).height();
	

	project_item_mouserover();
    
	$("#home_dashboard_project_listview").css("max-height",(window_height-180)+"px"); 
	  
    $("#home_add_project").click(function() 
    {
		$("#head_add_project").trigger('click');
	});
    
    $("#home_project_toolbar_add_project").click(function() 
    	    {
    			$("#head_add_project").trigger('click');
    		});
    
    
    
	
	
     
    function project_item_mouserover() {
		$("div[name=home-project-item]").mouseover(function() {
			$(this).addClass("home_project_hover");
		});

		$("div[name=home-project-item]").mouseout(function() {
			$(this).removeClass("home_project_hover");
		});

	}
     
	

});
