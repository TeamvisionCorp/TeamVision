$(document).ready(function() {
	var theme = 'bootstrap';
	var current_Uri = window.location.href;
	var window_height=$(window).height();
	copy_parameter_group();
	init_page();
	load_basic_info_webpart();
	select_menu_item();
	show_ci_task_step_popmenu();
	show_tag_popmenu();
	show_project_filter_popmenu();
	show_ci_tag_filter_popmenu();
	save_task_config();
	copy_task();
	delete_task();
	 start_task_from_proptey_bar();
	clean_task_history();
	show_task_row_operation_group();
	click_plugin_enalbe();
	// start_task_from_config();
	start_task_from_list();
	save_url_to_cookie();
	back_ci_task_entrance_page();
	create_task_parameter();
	delete_parameter_group();
	show_task_parameter_popmenu();
	search_task();
	open_build_log_dalog();
	show_qrcode();
	show_parameter_group_type_menu();
	select_parameter_group_type();
	load_more_tasks();
	load_more_history(-1);
	load_more_changelog();
	load_build_log();
	start_task_from_list_with_parameter();
	select_ci_task_filter_item();
	//初始化task 相关页面
	function init_page() {
		/*初始化页面元素*/
		try {
			$("span[name=loader]").hide();
			$("div[name=project-task-tags]").hide();
			$("div[name=ci-task-plugins]").hide();
			$("div[name=task-parameter-group").hide();
			$("div[name=ci-tag-group").hide();
			$("#ci_deploy_add").unbind('click').click(function() {
				$("#head_add_ci_task").click();
			});
			remove_plugin();
			init_parameter_view_panel();
			try
			{
				$("div[name=ci_plugins]").jqxSortable();
				init_case_filter();
			}
			catch(e)
			{
				console.log(e);
			}
			
			init_dropdown_list("ci_credentials");
			init_dropdown_list("git_check_out_strategy");
			init_dropdown_list("svn_check_out_strategy");
			init_dropdown_list("build_tool_jdk");
			init_dropdown_list("build_tool_gradle");
			init_dropdown_list("build_tool_xcode");
			init_dropdown_list("build_tool_pods");
			init_dropdown_list("deploy_server");
            init_dropdown_list("deploy_service");
			init_dropdown_list("ci_task_parameter_group");
			init_dropdown_list("auto_tool_jdk");
			init_dropdown_list("auto_host_info");
			$("#ci_task_container").css('max-height',(window_height-250)+"px");
			$("#task_history_container").css('max-height',(window_height-250)+"px");
			$(".doraemon_wizard_column_items").css('max-height',(window_height-250)+"px");
		} catch(e) {
			console.log(e);
		}
	}
	
	scroll_bottom_load_task();
	function scroll_bottom_load_task()
	{
		$("#ci_task_container").scroll(function(){
		    var taskContainerHeight = $(this).height();
		    var containerScrollHeight = $(this)[0].scrollHeight;
		    var containerScrollTop = $(this)[0].scrollTop; 
		    if(containerScrollTop + taskContainerHeight >=containerScrollHeight-40) 
		    {
		      var task_items=$(".ci_task_listview_item");
		    	  if(containerScrollHeight<=840 ||task_items.length>=10)
		    	{
		    		  load_more_tasks();  
		    	}
		    }
		  });
		
	}


	function ajax_init_function() {
		init_page();
		show_tag_popmenu();
		copy_task();
		delete_task();
		show_task_row_operation_group();
		select_menu_item();
		start_task_from_list();
//		show_build_button();
		show_package_download_controll();
		popmenu_search();
		open_build_log_dalog();
		show_task_parameter_popmenu();
		start_task_from_list_with_parameter();
	}
	
	//search task
	function search_task()
	{
		$("#task_search_keyword").keyup(function(e){
			var keyword=$(this).val().trim();
			if(keyword=="")
			{
				keyword="all";
			}
			if(e.keyCode==13)
			{
			  var task_type=$("#task_type_id").val();
			  if(task_type=="")
			  {
			  	task_type=0;
			  }
			  var product_id=$("#task_product_id").val();
			  if(product_id=="")
			  {
			  	product_id='all';
			  }
			  load_task_with_filter();
			}
		});
	}
	
	//get more tasks by click view more task link
	
	function load_more_tasks()
	{
		try
		{
			var keyword=$("#task_search_keyword").val().trim();
			if(keyword=="")
			{
				keyword="all";
			}
			var page_size=$("#ci_task_container").children().length;
			$.post("/ci/dashboard/more_tasks",{"page_size":page_size,'keyword':keyword},function(data,status){
				$("#ci_task_container").append(data);
				ajax_init_function();
			});
		}
		catch(e)
		{
			console.log(e);
		}
			
	}
	
	
		//get more history by click view more history link
	
	function load_more_history(start_index)
	{
		$("#ci_view_more_history").click(function(){
			var ci_task_id = $("#ci_task_id").val();
			var page_size=$("#task_history_container").children().length;
			if(start_index!=-1)
			{
				page_size=start_index;
			}
			$.post("/ci/task/"+ci_task_id+"/more_history",{"page_size":page_size},function(data,status){
				$("#task_history_container").append(data);
				ajax_init_function();
			});
		});
	}
	
	
	
		//get more changelog by click view more changlog link
	function load_more_changelog()
	{
		$("#ci_view_more_changelog").click(function(){
			var ci_task_id = $("#ci_task_id").val();
			var page_size=$("#task_changelog_container").children().length;
			$.post("/ci/task/"+ci_task_id+"/more_changelog",{"page_size":page_size},function(data,status){
				$("#task_changelog_container").append(data);
				 expand_changelog_byclick();
		         click_build_log_content();
			});
		});
	}
	
	//show qrcode image
	function show_qrcode()
	{
		$(".list-group-item").mouseover(function(){
			var qrcode_url=$(this).attr('qrcode_uri');
			if(qrcode_url)
			{
			  var qr_code_container=$(this).parent().parent().parent().find("div[name=qrcode_image]");
			  var img_src="/ci/history/download_package/qrcode?content="+qrcode_url;
			  $(qr_code_container).find("img[name=qrcode_img]").attr('src',img_src);
			  $(qr_code_container).show();
			}
			
		});
		$(".list-group-item").mouseout(function(){
			$(this).parent().parent().parent().find("div[name=qrcode_image]").hide();
		});
	}

	//copy task
	function copy_task() {
		$("span[name=task_copy]").click(function() {
			var ci_task_id = $($(this).parent().parent().parent().parent().find("span[name=ci_task_id]")[0]).text().replace('#', '');
			var sub_nav_action_index = window.location.href.lastIndexOf('/');
			var sub_nav_action = window.location.href.substring(sub_nav_action_index + 1).replace('#', "");
			$.get("/ci/task/copy/" + ci_task_id, function(data, status) {
				if (data == "True") {
					$("#ci_task_container").load("/ci/task/get_task_list", {
						"task_id" : ci_task_id,
						"sub_nav_action" : sub_nav_action
					}, function(data, status) {
						ajax_init_function();
					});
				} else {
					init_notification('error', data, true);
				}
			});
		});
	}

	//delete task
	function delete_task() {
		$("span[name=task_delete]").click(function() {
			var ci_task_id = $("#ci_task_id").val();
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.get("/ci/task/delete/" + ci_task_id, function(data, status) {
					if (data == "True") {
						$("span[name=ci_task_back]").click();
					} else {
						init_notification('error', data, true);
					}
				});
			});
		});
	}
	
	
	//clean task history
	function clean_task_history() {
		$("span[name=workspace_clean]").click(function() {
			var ci_task_id = $("#ci_task_id").val();
			$("#popup-dialog-container").load("/ci/task/confirm_dialog",function(){
			$("#task_history_clean_confirm").modal('show');
			$("#task_history_clean_confirm_button").click(function() {
				$("#task_history_clean_confirm").modal('hide');
				
				$.get("/ci/task/clean_history/" + ci_task_id, function(data, status) {
					if (data == "True") {
						load_more_history(0);
					} else {
						init_notification('error', data, true);
					}
				});
			});
		});
	});
	}

	function start_task_from_proptey_bar() {
		$("span[name=build_confirm]").click(function() {
			var ci_task_id = $("#ci_task_id").val();
			var form_serialize=$("#ci_task_build_confim_form").serialize();
			var parameter_group_id=form_serialize.split('=')[1];
			start_task(ci_task_id,parameter_group_id);
		});
	}

	function start_task_from_list() {
		$("span[name=build_task]").unbind('click').click(function() {
			var ci_task_id = $($(this).parent().parent().parent().find("span[name=ci_task_id]")[0]).text().replace('#', '');
			start_task(ci_task_id,"");
		});

	}
	
	
	function load_build_log()
	{
		var file_id=$("#build_log_file_id").val();
		$("#build_log_container").load("/ci/history/log_content/"+file_id,function(){
			$("#build_log_loader").hide();
		});
	}
	
	function start_task_from_list_with_parameter() {
		$("span[name=confirm_build_withparameter]").unbind('click').click(function() {
			var ci_task_id = $($(this).parent().parent().parent().parent().parent().parent().find("span[name=ci_task_id]")[0]).text().replace('#', '');
			var parameter_id="";
			$(this).parent().find('li').each(function(){
				var i_child=$(this).children("i:eq(0)");
				if(i_child.hasClass('fa-check'))
				{
					parameter_id=$(this).attr('labelid');
				}
			});
			start_task(ci_task_id,parameter_id);
		});

	}

	//start task
	function start_task(ci_task_id,parameter_group_id) {
		$.post("/ci/task/" + ci_task_id+"/start",{"parameter_group_id":parameter_group_id}, function(data, status) {
			if (data == "False") {
				init_notification('error', data, true);
			} else {
				init_notification('success',"构建命令已经发出，请耐心等待！", true);
			}
		});

	}
	
	
	//刷线任务队列
	function refresh_tq_list() {
		$("#ci_dashboard_taskqueue_container").load("/ci/dashboard/tq_list", function() {
			cancel_tq();
		});
	}
	
	function cancel_tq() {
		$("span[name=tq_stop]").unbind('click').click(function() {
			var tq_uuid = $($(this).parent().parent().parent().find("span[name=tq_uuid]")[0]).text();
			var ci_task_id = $($(this).parent().parent().parent().find("span[name=task_id]")[0]).text();
			stop_task_request(ci_task_id, tq_uuid);
		});
	}

	function cancel_task() {
		$("span[name=task_stop]").click(function() {
			var tq_uuid = $($(this).parent().find("span[name=tq_uuid]")[0]).text();
			var ci_task_id = $($(this).parent().parent().parent().find("span[name=task_id]")[0]).text();
			stop_task_request(ci_task_id, tq_uuid);
		});
	}

	function stop_task_request(ci_task_id, tq_uuid) {
		$.post("/ci/task/stop/" + ci_task_id, {
			"task_uuid" : tq_uuid
		}, function(data, status) {
			if (data == "False") {
				init_notification('error', data, true);
			} else {
				init_notification('success', "任务取消指令已经下发！", true);
			}

		});

	}
	
	//mouse over on task list view,show build button
