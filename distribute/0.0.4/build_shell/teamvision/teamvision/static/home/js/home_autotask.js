$(document).ready(function() {
	var theme = 'metro';

	// load_left_navitem();
	// load_left_sub_navitem();
	// load_autotask_listview();
	// load_dashboard_page();


	
	
	$("#home_autotask_addbutton").jqxButton({
			theme : theme,
			width : '100',
			height : '30',
			roundedCorners : 'all'
		});

	function clearLRcolumn() {
		$("#leftContainer").empty();
		$("#middleContainer").empty();

	}
    
    left_navitem_mouserover();
	left_nav_clickhandler();
    
	function load_left_navitem() {
		$("#leftContainer").load('home/autotask/get_left_navigater', function() {
			left_navitem_mouserover();
			left_nav_clickhandler();
		});

	}
   left_sub_navitem_mouserover();
			left_sub_nav_clickhandler();
 
	function load_left_sub_navitem() {
		$("#home_autotask_sub_leftnav").load('home/autotask/get_left_sub_nav', function() {
			left_sub_navitem_mouserover();
			left_sub_nav_clickhandler();
		});

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
		});

		$(".left_sub_menu_container ul li").mouseout(function() {
			$(this).removeClass("left_sub_menu_item_hover");
		});

	}

	function left_sub_nav_clickhandler() {
		$(".nav li").click(function() 
		{
			$("li[class='left_sub_meun_active']").removeClass("left_sub_meun_active");
			$(this).addClass("left_sub_meun_active");
		});
	}

	function load_autotask_listview() {
		$("#home_autotask_view").load('home/autotask/get_autotask_list', function() {
			// var source = ['JavaScript Certification - Welcome to our network', 'Business Challenges via Web take a part', 'jQWidgets better web, less time. Take a tour', 'Facebook - you have 7 new notifications', 'Twitter - John Doe is following you. Look at his profile', 'New videos, take a look at YouTube.com'];
			// $('#home_autotask_listview_dcocking').jqxDocking({
				// theme : theme,
				// orientation : 'vertical',
				// mode : 'docked',
				// windowsOffset : 20,
				// width : "100%"
			// });
			// // $('#home_autotask_listview_dcocking').jqxDocking('enableWindowResize', 'home_autotask_listview_window');
			// $('#home_autotask_listview_window').jqxWindow({ maxHeight:5000}); 
			// var height=$(document).height();
			// $('#home_autotask_listview_window').css("height",height);
// 			
		   // $(window).resize(function()
			// {
// 
                  // var height=$(document).height();
//                   
		          // $('#home_autotask_listview_window').css("height",height);
			// });
			// autotask_item_mouserover();
		});

	}
	
     
    function autotask_item_mouserover() 
    {
		$("#home_autotask_listview_autotaskul li").mouseover(function() {
			$(this).addClass("home_autotask_hover");
		});

		$("#home_autotask_listview_autotaskul li").mouseout(function() {
			$(this).removeClass("home_autotask_hover");
		});

	}
     
});
