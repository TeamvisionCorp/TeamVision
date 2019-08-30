$(document).ready(function() {
	// Create a jqxMenu

	var theme = 'metro';
	var rootUri=window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	load_header_menu();
	load_header_settings();
	$("body").show();

	init_page();
	show_header_project_popmenu();
	select_header_project_item();
	popmenu_search("context_search_input");
	popmenu_search("header_project_search_input");
//	minsized_header_settings_menu();


	function init_page() {
		/*初始化页面元素*/
		$("div[name=project-group]").hide();
		// $("input[name=context_search_input]").hide();

	}

	/*点击元素之外的地方隐藏控件*/
	function hide_control_byclick_page(hide_object, trigger) {

		trigger.click(function(e) {
			e.stopPropagation();
		});

		$(document).on('click', function(e) {
			if(!parentHasClass(e.target,"filed-pop-meun"))
			{
				hide_object.hide();
			}
		});
	}
	
	function parentHasClass (obj,className){ 
		while (obj != undefined && obj != null && obj.tagName.toUpperCase() != 'BODY'){ 
		if ($(obj).hasClass(className)){ 
		return true; 
		} 
		obj = obj.parentNode; 
		} 
		return false; 
		} 
	


	function show_header_project_popmenu() {
		$("#header_project_name").click(function() {
			var popmenu = $(this).parent().find("div[name=project-group]");
			currentoPopObject = popmenu;
			currentTrigger = $(this);
			popmenu.show();
			popmenu.addClass("filed-pop-meun");
			var current_project=$("#project_id").attr("projectid");
		    $(popmenu).find("li[labelid="+current_project+"]").children("i:eq(0)").addClass('fa-check');
			hide_control_byclick_page(popmenu, $(this));
		});

	}

	function select_header_project_item() {
		$("input[name=header_project_search_input]").parent().nextAll().each(function() 
		{
			$(this).click(function(e) {
				e.stopPropagation();
				var labelid = $(this).attr('labelid');
				var text = $(this).text().trim();
				var background = $(this).children("i:eq(1)").css('color');
				var firstChild = $(this).children("i:eq(0)");
				var classname = firstChild.attr('class');
				if (classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) 
				{
					//从调用接口删除数据
				} else {
					uncheck_all_project_menu_item($(this),$(this).parent());
			        firstChild.addClass('fa-check');
			        var current_project=$("#project_id").attr("projectid");
			        $("div[name=project-group]").hide();
			        var new_url=rootUri.replace("project/"+current_project,"project/"+labelid);
			        console.log(new_url);
			        window.location.href=new_url;
					//调用接口添加用户数据
				}
			});
		});
	}
	
	function uncheck_all_project_menu_item(currentitem, role_group) {
		role_group.children().each(function() {
			if ($(this) != $(currentitem)) {
				var labelid = $(this).attr('labelid');
				var firstChild = $(this).children("i:eq(0)");
				var classname = firstChild.attr('class');
				if (classname && classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) {
					firstChild.removeClass('fa-check');
					var removedlabel = $(this).parent().parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
					removedlabel.remove();
				}

			}
		});
	}

	function popmenu_search(menu_name) {
		$("input[name="+menu_name+"]").keyup(function() {
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

	//加载header menu
	function load_header_menu() {
//		$("#headermenubar").jqxMenu({
//			theme : "metro",
//			animationShowDuration : 300,
//			animationHideDuration : 200,
//			animationShowDelay : 200,
//			showTopLevelArrows : true,
//			autoOpen : false
//		});
//		$("#headermenubar").css('visibility', 'visible');
	}
	
	

	//加载页头设置菜单
	function load_header_settings() {
		$("#headersettingbar").jqxMenu({
			theme : "metro",
			animationShowDuration : 300,
			animationHideDuration : 200,
			animationShowDelay : 200,
			showTopLevelArrows : false,
			autoOpen : false
		});

		$("#headersettingbar").jqxMenu('setItemOpenDirection', 'loginuser', 'left', 'down');
		$("#headersettingbar").jqxMenu('setItemOpenDirection', 'new_item', 'left', 'down');
		$("#headersettingbar").jqxMenu('setItemOpenDirection', 'admin_board', 'left', 'down');
		$("#headersettingbar").jqxMenu('setItemOpenDirection', 'head_add_fortesting_top', 'left', 'down');
		$("#headersettingbar").css('visibility', 'visible');
	}
	
//	window.onresize = function() {
//		minsized_header_settings_menu();
//         }
	
	function minsized_header_settings_menu() {
		var window_width = window.innerWidth;
		if(window_width<1280)
		{
			$("#headersettingbar").jqxMenu('minimize');
		}
		else
		{
			$("#headersettingbar").jqxMenu('restore');
			
		}
	}

	//清理左右 栏
	function clearLRcolumn() {
		$("#leftContainer").empty();
		$("#middleContainer").empty();

	}
	//save header_menu_status
	save_header_menu_status();
	function save_header_menu_status()
	{
		$("li[name=header_menu_home]").click(function() {
			setCookie("header_menu","header_menu_home",'/home');
		});
		$("li[name=header_menu_test]").click(function() {
			setCookie("header_menu","header_menu_test",'/test');
		});
		$("li[name=header_menu_device]").click(function() {
			setCookie("header_menu","header_menu_device",'/device');
		});
		$("li[name=header_menu_project]").click(function() {
			setCookie("header_menu","header_menu_project",'/project');
		});
		$("li[name=header_menu_interface]").click(function() {
			setCookie("header_menu","header_menu_interface",'/interface');
		});
		
		$("li[name=header_menu_logcat]").click(function() {
			setCookie("header_menu","header_menu_logcat",'/logcat');
		});
		$("li[name=header_menu_ci]").click(function() {
			setCookie("header_menu","header_menu_ci",'/ci');
		});
		
		$("li[name=header_menu_env]").click(function() {
			setCookie("header_menu","header_menu_env",'/env');
		});
		
	}
	
	//show header menu status
	show_header_menu_status();
	function show_header_menu_status()
	{
	  var menu_status_name=getCookie("header_menu");
	  if(menu_status_name)
	  {
	  	$("li[name="+menu_status_name+"]").css({"border-bottom":"2px solid #32be77"});
	  	var color=$("span[name="+menu_status_name+"]").css('color');
	  	$("li[name="+menu_status_name+"] a").css({'color':' #fff'});
	  }
	}
	

//	remove_header_menu_hover_color(".master-page-menu ul li");
//	remove_header_menu_hover_color(".master-page-header-settings ul li");
	function remove_header_menu_hover_color(menu_name)
	{
		$(menu_name).mouseover(function(){
		$(this).css({'background':'rgba(0,0,0,0.05)'});
	});
	
	$(menu_name).mouseout(function(){
		$(this).css({'background':'#FFF'});
	});
	}
	
	//保存cookie
	function setCookie(name, value,path)//两个参数，一个是cookie的名子，一个是值
	{
		var Days = 1;
		//此 cookie 将被保存 30 天
		var exp = new Date();
		//new Date("December 31, 9998");
		exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
		document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString() + ";path="+path;
	}

	//读取cookie
	function getCookie(name)//取cookies函数
	{
		result = null;
		var nameEQ = name + "=";
		var ca = document.cookie.split(';');
		for (var i = 0; i < ca.length; i++) {
			var c = ca[i];
			while (c.charAt(0) == ' ')
			c = c.substring(1, c.length);
			if (c.indexOf(nameEQ) == 0)
				return unescape(c.substring(nameEQ.length, c.length));
		}
		return null;

	}
	
	
	function mousePos(e){
	    e=e||window.event;
	    var scrollX=document.documentElement.scrollLeft||document.body.scrollLeft;//分别兼容ie和chrome
	    var scrollY=document.documentElement.scrollTop||document.body.scrollTop;
	    var x=e.pageX||(e.clientX+scrollX);//兼容火狐和其他浏览器
	    var y=e.pageY||(e.clientY+scrollY);
	    if(x<10)
	    	{
	    	   console.log(x,y);
	    	   var leftBarWidth=$("#leftContainer").css("display");
	    	   if(leftBarWidth=="none")
	    		   {
	    		   $("#mydashboard").show();
	    		   $("#leftContainer").fadeIn(2000);
	    		   $("#contentContainer").css("padding-left","80px");
	    		   }
	    		   
	    	   
	    	}
	    return {x:x,y:y};
	  }
	
	$("#leftbar_hide").click(function(){
		   $("#mydashboard").hide();
		    $("#leftContainer").fadeOut(2000);
		    $("#contentContainer").css("padding-left","0px");
	   });
	
	document.onmousemove = mouseMove;
	function mouseMove(ev){
	 ev = ev || window.event;
	 mousePos(ev);
	}
	
	
	$('[data-toggle="tooltip"]').tooltip();

	// //初始化提示框信
	// function init_notification() {
		// $("#operation_notification").jqxNotification({
			// opacity : 0.8,
			// autoOpen : false,
			// closeOnClick : true,
			// width : 300,
			// autoClose : false,
			// position : 'bottom-right'
		// });
	// }

});