//	show_build_button();
	function show_build_button()
	{
		$(".ci_task_listview_item").mouseover(function(){
			$(this).find("span[name=build_task]").show();
			$(this).find("span[name=build_with_parameter]").show();
		});
		$(".ci_task_listview_item").mouseout(function(){
			$(this).find("span[name=build_task]").hide();
			$(this).find("span[name=build_with_parameter]").hide();
		});
	}
	

	/*load basic info*/
	function load_basic_info_webpart() {
		try {
			var task_id = $("#ci_task_id").val();
			$.get("/ci/task/" + task_id + "/task_config_basic", function(data, status) {
				$("#ci_task_info_item").append(data);
				init_basic_controll();
				$("#ci_task_trigger_timer").click(function(){
				$("#time_trigger").val("");
				});
				// $('textarea').height(this.scrollHeight);
				change_textarea_height();
			});
		} catch(e) {
			console.log(e);
		}

	}
	
	//textarea 获得焦点，输入回车高度自动扩展
	
	function change_textarea_height()
	{
		$('textarea').focus(function () { $(this).height(this.scrollHeight);});
		$('textarea').keydown(function (event) {
			if(event.keyCode==13)
				{
				$(this).height(this.scrollHeight);
				}
			
		});
		
	}

	//task row operation
	function show_task_row_operation_group() {
		$("a[name=ci_task_operation]").click(function() {
			$(this).parent().find("span[name=ci_task_operation_group]").fadeToggle(300);
		});
	}

	//show task tag menu
	function show_tag_popmenu() {
		$("span[name=add_tag]").click(function() {
			var popmenu = $(this).parent().find("div[name=project-task-tags]");
			// currentoPopObject = popmenu;
			// currentTrigger = $(this);
			popmenu.show();
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}
	
	//show project filter menu
	function show_project_filter_popmenu() {
		$("span[name=project_filter_down_arrow]").click(function() {
			var popmenu = $(this).parent().find("div[name=project-group]");
			// currentoPopObject = popmenu;
			// currentTrigger = $(this);
			popmenu.show();
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}
	
	//show ci_tag filter menu
	function show_ci_tag_filter_popmenu() {
		$("span[name=tag_filter_down_arrow]").click(function() {
			var popmenu = $(this).parent().find("div[name=ci-tag-group]");
			// currentoPopObject = popmenu;
			// currentTrigger = $(this);
			popmenu.show();
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}
	
	//show task parameter group menu
	function show_task_parameter_popmenu() {
		$("span[name=build_with_parameter]").click(function() {
			var popmenu = $(this).parent().find("div[name=task-parameter-group]");
			// currentoPopObject = popmenu;
			// currentTrigger = $(this);
			popmenu.show();
			popmenu.jqxPanel({
				theme : theme,
				width : 300,
				height :200,
			});
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}

	//初始化配置基本信息页Jquery 控件
	function init_basic_controll() {
		try {
			$("#ci_basic_info_items").jqxSortable();
			init_combo_box("ci_task_project", false);
			init_combo_box("ci_agent_select", false);

			init_agent_conditions_combobox();
			
			init_combo_box("DeployService", false);
		} catch(e) {
			console.log(e);
		}

	}

	//初始化agent 过滤条件选择框
	function init_agent_conditions_combobox() {
		var select_items = Array();
		var index = 0;
		$("#ci_agent_condations option").each(function() {
			if ($(this).attr("selected") == "selected") {
				select_items.push(index);
			}
			index = index + 1;
		});

		$("#ci_agent_condations").jqxComboBox({
			theme : theme,
			width : 300,
			height : 33,
			multiSelect : true,
			autoComplete : true,
			searchMode : 'containsignorecase'
		});

		for (var i = 0; i < select_items.length; i++) {
			$("#ci_agent_condations").jqxComboBox('selectIndex', select_items[i]);
		}
	}
     
	//初始化用例过滤过滤条件选择框
	function init_case_filter()
	{
		$("select[name=autocase_filter]").each(function(index,item){
			var form_id=$(item).parent().parent().parent().attr('id');
			init_case_filter_combobox(form_id);
		});
	}
	
	
	function init_case_filter_combobox(form_id) {
		var select_items = Array();
		var index = 0;
		
		$("#"+form_id+" select[name=autocase_filter] option").each(function() {
			if ($(this).attr("selected") == "selected") {
				select_items.push(index);
			}
			index = index + 1;
		});

		$("#"+form_id+" select[name=autocase_filter]").jqxDropDownList({
			theme : theme,
			width : 300,
			height : 33,
			checkboxes:true
		});

		for (var i = 0; i < select_items.length; i++) {
			$("#"+form_id+" select[name=autocase_filter]").jqxDropDownList('checkIndex', select_items[i]);
		}
	}

	
	 
	// 弹出CI Step菜单
	function show_ci_task_step_popmenu() {
		$("span[name=add_ci_plugin]").click(function() {
			var popmenu = $(this).parent().find("div[name=ci-task-plugins]");
			// currentoPopObject = popmenu;
			// currentTrigger = $(this);
			popmenu.show();
			popmenu.jqxPanel({
				theme : theme,
				width : 200,
				height : 300
			});
			popmenu.addClass("ci-task-config-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});
	}
	
	

	function select_menu_item() {
		$("input[name=context_search_input]").parent().nextAll().each(function() {
			$(this).unbind('click').click(function(e) {
				e.stopPropagation();
				var labelid = $(this).attr('labelid');
				var text = $(this).text().trim();
				var background = $(this).children("i:eq(1)").css('color');
				var firstChild = $(this).children("i:eq(0)");
				var classname = firstChild.attr('class');
				var item_role = $(this).parent().find("input[name=context_search_input]").attr("role");
				if (classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) {
					firstChild.removeClass('fa-check');
					remove_item($(this), labelid, item_role);
				}
				else 
				{
					if(item_role!="task-parameter")
					{
					  firstChild.addClass('fa-check');
					  add_item($(this), labelid, background, text, item_role);	
					}
					else
					{
						firstChild.addClass('fa-check');
						uncheck_task_parameter_item(this);
					}
				}
				menu_item_change_trigger($(this), item_role);
			});
		});
	}
	
	
	function select_ci_task_filter_item() {
		$("input[name=ci_task_filter_search_input]").parent().nextAll().each(function() {
			$(this).click(function(e) {
				e.stopPropagation();
				var labelid = $(this).attr('labelid');
				var text = $(this).text().trim();
				var background = $(this).children("i:eq(1)").css('color');
				var firstChild = $(this).children("i:eq(0)");
				var classname = firstChild.attr('class');
				var item_role = $(this).parent().find("input[name=ci_task_filter_search_input]").attr("role");
				console.log(labelid);
				if (classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) {
					firstChild.removeClass('fa-check');
					remove_item($(this), labelid, item_role);
				}
				else 
				{
					if(item_role!="task-parameter")
					{
					  firstChild.addClass('fa-check');
					  add_item($(this), labelid, background, text, item_role);	
					}else{
						firstChild.addClass('fa-check');
						uncheck_task_parameter_item(this);
					}
				}
				ci_task_filter_item_change_trigger($(this), item_role);

			});
		});
	}

    function uncheck_task_parameter_item(target)
    {
    	$(target).siblings().each(function(){
    	var firstChild = $(this).children("i:eq(0)");
    	firstChild.removeClass('fa-check');
    	});
    }

	function menu_item_change_trigger(currentitem, role) {
		if (role == "ci-task-tag-inline") {
			set_task_tag($(currentitem));
		}
		
		if (role == "ci-history-tag-inline") {
			set_history_tag($(currentitem));
		}

		if (role == 'ci-plugin') {
			set_ci_plugin($(currentitem));
		}
		
		
	}
	
	function ci_task_filter_item_change_trigger(currentitem, role) {
		
		if (role == 'project-filter') {
			set_ci_task_project_filter($(currentitem));
		}
		
		if (role == 'ci-tag-filter') {
			set_ci_task_tag_filter($(currentitem));
		}
	}

	function set_ci_plugin(target) {
		var plugin_container = $(target).parent().parent().parent().parent().parent().parent().parent().find("div[name=ci_plugins]");
		var plugin_id = $(target).attr('labelid');
		var ci_task_id = $("#ci_task_id").val();
		$.get("/ci/plugin/2/get_plugin", {
			"plugin_id" : plugin_id,
			"task_id" : ci_task_id
		}, function(data, status) {
			//
			$(plugin_container).append(data);
			$(plugin_container).jqxSortable();
			remove_plugin(plugin_container);
			$(plugin_container).jqxSortable('refresh');
			click_plugin_enalbe();
			init_page();
			change_textarea_height();
			set_outputs_option();

		});
		var popmenu = $(this).parent().parent().parent().parent();
		popmenu.hide();
	}

	//设置构建产物是否上传，以及构建目录是否清理
	set_outputs_option();
	function set_outputs_option()
	{
		var outputs_value_before="";
		$("input[method=outputs_target_path]").click(function(){
			outputs_value_before=$(this).val().trim();
		});
		
		$("input[method=outputs_target_path]").blur(function(){
			var outputs_value_after=$(this).val().trim();
			if(outputs_value_before!=outputs_value_after)
				{
				   if(outputs_value_after!="")
					   {
					      $(this).parent().parent().parent().find("input[name=is_upload_file]").attr("checked","true");
					      $(this).parent().parent().parent().find("input[name=is_clean_outputs]").attr("checked","true");
					   }
				}
			
		});
	}
	
	
	function remove_plugin() {
		$("i[name=plugin_close]").click(function() {
			var plugin_element = $(this).parent().parent().parent().parent().parent();
			plugin_element.remove();
		});
	}
	
	
	function set_ci_task_project_filter(target) {
		var labelid = "";
		var project_name = "项目";
		$(target).parent().children("li[labelid]").each(function(index,item) {
			var if_checked=$(this).find("i:eq(0)").hasClass('fa-check');
		    if(if_checked)
		    	{
		    	  labelid = labelid + $(this).attr("labelid").trim() + ",";
		    	  project_name=$(this).text().trim();
		    	  console.log(project_name);
		    	}
		});
		if(project_name.length>4)
		{
			project_name=project_name.substr(0,4)+"... ";
		}
		$("span[name=project_filter_down_arrow]").attr("select_project",labelid);
		$("span[name=project_filter_name]").text(project_name);
		load_task_with_filter();
	}
	
	
	function set_ci_task_tag_filter(target) {
		var labelid = "";
		var tag_name = "标签";
		var select_item_i="";
		$(target).parent().children("li[labelid]").each(function(index,item) {
			var if_checked=$(this).find("i:eq(0)").hasClass('fa-check');
		    if(if_checked)
		    	{
		    	  labelid = labelid + $(this).attr("labelid").trim() + ",";
		    	  tag_name=$(this).text().trim();
		    	  select_item_color=$(this).find("i:eq(1)").css('color');
		    	  select_item_i=select_item_i+"<i title=\""+tag_name+"  \" style=\"color:"+select_item_color+" \" class=\"fa fa-square fa-fw fa-lg\"></i>";
		    	  console.log(tag_name);
		    	}
		});
		if(tag_name.length>4)
		{
			tag_name=tag_name.substr(0,4)+"... ";
		}
		$("span[name=tag_filter_down_arrow]").attr("select_tag",labelid);
		$("span[name=tag_filter_icon]").empty();
		$("span[name=tag_filter_icon]").append(select_item_i);
//		$("span[name=tag_filter_name]").text(tag_name);
		load_task_with_filter();
	}
	
	
	function load_task_with_filter()
	{
		var search_keyword=$("#task_search_keyword").val().trim();
		var project_ids=$("span[name=project_filter_down_arrow]").attr("select_project");
		var tag_ids=$("span[name=tag_filter_down_arrow]").attr("select_tag");
		$("#ci_task_container").load("/ci/dashboard/more_tasks",{"tag_id":tag_ids,"project_id":project_ids,'keyword':search_keyword},function(data,status){
			ajax_init_function();
		});
		
	}

	function set_task_tag(target) {
		var labelid = "";
		$(target).parent().parent().parent().children("span[labelid]").each(function() {
			labelid = labelid + $(this).attr("labelid").trim() + ",";
		});
		var task_id = $(target).parent().parent().parent().parent().find("span[name=ci_task_id]").text().replace('#', '');
		update_task_property("Tags", labelid, task_id, false);
	}
	
	function set_history_tag(target) {
		var labelid = "";
		$(target).parent().parent().parent().children("span[labelid]").each(function() {
			labelid = labelid + $(this).attr("labelid").trim() + ",";
		});
		var history_id = $(target).parent().parent().parent().parent().find("input[name=task_history_id]").val();
		if(history_id==null){
			history_id = $(target).parent().parent().parent().parent().parent().parent().parent().parent().find("input[name=task_history_id]").val();
		}
		update_history_property("Tags",labelid, history_id, false);
	}

	//更新任务名称
	function update_task_property(key, value, task_id, check_null) {
		var loader = $("span[name=loader]");
		loader.show();
		var parameters = {};
		parameters[key] = value;
		$.post("/ci/task/" + task_id + "/update_property", parameters, function(data, status) {
			if (data == "True") {
			} else {
				init_notification('error', data, true);
			}
		});

		loader.hide();
	}
	
	//更新任务名称
	function update_history_property(key,value, history_id, check_null) {
		var loader = $("span[name=loader]");
		loader.show();
		var parameters = {};
		parameters[key] = value;
		$.ajax({
			type: "PATCH",
			url : "/api/ci/task_history/"+history_id+"/",
			data:parameters,
			dataType:"application/json",
			success:function(data)
			{
				if (data == "True") {
			} else {
				init_notification('error', data, true);
			}
			}
		});

		loader.hide();
	}


	function add_item(currentitem, labelid, background, text, role) {
		if (role == "ci-task-tag-inline") {
			var insertElement = "<span class='label label-default visible-lg-inline-block' labelid='" + labelid + "' style='background-color:" + background + "; opacity:0.5;font-size:8px !important;'>" + text + "</span>";
			var insertedElement = currentitem.parent().parent().parent().children('span:eq(0)');
			$(insertElement).insertAfter(insertedElement);
		}
		if (role == "ci-history-tag-inline") {
			var insertElement = "<span class='label label-default visible-lg-inline-block' labelid='" + labelid + "' style='background-color:" + background + "; opacity:0.5;font-size:8px !important;'>" + text + "</span>";
			var insertedElement = currentitem.parent().parent().parent().children('span:eq(0)');
			$(insertElement).insertAfter(insertedElement);
		}
	}

	function remove_item(currentitem, labelid, role) {
		if (role.indexOf('inline') >= 0) {
			var removedlabel = $(currentitem).parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
			removedlabel.remove();
		} else {
			var removedlabel = $(currentitem).parent().parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
			removedlabel.remove();
		}
	}

	//save task config

	function save_task_config() {
		send_config_sections("ci_post_build_save_button", "ci_post_build_items");
		send_config_sections("ci_build_save_button", "ci_build_items");
		send_config_sections("ci_scm_save_button", "ci_scm_items");
		send_config_sections("ci_pre_build_save_button", "ci_pre_build_items");
		send_config_sections("ci_basic_info_save_button", "ci_basic_info_items");
	}

	//send config section
	function send_config_sections(trigger_id, section_id) {
		$("#" + trigger_id).click(function() {
			var section_config_data = get_section_config(section_id);
			var ci_task_id = $("#ci_task_id").val();
			$.ajax({
				url : "/ci/task/" + ci_task_id + "/config/save_task_config",
				type : "post",
				dataType : "json",
				data : {
					section : section_config_data
				},
				complete : function(data) {
					if (data == "False") {
						init_notification('error', data, true);
					} else {
						init_notification('success', "任务配置已经成功保存", true);
					}
				}
			});
		});

	}

	//get section config

	function get_section_config(section_id) {
		var widgetIdsSerialized = $("#" + section_id).jqxSortable("serialize", {key:"ci_plugin"});
		var section_name = $("#" + section_id).parent().parent().attr('section_name');
		result = {};
		var temp_array = new Array();
		ids = widgetIdsSerialized.split('&');
		for ( i = 0; i < ids.length; i++) {
			var data = {};
			var id = ids[i].replace("=", "_");
			var jsonuserinfo = $("#" + id).find("form:eq(0)").serializeArray();
			data["parameter"] = jsonuserinfo;
			data["order"] = i;
			data["is_enable"] = $("#" + id).find("span[name=ci_plugin_enabled]:eq(0)").text();
			data["plugin_id"] = $("#" + id).attr('plugin_id');
			if (section_id == "ci_basic_info_items") {
				for ( j = 0; j < data['parameter'].length; j++) {
					if (data['parameter'][j]['name'] == 'agent_condations') {
						data['parameter'][j]['value'] = get_basic_agent_filter_condations();
						break;
					}
				}

			}
			for ( j = 0; j < data['parameter'].length; j++) {
				if (data['parameter'][j]['name'] == 'autocase_filter') {
					data['parameter'][j]['value'] = get_basic_case_filter_condations(id);
					break;
				}
			}
			temp_array[i] = data;
		}
		result[section_name] = temp_array;
		return JSON.stringify(result);
	}

	function get_basic_agent_filter_condations() {
		var items = $("#ci_agent_condations").jqxComboBox('getSelectedItems');
		var str = "";
		for (var i = 0; i < items.length; i++) {
			str += items[i].value + ",";
		}
		return str;
	}
	
	
	function get_basic_case_filter_condations(id) {
		var items = $("#"+id+" select[name=autocase_filter").jqxDropDownList('getCheckedItems');
		var str = "";
		for (var i = 0; i < items.length; i++) {
			str += items[i].value + ",";
		}
		return str;
	}


	/*点击元素之外的地方隐藏控件*/
	function hide_control_byclick_page(hide_object, trigger) {

		trigger.click(function(e) {
			e.stopPropagation();
		});

		$(document).on('click', function(e) {
			if ($(e.target).html() != hide_object.html() && $(e.target).html() != "") {
				hide_object.hide();
			}
		});
	}

	//enlable plugin
	function click_plugin_enalbe() {
		$("span[name=ci_plugin_enabled]").click(function() {
			if ($(this).text() == "On") {
				$(this).text("Off");
				$(this).css("background", "gray");
			} else {
				$(this).text("On");
				$(this).css("background", "green");
			}
		});
	}

	show_package_download_controll();
	function show_package_download_controll() {
		$("span[name=down_package]").click(function() {
			var history_id = $(this).parent().parent().parent().find("input[name=task_history_id]").val().trim();
			var package_list_container = $(this).parent().parent().find("div[name=ci_task_download_package]");
			var package_list_url="/ci/history/"+history_id.toString()+"/package_list";
			$(package_list_container).load(package_list_url, function() {
				$(package_list_container).show();
				popmenu_search();
				hide_control_byclick_page(package_list_container, $(this));
				show_qrcode();
			});
		});
	}

	change_wirzard_column_width();
	function change_wirzard_column_width() {
		var widths = $("#doraemon_wirzrd").width();
		$(".doraemon_wizard_column_expanded").each(function() {

			if (!$(this).hasClass("hide_wizard_expanded")) {
				$(this).width(widths);
			}

		});
	}

	//添加任务参数组
	function create_task_parameter() {
		$("#task_add_parameter_group").keydown(function(e) {
			if (e.keyCode == 13) {
				var task_id =$("#ci_task_id").val();
				var group_name = $(this).val();
				var group_type=get_parameter_group_type();
				$.post("/ci/task/" + task_id + "/parameter_group/create", {
					'group_name' : group_name,
					'group_type':group_type
				}, function(data, status) {
					if (data == "True") {
						$("#task_parameter_groups").load("/ci/task/" + task_id + "/parameter_group/list", function() {
							view_task_parameter();
							delete_parameter_group();
							copy_parameter_group();
							$($("div[name=task_parameter_group_row]")[0]).click();
							change_textarea_height();
						});
					}
				});
			}

		});
	}
	
	//获取参数组type
	function get_parameter_group_type()
	{
		var group_type=2;
		$("#parameter_group_type_menu").find("i").each(function(){
			if($(this).hasClass('selected'))
				{
				  group_type=$(this).attr('type');
				}
		});
		return group_type;
	}
	
	
	//显示参数组类型选择下拉框
	function show_parameter_group_type_menu()
	{
		$("#parameter_group_settings").mouseover(function(){
			var group_type_menu=$("#parameter_group_type_menu")
		   $(group_type_menu).show();
		   hide_control_byclick_page(group_type_menu,group_type_menu);
		});
	}
	
	//选择参数组类型
	function select_parameter_group_type()
	{
		$(".option-item").click(function(){
	     $(".option-item .selected").removeClass("selected");
	     $(this).find("i").addClass("selected");
		});
	}

	//加载当前任务参数组列表

	function load_task_parameter_group_list() {
		var task_id =$("#ci_task_id").val();
		$("#task_parameter_groups").load("/ci/task/" + task_id + "/parameter_group/list", function() {
			view_task_parameter();
			delete_parameter_group();
			copy_parameter_group();
		});
	}

    //input,textarea 等输入框获得焦点显示边框
	function show_border_onfocus()
	{
		$("input").mouseover(function(input_element){
			  $(this).removeClass("input-2-label");	
		});
		$("input").mouseout(function(){
			if($(this).hasClass("display-input"))
			{
			  $(this).addClass("input-2-label");
			}
				
		});
		$("textarea").mouseover(function(input_element){
	      $(this).removeClass("input-2-label");	
		});
		$("textarea").mouseout(function(){
			if($(this).hasClass("display-input"))
			{
			  $(this).addClass("input-2-label");
			}
		});
		
	}



	view_task_parameter();

	//查看编辑任务参数组
	function view_task_parameter() {
		$("div[name=task_parameter_group_row]").click(function() {
			var parameter_id = $(this).find("span[name=task_parameter_id]").text();
			$(this).siblings().each(function(i, item) {
				$(item).removeClass("parameter-group-selected");
			});
			$(this).addClass("parameter-group-selected");
			$("#task_parameter_group_list").removeClass('col-sm-12');
			$("#task_parameter_group_list").addClass('col-sm-6');
			$("#task_parameter_group_edit").load("/ci/task/parameter_group/edit", {
				"parameter_id" : parameter_id
			}, function() {
				add_task_parameter();
				remove_task_parameter();
				save_task_parameter();
				set_parameter_group_default();
				set_parameter_group_plugin_setting();
				set_plugin_enable_inparameter_group();
				close_parameter_edit_webpart();
				show_border_onfocus();
				change_textarea_height();
				lock_task_parameter();
				unlock_task_parameter();
				init_parameter_view_panel();
				$("div[name=parameter_value]").mouseover(function() {
					$(this).addClass("parameter-value-container-mouseover");
				});
				$("div[name=parameter_value]").mouseout(function() {
					$(this).removeClass("parameter-value-container-mouseover");
				});
			});
			$("#task_parameter_group_edit").show();

		});
	}
	

	//删除任务参数组

	function delete_parameter_group() {
		$("span[name=delete_parameter_group]").click(function(e) 
		{
			var group_id = $(this).parent().parent().find("span[name=task_parameter_id]").text();
			$.post("/ci/task/parameter_group/delete", {
				'group_id' : group_id
			}, function() {
				load_task_parameter_group_list();
			});
			e.stopPropagation();
		});
	}

	//复制任务参数组

	function copy_parameter_group() {
		$("span[name=copy_parameter_group]").click(function(e) {
			var group_id = $(this).parent().parent().find("span[name=task_parameter_id]").text();
			$.post("/ci/task/parameter_group/copy", {
				'group_id' : group_id
			}, function() {
				load_task_parameter_group_list();
			});
			e.stopPropagation();
		});
	}

	//添加参数到任务参数组
	function add_task_parameter() {
		$("#add_task_parameter").click(function() {
			$.get("/ci/task/parameter/keyvalue_controll", function(data, status) {
				$("#task_parameter_value_container").prepend(data);
				remove_task_parameter();
				$("div[name=parameter_value]").mouseover(function() {
					$(this).addClass("parameter-value-container-mouseover");
				});
				$("div[name=parameter_value]").mouseout(function() {
					$(this).removeClass("parameter-value-container-mouseover");
				});
				change_textarea_height();
			});
		});
	}

	//从参数组删除任务参数
	function remove_task_parameter() {
		$("i[name=parameter_delete").click(function() {
			$(this).parent().parent().remove();
		});
	}
	
	//设置发布参数组所有值为只读
	function lock_task_parameter() {
		var group_type=$("label[name=group_type]").attr("value").trim();
		if(group_type=="1")
			{
			  $("i[name=parameter_lock]").show();
			  
			  $("#task_parameter_value_container input[name=key]").attr("readonly","readonly");
			  $("#task_parameter_value_container input[name=key]").addClass("readlony-background");
			  $("#task_parameter_value_container textarea[name=value]").addClass("readlony-background");
			  $("#task_parameter_value_container textarea[name=value]").attr("readonly","readonly");
			}
	}
	
	//设置发布参数组所有值为只读
	function unlock_task_parameter() {
       $("i[name=parameter_lock]").click(function(){
    	     if($(this).hasClass("fa-lock"))
    	    	 {
    	    	      $(this).parent().parent().find("input[name=key]").removeAttr("readonly");
    		      $(this).parent().parent().find("textarea[name=value]").removeAttr("readonly"); 
    		      $(this).removeClass("fa-lock");
    		      $(this).addClass("fa-unlock");
    	    	 }
    	     else
    	    	 {
    	    	 $(this).parent().parent().find("input[name=key]").attr("readonly","readonly");
    		      $(this).parent().parent().find("textarea[name=value]").attr("readonly","readonly");
    		      $(this).removeClass("fa-unlock");
    		      $(this).addClass("fa-lock");
    		      $("#task_parameter_value_container input[name=key]").addClass("readlony-background");
    			  $("#task_parameter_value_container textarea[name=value]").addClass("readlony-background");
    	    	 }
	   });
	}

//	//保存任务参数组修改
//	function save_task_parameter() {
//		$("#save_task_parameter").click(function() {
//			
//		});
//	}
	
	
	//保存任务参数组修改
	function save_task_parameter()
	{
		$("#save_task_parameter").click(function() {
			var task_id=$("#ci_task_id").val();
			var group_id=$("input[name=group_id]").val();
			$("#popup-dialog-container").load("/ci/task/parameter_group/confirm_dialog",$('#task_parameter_group_form').serialize(),function(){
				$("#parameter_group_confirm").modal('show');
				$("#parameter_group_confirm_button").click(function(){
					$("#parameter_group_confirm").modal('hide');
					$.post("/ci/task/parameter_group/save", $('#task_parameter_group_form').serialize(), function(data,status) {
						if (data == "True") {
							init_notification('success',"参数组修改保存成功！", true);
							load_task_parameter_group_list();
						} else {
							init_notification('error',"参数组修改保存失败！", true);
						}
			
					});
				});
			});
		});
	}
	

	//设置任务参数组默认属性
	function set_parameter_group_default() {
		$("#task_parameter_group_default").click(function() {
			var is_default = $(this).attr('isdefault');
			if (is_default | is_default == "True") {
				$(this).attr('isdefault', "False");
				$(this).removeClass("fa-toggle-on");
				$(this).addClass("fa-toggle-off");
				$(this).css("color", "gray");
				$("#group_is_default").val("False");
			} else {
				$(this).attr('isdefault', "True");
				$(this).removeClass("fa-toggle-off");
				$(this).addClass("fa-toggle-on");
				$(this).css("color", "#32be77");
				$("#group_is_default").val("True");
			}
		});
	}
	//是否在参数组中启用插件设置
	function set_parameter_group_plugin_setting() {
		$("#parameter_group_enable_plugin_setting").click(function() {
			var is_default = $(this).attr('isdefault');
			if (is_default | is_default == "True") {
				$(this).attr('isdefault', "False");
				$(this).removeClass("fa-toggle-on");
				$(this).addClass("fa-toggle-off");
				$(this).css("color", "gray");
				$("#enable_plugin_settings").val("False");
			} else {
				$(this).attr('isdefault', "True");
				$(this).removeClass("fa-toggle-off");
				$(this).addClass("fa-toggle-on");
				$(this).css("color", "#32be77");
				$("#enable_plugin_settings").val("True");
			}
		});
	}
	
	
	//从参数组设置插件是否可用
	function set_plugin_enable_inparameter_group() {
		$("i[name=task_parameter_group_plugin_is_enable]").click(function() {
			var is_enable = $(this).attr("is_enable");
			var plugin_element=$(this).parent().parent().find("input[name=plugin_is_enable]");
			var plugin_id=$(plugin_element).val();
			if (is_enable == "On") {
				$(this).attr('is_enable', "Off");
				$(this).removeClass("fa-toggle-on");
				$(this).addClass("fa-toggle-off");
				$(this).css("color", "gray");
				$(plugin_element).val(plugin_id.replace("On","Off"));
			} else {
				$(this).attr('is_enable', "On");
				$(this).removeClass("fa-toggle-off");
				$(this).addClass("fa-toggle-on");
				$(this).css("color", "#32be77");
				$(plugin_element).val(plugin_id.replace("Off","On"));
			}
		});
	}

	//隐藏参数组编辑查看页面
	function close_parameter_edit_webpart() {
		$("#close_task_parameter_edit_webpart").click(function() {
			$("#task_parameter_group_edit").hide();
			$("#task_parameter_group_list").addClass('col-sm-12');
			$("#task_parameter_group_list").removeClass('col-sm-6');
		});
	}
	
	
	//初始化参数组信息
	
	function init_parameter_view_panel()
	{
		try
		{
			$("#task_parameter_group_form").jqxNavigationBar({theme:'bootstrap',expandMode: "singleFitHeight", width: '100%', height: '700px'});
			
		}
		catch(e)
		{
			console.log(e);
		}
		
	}
	
	

	
	


	window.onresize = function() {
		change_wirzard_column_width();
	}

	$(".doraemon_wizard_column_collapsed").click(function() {
		$(this).addClass("hide_wizard_collapsed");
		$(".doraemon_wizard_column_expanded").each(function() {

			if (!$(this).hasClass("hide_wizard_expanded")) {
				$(this).addClass("hide_wizard_expanded");
				var save_button = $(this).find("span[name=ci_task_config_save_btn]");
				$(save_button).click();
				$(this).parent().find(".doraemon_wizard_column_collapsed.hide_wizard_collapsed").removeClass("hide_wizard_collapsed");
			}
		});
		$(this).parent().find("div:eq(0)").removeClass("hide_wizard_expanded");
		change_wirzard_column_width();
	});
	
	
	$(".doraemon_wizard_navbar_item").click(function()
	{
		var item_name=$(this).attr('name');
		$(".doraemon_wizard_column").hide();
		var section=$("#doraemon_wirzrd").find("div[section_name="+item_name+"]");
		$(section).show();
		$(this).siblings().each(function(i,item){
			$(item).removeClass("doraemon_wizard_navbar_item_active");
		});
		$(this).addClass("doraemon_wizard_navbar_item_active");
	});

	//点击历史连接，保存当前url到cookie
	function save_url_to_cookie() {
		$("span[name=ci_task_history_link]").click(function() {
			setCookie("ci_task_entrance_link", window.location.href);
		});
		$("span[name=ci_task_config_link]").click(function() {
			// delCookie('ci_task_entrance_link');
			setCookie("ci_task_entrance_link", window.location.href);
		});
		$("a[name=ci_task_name]").click(function() {
			// delCookie('ci_task_entrance_link');
			setCookie("ci_task_entrance_link", window.location.href);
		});
	}

	//点击ci_task_property 页面返回按钮，读取入口url并刷新
	function back_ci_task_entrance_page() {
		$("span[name=ci_task_back]").click(function() {
			var uri = getCookie("ci_task_entrance_link");
			if (uri == null) {
				window.location.href = '/ci/task';
			} else {
				window.location = uri;
			}
		});

	}

	//保存cookie
	function setCookie(name, value)//两个参数，一个是cookie的名子，一个是值
	{
		var Days = 1;
		//此 cookie 将被保存 30 天
		var exp = new Date();
		//new Date("December 31, 9998");
		exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
		document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString() + ";path=/";
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

	//删除cookie
	function delCookie(name)//删除cookie
	{
		var exp = new Date();
		exp.setTime(exp.getTime() + 0 * 24 * 60 * 60 * 1000);
		var cval = getCookie(name);
		if (cval != null)
			document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString() + ";path=/";
	}
	
	//展开前3条变更记录
	expand_top3_changelog();
	function expand_top3_changelog()
	{
		var index=1;
		$("div[name=build_changelogs]").each(function()
		{   if(index<4)
			{
			   $(this).show();	
			   var expand_flag_container=$(this).parent().find("span[name=task_changelog_expand]");
			   var expand_flag_flag=$(expand_flag_container).find("i:eq(0)");
			   $(expand_flag_flag).removeClass("fa-plus-circle");
			   $(expand_flag_flag).addClass("fa-minus-circle");
			   index=index+1;
			}
		});
	}
	
	
	

	
	//隐藏详细日志页面
	close_changelog_detail_webpart();
	function close_changelog_detail_webpart() {
		$("#close_changelog_detail_webpart").click(function() {
			$("#task_changelog_detail").hide();
			$("#task_changelog_list").addClass('col-sm-12');
			$("#task_changelog_list").removeClass('col-sm-8');
		});
	}
	
	
	
	//click build log content
	click_build_log_content();
	function click_build_log_content()
	{
	    $("div[name=build_changelog_content]").click(function(){
	    	var history_id=$(this).find("span[name=task_history_id]").text();
	    	var changelog_version=$(this).find("em[name=changlog_version]").text();
	    	$(".parameter-group-selected").removeClass("parameter-group-selected");
			$(this).addClass("parameter-group-selected");
			$("#task_changelog_list").removeClass('col-sm-12');
			$("#task_changelog_list").addClass('col-sm-8');
			$("#task_changelog_detail").load("/ci/history/"+history_id+"/changelog_detail/"+changelog_version,function() {
				close_changelog_detail_webpart();
				
			});
			$("#task_changelog_detail").show();
	    });
	}
	
	
	//点击展开日志
	expand_changelog_byclick();
	function expand_changelog_byclick()
	{
		
		$("span[name=task_changelog_expand]").click(function(){
			var expand_flag_flag=$(this).find("i:eq(0)");
			var changelogs=$(this).parent().parent().find("div[name=build_changelogs]");
			if(expand_flag_flag.hasClass('fa-plus-circle'))
			{
				$(changelogs).show();
				$(expand_flag_flag).removeClass("fa-plus-circle");
			   $(expand_flag_flag).addClass("fa-minus-circle");
			}
			else
			{
				$(changelogs).hide();
				$(expand_flag_flag).addClass("fa-plus-circle");
			   $(expand_flag_flag).removeClass("fa-minus-circle");
			}
		});
	}
	
	
	//在history 页面添加实时日志显示框
	
	function open_build_log_dalog() {
		$("span[name=ci_bulid_log]").click(function(event) {
			$("#global-mark").addClass('mark');
			$("#global-mark").show();
			var history_id = $($(this).parent().parent().find("input[name=task_history_id]")).val().trim();
			$("#popup-dialog-container").load("/ci/dashboard/build_log_dialog", {
				"history_id" : history_id
			}, function() {
				$("#global-mark").removeClass('mark');
				load_pre_log();
			$("#global-mark").hide();
			adjust_bulid_log_dialog_size();
				window.onresize = function() {
		       adjust_bulid_log_dialog_size();
	            }
				$("#build-log-popup-dialog").modal('show');
				$('#build-log-popup-dialog').on('hidden.bs.modal', function(e) {
					$("#web_socket_scripts").empty(); 
				});
			});
		});
	}

	
	
	
	//load pre log contents
	
	function load_pre_log()
	{
		$("#prelog_trigger").click(function(){
			$("#build_log_loader").show();
			var tq_id=$("#log_dialog_tq_id").val();
			$(this).hide();
			$("#billboard").load("/ci/dashboard/pre_build_log",{"tq_id":tq_id});
		});
	}
	
    adjust_bulid_log_dialog_size();
	function adjust_bulid_log_dialog_size() {
		var window_width = window.innerWidth;
		console.log(window_width);
		var parent_width=window_width*0.8;
		var child_width=window_width*0.8*0.8;
			$("#build-content-container").parent().css('width',parent_width+"px");
			$("#billboard").css('width',child_width+"px" );
			$("#build-content-container").parent().css('margin-left', 'auto');
	}

	/*################################### 通用方法 #############################*/

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

	//初始化combobox
	function init_combo_box(element_name, is_multi) {
		try {
			$("select[name=" + element_name + "]").jqxComboBox({
				theme : theme,
				width : 300,
				height : 33,
				autoComplete : true,
				searchMode : 'containsignorecase',
				multiSelect : is_multi
			});

		} catch(e) {
			console.log(e);
		}
	}

	//初始化dropdownlist
	function init_dropdown_list(element_name, is_multi) {

		try {
			$("select[name=" + element_name + "]").jqxDropDownList({
				theme : theme,
				width : 300,
				height : 33
			});
		} catch(e) {
			console.log(e);
		}
	}

	function init_notification(template, data, autoclose) {
		$("#operation_notification").jqxNotification({
			width : 250,
			// position : "bottom-right",
			opacity : 0.8,
			autoOpen : false,
			animationOpenDelay : 300,
			autoClose :autoclose,
			template : template,
			appendContainer: "#notification_container",
		});
		$("#operation_notification_message").empty();
		$("#operation_notification_message").append(data);
		$("#operation_notification").jqxNotification("open");
	}

});
