$(document).ready(function() {
 var theme='bootstrap';
	/*################################    创建新项目          #############################################################*/

	create_newproject();

	function create_newproject() {

		$("#head_add_project").click(function() {
			$("#popup-dialog-container").load("/project/create_dialog", function() {

				$("select[name=PBPlatform]").jqxDropDownList({
					theme : theme,
					width : 300,
					height : 33
				});

				$("select[name=PBLead]").jqxComboBox({
					theme : theme,
					width : 300,
					height : 33,
					autoComplete : true,
					searchMode:'containsignorecase'
				});
				
				
				$("select[name=Product]").jqxDropDownList({
					theme : theme,
					width : 300,
					height : 33
				});
				
				
			   

				$("#newproject-popup-dialog").modal('show');
				submit_project_form();
			});
		});

	}

	function submit_project_form() {
		$("#project_create_button").click(function() {

			if (validate_project()) {
				$("#newproject-popup-dialog").modal('hide');
				$.post("/project/create", $('#project-create-form').serialize(), function(data, status) {
					if (data == "True") {
						init_notification("success", "项目创建成功!", false);
					} else {
						init_notification("error", data, false);
					}
				});
			}
		});
	}

	function validate_project() {
		var project_title = $("#project_title"), project_key = $("#project_key"), project_lead = $("#project_lead");
		allFields = $([]).add(project_title).add(project_key).add(project_lead);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(project_title, "请输入项目名称");
		valid = valid && check_project_filed_exists("PBTitle", project_title, "项目名称已经存在");
		valid = valid && check_object_is_null(project_key, "请输入项目key");
		valid = valid && check_project_key(project_key, "项目key长度为3-10个英文字符");
		valid = valid && check_project_filed_exists("PBKey", project_key, "项目Key已经存在");
		valid = valid && check_object_is_null(project_lead, "项目负责人不能为空");
		return valid;
	}

	function check_project_filed_exists(filed_name, filed, message) {
		var result=true;
		var filed_value = filed.val().trim();
		$.ajax({
			async : false,
			type : "POST",
			url : "/project/check_value_exists",
			data : 
			{
				"filed" : filed_name,
				"value" : filed_value
			},
			success : function(data, status)
			 {
				if (data == "False")
				 {
					result= true;
				} 
				else 
				{
					filed.parent().parent().addClass("has-error");
					init_notification("error", message, true);
					result= false;
				}
			 }
		});
		return result;

	}

	function check_project_key(project_key, message) {
		var express = /^[a-zA-Z]{3,10}/;
		if (express.test(project_key.val())) {
			return true;
		} else {
			project_key.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		}

	}
	

	/*##########################################创建任务############################################################*/

	create_newtask();

	function create_newtask() {

		$("#head_add_task").click(function() {
			$("#popup-dialog-container").load("/project/task/create_dialog", function() {
				$("#newtask-popup-dialog").modal('show');
				init_page();

				show_tag_popmenu();

				select_menu_item();

				show_calender("span[name=dead_line_date]", "span[name=task-deadline-date]");
				show_calender("span[name=start_date]", "span[name=task-start-date]");

				show_member_popmenu();

				show_project_popmenu();

				popmenu_search();
				set_progress();

				submit_task_form();
			});
		});

	}

	function set_progress() {
		var progress = 0;
		$("span[name=task-progress]").click(function() {
			$(this).text("");
		});

		$("span[name=task-progress]").blur(function() {
			progress = $(this).text();
			$(this).text(progress + "%");
			$(this).parent().css('width', progress + "%");
			console.log(progress);
			$(this).parent().attr("aria-valuenow", progress);
		});
	}

	function init_page() {
		/*初始化页面元素*/
		$("div[name=project-task-tags]").hide();
		$("div[name=calender]").hide();
		$("div[name=member-list]").hide();
		$("div[name=project-group]").hide();
	}

	function submit_task_form() {
		$("#task_create_button").click(function() {
			var filed_values = get_task_filed();
			console.log(filed_values);
			if (validate_task(filed_values["Title"], filed_values["ProjectID"],filed_values["DeadLine"],filed_values["StartDate"])) {
				$("#newtask-popup-dialog").modal('hide');
				$.post("/project/task/create", filed_values, function(data, status) {
					if (data == "True") {
						init_notification("success", "任务创建成功!", false);
					} else {
						init_notification("error", data, false);
					}
				});
			}
		});
	}

	function get_task_filed() {
		var filed_dic = {};
		filed_dic["Title"] = $("#project_task_title").val();
		filed_dic["Description"] = $("#project_task_description").val();
		filed_dic["Owner"] = get_task_label_filed("Owner");
		filed_dic["ProjectID"] = get_task_label_filed("ProjectID");
		filed_dic["StartDate"] = $("#newtask-popup-dialog span[name=task-start-date]").text().replace("未设置开始日期","");
		filed_dic["DeadLine"] = $("#newtask-popup-dialog span[name=task-deadline-date]").text().replace("未设置截止日期","");
		filed_dic["Progress"] = $("#newtask-popup-dialog span[name=task-progress]").parent().attr('aria-valuenow');
		filed_dic["WorkingHours"] = $("#newtask-popup-dialog span[name=task-working-hours]").text();
		filed_dic["Tags"] = get_task_label_filed("Tags");
		return filed_dic;
	}

	function validate_task(ttitle, ProjectID,deadline,startdate) {
		var valid = true;
		valid = valid && check_value_is_null(ttitle, "请输入任务名称！");
		valid = valid && check_value_is_null(ProjectID, "请选择任务所属项目");
		valid = valid && check_value_is_null(deadline, "请输入截止日期");
		valid = valid && check_value_is_null(startdate, "请输入开始日期");
		return valid;
	}

	function get_task_label_filed(filed_name) {
		var labelid = "";
		$("div[name=" + filed_name + "]").children("span[labelid]").each(function() {
			labelid = labelid + $(this).attr("labelid").trim() + ",";
		});
		return labelid;
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

	function show_tag_popmenu() {
		$("span[name=add_tag]").click(function() {
			var popmenu = $(this).parent().find("div[name=project-task-tags]");
			currentoPopObject = popmenu;
			currentTrigger = $(this);
			popmenu.show();
			popmenu.jqxPanel({
				theme : 'metro',
				width : 200,
				height : 200
			});
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}

	function select_menu_item() {
		$("input[name=context_search_input]").parent().nextAll().each(function() {
			$(this).click(function(e) {
				e.stopPropagation();
				var labelid = $(this).attr('labelid');
				var text = $(this).text().trim();
				var firstChild = $(this).children("i:eq(0)");
				var background = $(this).children("i:eq(1)").css('color');
				var classname = firstChild.attr('class');
				if (classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) {
					firstChild.removeClass('fa-check');
					if ($(this).parent().find("input[name=context_search_input]").attr("role")) {
						remove_tag($(this), labelid, false);
					} else {
						remove_tag($(this), labelid, true);
					}
				} else {
					var item_role = $(this).parent().find("input[name=context_search_input]").attr("role");
					console.log(item_role);
					add_item($(this), labelid, background, text, item_role);
				}
			});
		});
	}

	function add_item(currentitem, labelid, background, text, role) {
		var firstChild = $(currentitem).children("i:eq(0)");
		if (role == "tag-inline") {
			firstChild.addClass('fa-check');
			var insertElement = "<span class='label label-default' labelid='" + labelid + "' style='background-color:" + background + "; opacity:0.5'><i class='fa fa-tag fa-fw'></i>" + text + "</span>";
			var insertedElement = currentitem.parent().parent().parent().parent().parent().children('span:eq(0)');
			$(insertElement).insertAfter(insertedElement);
		} else if (role == "tag") {
			firstChild.addClass('fa-check');
			var tag_html = "<span class='col-sm-12 task_detail_menu_item' labelid=" + labelid + "><span class='label label-default' style='background-color:" + background + "; opacity:0.5'><i class='fa fa-tag fa-fw'></i>" + text + "</span></span>";
			var insertedElement = $(currentitem).parent().parent().parent().parent().parent();
			$(tag_html).insertAfter(insertedElement);
		} else if (role == "member") {
			firstChild.addClass('fa-check');
			var image_src = $(currentitem).children("img:eq(0)").attr("src");
			var tag_html = "<span class='col-sm-12 task_detail_menu_item' labelid=" + labelid + "><img src='" + image_src + "' class='img-circle' style='width:20px;height:20px' />" + text + "</span></span>";
			var insertedElement = $(currentitem).parent().parent().parent().parent().parent();
			$(tag_html).insertAfter(insertedElement);
		} else if (role == "project") {
			uncheck_all_menu_item(currentitem, currentitem.parent());
			firstChild.addClass('fa-check');
			var image_src = $(currentitem).children("img:eq(0)").attr("src");
			var tag_html = "<span class='col-sm-12 task_detail_menu_item' labelid=" + labelid + "><img src='" + image_src + "' class='img-circle' style='width:20px;height:20px'/>  " + text + "</span></span>";
			var insertedElement = $(currentitem).parent().parent().parent().parent().parent();
			$(tag_html).insertAfter(insertedElement);
			$("div[name=project-group]").hide();
		}
	}

	function remove_tag(currentitem, labelid, role) {
		if (role == "tag-inline") {
			var removedlabel = $(currentitem).parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
			removedlabel.remove();
		} else {
			var removedlabel = $(currentitem).parent().parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
			removedlabel.remove();
		}
		init_page();
	}

	function show_calender(trigger, target) {
		$(trigger).click(function() {
			$(this).next().show();
			$(this).next().jqxCalendar({
				theme : 'metro',
				width : '220px',
				height : '220px'
			});

			hide_control_byclick_page($(this).next(), $(this));

			$(this).next().on('change', function(event) {
				var date = $(this).jqxCalendar('getDate');
				var newDate = new Date(date);
				var selecteddate = newDate.getFullYear() + '-' + (newDate.getMonth() + 1) + '-' + newDate.getDate();
				$(target).text(selecteddate);
				event.stopPropagation();
				$(this).hide();
			});
		});

	}

	function show_member_popmenu() {
		$("span[name=task-add-owner]").click(function() {
			var popmenu = $(this).parent().find("div[name=member-list]");
			currentoPopObject = popmenu;
			currentTrigger = $(this);
			popmenu.show();
			popmenu.jqxPanel({
				theme : 'metro',
				width : 200,
				height : 200
			});
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}

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

	function show_project_popmenu() {
		$("span[name=task-add-project]").click(function() {
			var popmenu = $(this).parent().find("div[name=project-group]");
			currentoPopObject = popmenu;
			currentTrigger = $(this);
			popmenu.show();
			popmenu.jqxPanel({
				theme : 'metro',
				width : 200,
				height : 200
			});
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
		});

	}

	function uncheck_all_menu_item(currentitem, role_group) {
		role_group.children().each(function() {
			if ($(this) != $(currentitem)) {
				console.log("task2");
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

	/*#############################################################新建功能提测#################################################################################*/
	create_newfortesting();
	var old_project_id=0;
	var new_project_id=0;
	var inteval_code=0;
	var project_id=$("#project_id").attr('projectid');
	function create_newfortesting() {

		$("#head_add_fortesting").click(function() {
			if(project_id==null)
				{
				  project_id=1;
				}
			$("#popup-dialog-container").load("/project/fortesting/get_create",{'project_id':project_id,'test_application':0}, function() {
				init_fortesting_create_form(project_id);
				$("#newfortesting-popup-dialog").modal('show');
				submit_fortesting_form();
				flag=true;
				project_change_handler("fortesting-create-form");
			});
		});
	}
	
	
	
	function init_fortesting_create_form(project_id)
	{
        try
        {
			if(project_id!=null)
			{
				init_DropDownList("ProjectID",project_id);
			}
			else
			{
				init_DropDownList("ProjectID",0);		
			}
			init_DropDownList("VersionID",0);
        	
        	   init_editor("fortesting-create-form","TestingFeature");
        	   init_editor("fortesting-create-form","TestingAdvice");
        	   init_fortesting_file_upload("fortesting-create-form");
        	   init_datetime_input();
    		   load_project_module("ProjectModule",project_id);
    		   load_project_version("VersionID",project_id);
        }
        catch(ex)
        {
        	   console.log(ex);
        }
	}
	
	function init_datetime_input()
	{
		$("#fortesting-create-form #ExpectCommitDate").jqxDateTimeInput({ "width": 300, "height": 25,"formatString":"yyyy-MM-dd",readonly: true});
 	   $('#fortesting-create-form #ExpectCommitDate').on('valueChanged', function (event) {
         
            var date =$("#fortesting-create-form #ExpectCommitDate").jqxDateTimeInput("getText");
            $('#fortesting-create-form #ExpectCommitDate_jqxDateTimeInput').attr("value",date);
        });
	}
	

	function submit_fortesting_form() {
		$("#fortesting_create_button").click(function() {
			if (validate_fortesting()) {
				$("#newfortesting-popup-dialog").modal('hide');
				$.post("/project/fortesting/create", $('#fortesting-create-form').serialize(), function(data, status) {
					if (data == "True") {
						init_notification('success', "提测创建成功！");
						location.reload();
					} else {
						init_notification('error', data);
					}
				});
				clearInterval(inteval_code);
			}
			
		});
	}

	function validate_fortesting() {
		var project = $("#ProjectID"), version = $("#fortesting-create-form #VersionID"), newfeature = $("#fortesting-create-form #TestingFeature"), advice = $("#fortesting-create-form #TestingAdvice");
		var topic=$("#Topic");
		allFields = $([]).add(project).add(version).add(newfeature).add(advice).add(topic);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(project, "项目不能为空！");
		valid = valid && check_object_is_null(version, "版本不能为空！");
		valid = valid && check_object_is_null(topic, "提测主题必须填写");
		valid = valid && check_editor_is_null(newfeature, "提测内容为必填项");
		valid = valid && check_editor_is_null(advice, "测试建议为必填项");
		return valid;
	}
	
	function check_editor_is_null(editor,message)
	{
		var value=$(editor).jqxEditor('val');
		if(value.length<=1)
		{
			editor.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;	
		}
		else
			{
			  return true;
			}
	}
	
	
	/*##############################################新建CI任务#################################################*/
	
	
		create_new_ci_task();

	function create_new_ci_task() {

		$("#head_add_ci_task").click(function() {
			$("#popup-dialog-container").load("/ci/task/create_dialog", function() {

				
				init_ci_task_form();
				$("#new_ci_task_popup_dialog").modal('show');
				
				$("#ci_create_task_deploy").click(function(){
				   $("#deploy_service_combobox").show();
				});
				$("#ci_create_task_copy").click(function(){
				   $("#my_tasks_combobox").show();
				});
				submit_ci_task_form();
			});
		});

	}
	
	function init_ci_task_form()
	{
		$("select[name=Project]").jqxComboBox({
			theme : theme,
			width : 300,
			height : 33,
			autoComplete : true,
			searchMode : 'containsignorecase'
		});
		
		// $("select[name=DeployService]").jqxComboBox({
		// 	theme : theme,
		// 	width : 300,
		// 	height : 33,
		// 	autoComplete : true,
		// 	searchMode : 'containsignorecase'
		// });
		
		$("select[name=my_all_tasks]").jqxComboBox({
			theme : theme,
			width : 300,
			height : 33,
			autoComplete : true,
			searchMode : 'containsignorecase'
		});
		
	}
	
	function submit_ci_task_form() {
		$("#ci_task_create_button").click(function() {
			if (validate_ci_task()) {
				$("#new_ci_task_popup_dialog").modal('hide');
				$.post("/ci/task/create", $('#ci_task_create_form').serialize(), function(data, status) {
					if (data != "0") 
					{
						window.location.href="/ci/deploy/"+data+"/config";
					} else {
						init_notification('error', data);
					}
				});

			}
		});
	}

	function validate_ci_task() {
		var ci_task_name = $("#ci_task_name"),ci_task_project=$("#ci_task_project");
		allFields = $([]).add(ci_task_name).add(ci_task_project);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(ci_task_name, "任务名称不能为空！");
		valid = valid && check_project_is_null(ci_task_project,"任务项目不能为空");
		return valid;
	}
	
	function check_project_is_null(validate_object,message)
	{
		var select_item = $(validate_object).jqxComboBox('getSelectedItem');
		if(select_item!=null)
		{
			return true;
		}
		else
		{
			validate_object.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		}
	}

	
	/*###################################################新建问题###################################################*/
	
	create_newIssue();
	function create_newIssue() {
		

		$("#head_add_issue").click(function() {
			var project_id=$("#project_id").attr('projectid');
			if(project_id==null)
				{
				  project_id=0;
				}
			$("#popup-dialog-container").load("/project/issue/open_create_dialog",{'project_id':project_id}, function() {
				init_CreateIssueForm(project_id);
				project_change_handler("project_issue_create_form");
				OS_change_handler();
				$("#newissue-popup-dialog").modal('show');
				submit_issue_create_form(project_id);
			});
		});
	}
    
	function init_CreateIssueForm(project_id)
	{
        try
        {
            var form_id="#project_issue_create_form";
            init_comboBox("IssueProcessor",0);
		   init_DropDownList("ProjectID",project_id);
		   init_DropDownList("VersionID",0);
		   init_DropDownList("IssueCategory",0);
            init_DropDownList("IssueTeam",1);
		   init_DropDownList("IssueCategory",0);
		   init_DropDownList("IssueSeverity",0);
		   init_DropDownList("ProjectPhase",0);
		   init_DropDownList("OS",0);
		   init_DropDownList("OSVersion",0);
		   init_editor("project_issue_create_form","IssueDescription");
		   init_issue_file_upload("project_issue_create_form");
		   load_project_module("ProjectModule",project_id);
		   load_project_version("VersionID",project_id);
		   load_project_member("IssueProcessor",project_id);
        }
        catch(ex)
        {
        	   console.log(ex);
        }
	}
	
	function submit_issue_create_form(project_id)
	{
		$("#issue_create_button").click(function() {
			if (true) {
				$("#newissue-popup-dialog").modal('hide');
				$.post("/project/issue/create", $('#project_issue_create_form').serialize(), function(data, status) {
					if (data == "True") 
					{
						$("#reload_issue_list").trigger("click");
					} else {
						init_notification('error', data);
					}
				});

			}
		});
	}
	
	
	
	
	/*###############################################通用方法##################################################*/

	function check_object_is_null(o, message) {
		console.log(o.val());
		if (!(o.val().length > 0)) {
			o.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		} else {
			return true;
		}
	}

	function check_value_is_null(value, message) {
		if (!(value.length > 0)) {
			init_notification("error", message, true);
			return false;
		} else {
			return true;
		}
	}

	function init_notification(template, data, autoclose) {
		$("#operation_notification").jqxNotification({
			width : 250,
			// position : "bottom-right",
			opacity : 0.8,
			autoOpen : false,
			animationOpenDelay : 300,
			autoClose : autoclose,
			template : template,
			appendContainer: "#notification_container",
		});
		$("#operation_notification_message").empty();
		$("#operation_notification_message").append(data);
		$("#operation_notification").jqxNotification("open");
	}

	function init_editor(formid,editor_id)
	{
		  $('#'+formid+' #'+editor_id).jqxEditor({
        	  height: 200,
        	  width: "100%",
        	  theme:'office',
        	  tools: 'bold italic underline | ul ol | html',
        	  lineBreak: 'br'
        	});
        
        $(".jqx-editor-content").css('height','159px');
	}
	
	function init_comboBox(name,value)
	{
		$("select[name="+name+"]").jqxComboBox({
			theme : theme,
			width : "100%",
			height : 33,
			autoComplete : true,
			searchMode : "containsignorecase"
		});
		if(value!=0){
			var item = $("select[name="+name+"]").jqxComboBox('getItemByValue',value);
			$("select[name="+name+"]").jqxComboBox('selectItem', item);
		}
	}
	
	function init_DropDownList(name,value)
	{

		$("select[name="+name+"]").jqxDropDownList({
			theme : theme,
			width : "100%",
			height : 33,
            filterable : true
		});
		if(value!=0){
			var item = $("select[name="+name+"]").jqxDropDownList('getItemByValue',value);
			$("select[name="+name+"]").jqxDropDownList('selectItem', item);
		}	
	}

    function init_DropDownListWithParentID(name,value,parentid)
    {
        $(parentid+" select[name="+name+"]").jqxDropDownList({
            theme : theme,
            width : "100%",
            height : 33,
            filterable : true
        });
        if(value!=0){
            var item = $("select[name="+name+"]").jqxDropDownList('getItemByValue',value);
            $("select[name="+name+"]").jqxDropDownList('selectItem', item);
        }
    }
	
	function init_fortesting_file_upload(formName)
	{
		 $("form[name="+formName+"]").dropzone({ 
         	
     	    url:'/project/fortesting/upload_attachment',         
         method:'post',
         paramName:'attachment',
         addRemoveLinks: true,
         maxFiles: 10,
         maxFilesize: 10,
         width:"100%",
         uploadMultiple: true,
         parallelUploads: 10,
//         acceptedFiles: ".pdf, .doc,.txt,.docx,.xlsx,.xls,.sql",
         success: function(file, response, e) {
             file.id=response;
             var attachments=$("#"+formName+" #upload_files").val();
             $("#"+formName+"  #upload_files").attr("value",attachments+file.id+",");
         },
		 removedfile: function(file,e){
			 file.previewElement.remove();
			 var file_id=file.id;
			 $.get("/project/fortesting/0/delete_file/"+file_id,function(data,status){
				 var attachments=$("#fortesting-create-form #upload_files").val();
	             $("#"+formName+"  #upload_files").attr("value",attachments.replace(file.id+",","")); 
			 });
		 }
     });
     
     $("form[name="+formName+"]").click(function(){
     	     $(this).parent().parent().css('height','200px');
     });
	}
	
	function init_issue_file_upload(formName)
	{
		 $("form[name="+formName+"]").dropzone({ 
         	
     	    url:'/project/issue/cached_attachment',         
         method:'post',
         paramName:'attachment',
         addRemoveLinks: true,
         maxFiles: 10,
         maxFilesize: 10,
         width:"100%",
         uploadMultiple: true,
         parallelUploads: 10,
//         acceptedFiles: ".pdf, .doc,.txt,.docx,.xlsx,.xls,.sql",
         success: function(file, response, e) {
             results=response.split(",");
             if(results[1]=="null")
            	 {
            	     var attachments=$("#"+formName+" #upload_files").val();
                 $("#"+formName+"  #upload_files").attr("value",attachments+results[0]+",");
            	 }
             else
            	 {
            	   init_notification("error",results[1],false);
            	 }
         },
		 removedfile: function(file,e){
			 file.previewElement.remove();
		 }
     });
     
     $("form[name="+formName+"]").click(function(){
     	     $(this).parent().parent().css('height','200px');
     });
	}
	
	//根据project 决定是否显示模块选项
	function load_project_module(module_name,project_id)
	{
		$("select[name="+module_name+"]").load("/project/fortesting/"+project_id+"/project_module_list",function(data,status){
			if(data=="")
				{
				  $("div[name=project_module]").hide();
				}
			else
				{
				$("div[name=project_module]").show();
				$("select[name="+module_name+"]").jqxDropDownList('loadFromSelect',module_name+'_jqxDropDownList');
				$("select[name="+module_name+"]").jqxDropDownList({
					theme : theme,
					width :"100%",
					height : 33,
					selectedIndex:0,
                    filterable: true
				});
				}
		});
	}
	
	//根据project 变更version可选值
	function load_project_version(version_controll,project_id)
	{
		$("select[name="+version_controll+"]").load("/project/fortesting/"+project_id+"/project_version_list",{"default_none":1},function(data,status){
				$("select[name="+version_controll+"]").jqxDropDownList('loadFromSelect', version_controll+'_jqxDropDownList');
				$("select[name="+version_controll+"]").jqxDropDownList({
					theme : theme,
					width : "100%",
					height : 33,
					selectedIndex:0,
                    filterable: true
				});
		});
	}
	
	function load_project_member(controll,project_id)
	{
		$("select[name="+controll+"]").load("/project/"+project_id+"/member/project_member_dropdownlist",function(data,status){
				$("select[name="+controll+"]").jqxComboBox('loadFromSelect', controll+'_jqxComboBox');
				$("select[name="+controll+"]").jqxComboBox({
					theme : theme,
					width : "100%",
					height : 33,
                    autoComplete : true,
                    searchMode : "containsignorecase"
				});
		});
	}
	
	function load_project_os_version(controll,os_value)
	{
		$("select[name="+controll+"]").load("/project/os/"+os_value+"/os_version_controll",function(data,status){
				$("select[name="+controll+"]").jqxDropDownList('loadFromSelect', controll+'_jqxDropDownList');
				$("select[name="+controll+"]").jqxDropDownList({
					theme : theme,
					width : "100%",
					height : 33,
					selectedIndex: 0,
                    filterable: true
				});
		});
	}
	
	
	
	function project_change_handler(from_id)
	{ 
		$("#"+from_id+" #ProjectID").on('change', function (event){
		    var args = event.args;
		    if (args) {
		    	var item = args.item;
		    var value = item.value;
		     load_project_module("ProjectModule",value);
			 load_project_version("VersionID",value);
			 load_project_member("IssueProcessor",value);
			
		}
		});
	}
	
	function OS_change_handler()
	{ 
		$("#OS").on('change', function (event){
		    var args = event.args;
		    if (args) {
		    	var item = args.item;
		    var value = item.value;
		    load_project_os_version("OSVersion",value);
		}
		});
	}
			  

});
