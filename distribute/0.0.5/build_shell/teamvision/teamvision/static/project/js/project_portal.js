$(document).ready(function() {
	var theme = 'metro';
	var rootUri = window.location.href;
    var current_filter="all";

    load_device_view("all");

	project_item_mouserover();
    
    
	$("#project_portal_project_listview").height($(window).height()-160);
	
	
    $("#portal_add_project").click(function() 
    {
		$("#head_add_project").trigger('click');
	});
    
    
    $("#portal_toolbar_add_project").click(function() 
    	    {
    			$("#head_add_project").trigger('click');
    	});
    
    
    
     
    function project_item_mouserover() {
		$("div[name=portal-project-item]").mouseover(function() {
			$(this).addClass("portal_project_hover");
		});

		$("div[name=portal-project-item]").mouseout(function() {
			$(this).removeClass("portal_project_hover");
		});

	}
   

    $("#project_portal_page_menu").children().click(function()
    {
    	$("#project_portal_page_menu").children().each(function()
    	{
     	  $(this).removeClass("project_portal_menu_item_active");
          });
     	$(this).addClass("project_portal_menu_item_active");
     	var filter=$(this).attr("method");
     	load_device_view(filter);
    });
     
     


    function load_device_view(filter)
    {
    	current_filter=filter;
    	$("#project_portal_project_listview").load("/project/filter",{"project_filter":filter},function(data,status)
       {
       });
    }
     
	

});
