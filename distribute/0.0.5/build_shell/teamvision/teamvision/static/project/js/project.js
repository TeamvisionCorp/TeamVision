$(document).ready(function() {
	var theme = 'metro';
	var currentUri=window.location.href;
    
    left_navitem_mouserover();
	left_nav_clickhandler();
	left_sub_navitem_mouserover();
    left_sub_nav_clickhandler();
    init_webapp_width();
    init_issue_filter_height();
    
    
    
    
    window.onresize = function() {
      	init_webapp_width();
      	init_issue_filter_height();
	}
    function init_webapp_width()
    {
     	 var left_hide_button=$("#leftbar_hide");
     	 if(left_hide_button)
         {
     		var container_width=$("#contentContainer").css("width");
         	if(container_width)
         	{
         		  var width1=container_width.replace("px","");
         		 $(".web-app-view-default").css("width",(width1)+"px"); 
         	}
         }
     	 else
     	 {
     		$(".web-app-view-default").css("width","100%");   
     	 }
     	 
     	$("#leftbar_hide").click(function(){
     		$(".web-app-view-default").css("width","100%");  
     	});
           
     	
    }
    
    function init_issue_filter_height()
    {
     	var container_height=$(".web-app-view-body-default").css("height");
     	if(container_height)
     		{
     		  var height1=container_height.replace("px","");
     		$(".issue-filter-panel-body").css("max-height",(height1-50)+"px"); 
     		$(".issue-item-panel-body").css("max-height",(height1-50)+"px"); 
     		$(".issue-item-panel-body").css("height",(height1-50)+"px"); 
     		
     		}
    }
    
    
	function left_navitem_mouserover() {
		$(".leftmenu li").mouseover(function() {
			$(this).addClass("leftmenuitemhover");
		});

		$(".leftmenu li").mouseout(function() {
			$(this).removeClass("leftmenuitemhover");
		});

	}
     
    
	function left_nav_clickhandler() {
		$(".leftmenu li").click(function() {
			$("li[class='leftmeunactive']").removeAttr("class");
			$(this).addClass("leftmeunactive");
		});
	}
	



	function left_sub_navitem_mouserover() {
		$(".left_sub_menu_container ul li").mouseover(function() {
			$(this).addClass("left_sub_menu_item_hover");
			$(".task_member_filter").parent().removeClass("left_sub_meun_active");
		});

		$(".left_sub_menu_container ul li").mouseout(function() {
			$(this).removeClass("left_sub_menu_item_hover");
		});

	}
	
	popmenu_search();
	function popmenu_search() {
		$("input[name=context_search_input]").keyup(function() {
			var inputKeyword = $(this).val().trim();
			var contextItems = $(this).parent().nextAll();
			for (var i = 0; i < contextItems.length; i++) {
				var currentItemText = $(contextItems[i]).text().trim();
				if (inputKeyword.trim() == "") {
					$(contextItems[i]).show();
				} else {
					if (currentItemText.toUpperCase().indexOf(inputKeyword.toUpperCase()) >= 0) {
						$(contextItems[i]).show();
					} else {
						$(contextItems[i]).hide();
					}

				}
			}
		});
	}

	function left_sub_nav_clickhandler() {
		$(".left_sub_menu_container ul li").click(function() 
		{
			$("li[class='left_sub_meun_active']").removeClass("left_sub_meun_active");
			$(this).addClass("left_sub_meun_active");
		});
		
		$(".task_member_filter li").click(function() 
		{
			$(".task_member_filter li").removeClass("left_sub_meun_active");
			$("#task_owner_filter").val($(this).attr('labelid'));
			$(this).addClass("left_sub_meun_active");
		});
	}
	
	

});
