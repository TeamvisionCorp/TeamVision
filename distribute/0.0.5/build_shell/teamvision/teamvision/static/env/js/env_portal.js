$(document).ready(function() {
	var theme = 'metro';
	var rootUri = window.location.href;
    var current_filter="all";

    load_env_view("all");

	env_item_mouserover();
    
    
	
    $("#portal_add_env").click(function() 
    {
		$("#head_add_env").trigger('click');
	});
    
    
    $("#portal_toolbar_add_env").click(function() 
    	    {
    			$("#head_add_env").trigger('click');
    		});
    
    
    
    
    
	
	
     
    function env_item_mouserover() {
		$(".env_archive_folder").mouseover(function() {
			$(this).addClass("portal_env_hover");
		});

		$(".env_archive_folder").mouseout(function() {
			$(this).removeClass("portal_env_hover");
		});

	}
   

    $("#env_portal_page_menu").children().click(function()
    {
    	$("#env_portal_page_menu").children().each(function()
    	{
     	  $(this).removeClass("env_portal_menu_item_active");
          });
     	$(this).addClass("env_portal_menu_item_active");
     	var filter=$(this).attr("method");
     	load_device_view(filter);
    });
     
     


    function load_env_view(filter)
    {
    	current_filter=filter;
    	$("#env_portal_env_listview").load("/env/filter",{"env_filter":filter},function(data,status)
       {
       });
    }
     
	

});
