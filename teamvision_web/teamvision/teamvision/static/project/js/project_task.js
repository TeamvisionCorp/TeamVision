$(document).ready(function() {
	var theme = 'metro';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	var window_height=$(window).height();

	init_page();

	// show_tag_popmenu();

	// select_menu_item();

	// show_calender();

	// click_check();
	
	show_member_popmenu("span[name=task-add-owner]");
	show_member_popmenu("span[name=task_edit_owner]");
	load_owner_task();
	delete_task();
	
	
	// set_progress();
	
	update_task_name();
	
	set_work_hours();
	
	update_task_description();
	
	add_task();
	
	view_more_tasks();
	
	function add_task()
	{
		$("#project_task_add").click(function(){
    	$("#head_add_task").trigger('click');
    });
   }
	
	
	// set_task_tag();
	
	//更新任务描述
	function update_task_description()
	{
		$("#project_task_description").blur(function()
		{
			var loader = $("span[name=loader]");
			loader.show();
			var task_description=$(this).val();
			var task_id=$("#project_task_id").text().trim();
			$.post("/project/task/"+task_id+"/update_property", {
					"Description" : task_description
				}, function(data, status) {
					if (data == "True") {
						loader.hide();
					} else {
						loader.hide();
						init_notification('error', data,true);
					}
				});
		});
	}
	
	
	//更新工时数据
	function set_work_hours()
	{
		$("span[name=task_workhours]").blur(function(){
			var task_id = $(this).parent().parent().find("span[name=task_id]").text().replace('#', '');
			var work_hours=$(this).text();
			update_task_property("WorkHours",work_hours,task_id,true);
		});
	}
	
	
	//更新任务进度
	function update_task_progress(target) {
			var loader = $("span[name=loader]");
			loader.show();
			var task_id = $(target).parent().parent().parent().find("span[name=task_id]").text().replace('#', '');
			var progress_number = $(target).parent().attr("aria-valuenow");
			if (progress_number != "") 
			{
				$.post("/project/task/"+ task_id + "/update_property", {
					"Progress" : progress_number
				}, function(data, status) {
					if (data == "True") {
						loader.hide();
					} else {
						loader.hide();
						init_notification('error', data,true);
					}
				});
			}
			loader.hide();
	}

	function set_progress()
	{
		var progress=0;
		$("span[name=task-progress]").click(function()
		{
			$(this).text("");
		});
		
		$("span[name=task-progress]").blur(function()
		{
			progress=$(this).text();
			$(this).text(progress+"%");
			$(this).parent().css('width',progress+"%");
			console.log(progress);
			$(this).parent().attr("aria-valuenow",progress);
			update_task_progress($(this));
		});
	}
	
	
	function update_task_name()
	{
		$("span[name=project-task_title]").blur(function()
		{
			var task_title=$(this).html().replace("<del>","").replace("</del>","");
			var task_id= $(this).parent().parent().parent().find("span[name=task_id]").text().replace('#', '');
			update_task_property("Title",task_title,task_id,true);
		});
	}
	//更新任务名称
	function update_task_property(key,value,task_id,check_null)
	{
		   var loader = $("span[name=loader]");
			loader.show();
			var is_send=true;
			if(check_null)
			{
				if(value=="")
				{
					is_send=false;
				}
			}
			if(is_send)
			{
			   var parameters={};
			   parameters[key]=value;
			   $.post("/project/task/"+ task_id + "/update_property",parameters
			   , 
			   function(data, status)
			   {
					if (data == "True") {
						loader.hide();
					} else {
						loader.hide();
						init_notification('error', data,true);
					}
			   });
			}
			loader.hide();
	}
	
	//删除任务
	function delete_task() {
		$("span[name=task_delete]").click(function()
		 {
			var task_id = $(this).parent().parent().children("div:eq(0)").find("span[name=task_id]").text().replace('#', '');
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post("/project/task/" + task_id + "/delete", function(data, status) {
					if (data == "True") 
					{
						location = location;
					} else {
						init_notification('error', data,true);
					}
				});
			});
		});

	}
	
	

	function init_page() {
		/*初始化页面元素*/
		$("div[name=project-task-tags]").hide();
		$("div[name=calender]").hide();
		$("div[name=member-list]").hide();
		$("span[name=loader]").hide();
		show_tag_popmenu();
	    select_menu_item();
	    show_calender();
	    set_progress();
	    update_task_name();
	    set_work_hours();
	    click_check();
	    $(".project-task-panel-body-nonbackground").css('max-height',(window_height-250)+"px");
	

	
	update_task_description();
		show_calender("span[name=project_task_deadline_trigger]", "span[name=TDeadLine]");
	}
     
  
     //点击check box 完成任务
	function click_check() {
		// var check_box = $($("div[class=project_task_listview_item_title]").children("div:eq(0)").find("i")[0]);
		var check_box = $("i[name=project-task-check]");
		// var status=1;
		check_box.click(function()
		 {
			var classname = $(this).attr('class');
			if (classname.toUpperCase().indexOf('fa-square-o'.toUpperCase()) >= 0)
			 {
			 	status=1;
				$(this).removeClass('fa-square-o');
				$(this).removeClass('unfinished-check');
				$(this).addClass('finished-check');
				$(this).addClass('fa-check-square');
				var title = $(this).next().text();
				$(this).next().remove();
				$("<del>" + title + "</del>").insertAfter($(this));
			} 
			else 
			{
				status=0;
				$(this).removeClass('finished-check');
				$(this).removeClass('fa-check-square');
				$(this).addClass('fa-square-o');
				$(this).addClass('unfinished-check');
				var title = $(this).next().text();
				$(this).next().remove();
				$("<span contentEditable='true' name='project-task_title'>" + title + "</span>").insertAfter($(this));
			}
			task_complete(status,$(this));
		});
	}
	
	//修改任务状态
	
	function task_complete(status,target)
	{
		var task_id=$(target).parent().parent().parent().find("span[name=task_id]").text().replace('#', '');
		update_task_property("Status",status,task_id,true);
	}

	/*点击元素之外的地方隐藏控件*/
	function hide_control_byclick_page(hide_object, trigger) {

		trigger.click(function(e)
		{
			e.stopPropagation();
		});

		$(document).on('click', function(e) 
		{
			if ($(e.target).html() != hide_object.html() && $(e.target).html()!="" ) {
				hide_object.hide();
			}
		});
	}

	function show_tag_popmenu() {
		$("span[name=add_tag]").click(function() 
		{
			var popmenu = $(this).parent().find("div[name=project-task-tags]");
			// currentoPopObject = popmenu;
			// currentTrigger = $(this);
			popmenu.show();
			popmenu.jqxPanel({
				theme : theme,
				width : 300,
				height : 200
			});
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}

	function select_menu_item() 
	{
		$("input[name=context_search_input]").parent().nextAll().each(function() 
		{
			$(this).click(function(e) 
			{
				e.stopPropagation();
				var labelid = $(this).attr('labelid');
				var text = $(this).text().trim();
				var background = $(this).children("i:eq(1)").css('color');
				var firstChild = $(this).children("i:eq(0)");
				var classname = firstChild.attr('class');
				var item_role=$(this).parent().find("input[name=context_search_input]").attr("role");
				if (classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) 
				{
					firstChild.removeClass('fa-check');
						remove_item($(this),labelid,item_role);
				} 
				else 
				{
					firstChild.addClass('fa-check');
					add_item($(this),labelid,background,text,item_role);
				}
				
				menu_item_change_trigger($(this),item_role);
				 
			});
		});
	}
	
	function menu_item_change_trigger(currentitem,role)
	{
		if(role=="tag-inline")
		{
		   set_task_tag($(currentitem));
		}
		
		if(role=="member-inline")
		{
		   set_task_owner($(currentitem));
		}
	}
	
	function set_task_owner(target)
	{
	   var labelid=""; 
	   $(target).parent().parent().parent().parent().parent().find("span[name=task_edit_owner]").children("span[labelid]").each(function()
	   {
	   	   labelid=labelid+$(this).attr("labelid").trim()+",";
	   });
	   var task_id=$(target).parent().parent().parent().parent().parent().parent().find("span[name=task_id]").text().replace('#', '');
	   update_task_property("Owner",labelid,task_id,true);
	}
   
    function set_task_tag(target)
    {
       var labelid=""; 
	   $(target).parent().parent().parent().parent().parent().children("span[labelid]").each(function()
	   {
	   	   labelid=labelid+$(this).attr("labelid").trim()+",";
	   });
	   var task_id=$(target).parent().parent().parent().parent().parent().parent().find("span[name=task_id]").text().replace('#', '');
	   
	   update_task_property("Tags",labelid,task_id,false);
    }
	
	function add_item(currentitem,labelid,background,text,role)
	{
		if(role=="tag-inline")
	
		{
		   var insertElement = "<span class='label label-default visible-lg-inline-block' labelid='" + labelid + "' style='background-color:" + background + "; opacity:0.5;font-size:8px !important;'>" + text + "</span>";
		   var insertedElement = currentitem.parent().parent().parent().parent().parent().children('span:eq(0)');
		   $(insertElement).insertAfter(insertedElement);	
		}
		else if(role=="tag")
		{
		   var tag_html="<span class='col-sm-12 task_detail_menu_item' labelid="+labelid+"><span class='label label-default' style='background-color:"+background+"; opacity:0.5'><i class='fa fa-tag fa-fw'></i>"+text+"</span></span>";    
		   var insertedElement = $(currentitem).parent().parent().parent().parent().parent();
		   $(tag_html).insertAfter(insertedElement);
		}
		else if(role=="member")
		{
		   var image_src=$(currentitem).children("img:eq(0)").attr("src");
		   var member_html="<span class='col-sm-12 task_detail_menu_item' labelid='"+labelid+"'><img src='"+image_src+"' class='img-circle' style='width:20px;height:20px' title='"+text+"' /></span>";    
		   var insertedElement = $(currentitem).parent().parent().parent().parent().parent();
		   $(member_html).insertAfter(insertedElement);
		}
		else if(role=="member-inline")
		{
		   var image_src=$(currentitem).children("img:eq(0)").attr("src");
		   var member_html="<span labelid="+labelid+"><img src='"+image_src+"' class='img-circle' style='width:30px;height:30px' title='"+text+"' /></span>";    
		   var insertedElement = $(currentitem).parent().parent().parent().parent().parent().find("span[name=task_edit_owner]");
		   insertedElement.append($(member_html));
		}
	}
	
	
	function remove_item(currentitem,labelid,role)
	{
		if(role.indexOf('inline')>=0)
		{
			var removedlabel = $(currentitem).parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
			removedlabel.remove();
		}
		else
		{
			var removedlabel = $(currentitem).parent().parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
			removedlabel.remove();
		}
	}


	function show_calender(trigger, target) {
		$(trigger).click(function() 
		{
			event.stopPropagation();
			var claender=$(this).next();
			claender.show();
		    claender.jqxCalendar({
				theme : 'metro',
				width : '220px',
				height : '220px'
			});
            hide_control_byclick_page(claender, $(this));
			claender.unbind('change').on('change', function(event)
			{
				event.stopPropagation();
				var date = $(this).jqxCalendar('getDate');
				var newDate = new Date(date);
				var selecteddate = newDate.getFullYear() + '-' + (newDate.getMonth() + 1) + '-' + newDate.getDate();
				$(this).parent().find(target).text(selecteddate);
				$(this).hide();
				var task_id=$(this).parent().parent().find("span[name=task_id]").text().replace('#', '');
				update_task_property("DeadLine",selecteddate,task_id,true);
			});
		});

	}
	
	
    function show_member_popmenu(trigger) 
    {
		$(trigger).click(function() {
			var popmenu = $(this).parent().find("div[name=member-list]");
			currentoPopObject = popmenu;
			currentTrigger = $(this);
			popmenu.show();
			popmenu.jqxPanel({
				theme : theme,
				width : 250,
				height : 200
			});
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}
		
    
    function view_more_tasks()
    {
    	$("#project_view_more_task").click(function(){
    		load_more_task($(this));
    	});
    	
    	$("#home_view_more_task").click(function(){
           load_more_task($(this));
    	});
    }
    
    
    function load_more_task(trigger)
    {
    	var task_counts=$(trigger).parent().parent().find(".project_task_listview_item.container-fluid").length;
    	    var sub_nav_action=$("#task_subaction_filter").val();
    	    var owner_id=$("#task_owner_filter").val();
    		$.post(rootUri+"/get_more_task",{"sub_nav_action":sub_nav_action,"owner":owner_id,"start_index":task_counts},function(data,status){
    			$("#project_task_container").append(data);
    			init_page();
    		});
    }
    
    
	function load_owner_task()
	{
	 $(".task_member_filter li").click(function() 
	 {
		 var sub_nav_action=$("#task_subaction_filter").val();
 	    var owner_id=$("#task_owner_filter").val();
 	   $("#project_task_container").load(rootUri+"/owner/"+owner_id,{"sub_nav_action":sub_nav_action,"owner":owner_id,},function(data,status){
 			init_page();
 		});
	 });
	}
    
    
	function init_notification(template,data,autoClose) 
	{		
		$("#operation_notification").jqxNotification({
                width: 250,
                 // position: "bottom-right", 
                 opacity: 0.8,
                autoOpen: false, animationOpenDelay: 300, autoClose: autoClose,
                template:template,
                appendContainer: "#notification_container",
        });
        $("#operation_notification_message").empty();
        $("#operation_notification_message").append(data);
        $("#operation_notification").jqxNotification("open");
	}
});
