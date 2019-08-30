$(document).ready(function() {
	var theme = 'bootstrap';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	var window_height=$(window).height();

	init_page();
	
	init_project_dorpdown();

	show_member_add_dialog();

	show_member_role_popmenu();

	select_member_role_item();

	save_project_changes();

	delete_project();

	remove_member();

	add_webhook();

	save_webhook();

	delete_webhook();
	
	set_webhook_default();
	
	perform_webhook();
	
	// init_webhook_form_default_button();
    init_webhook_list_default_button();
    
    
    show_calender("span[name=project_version_startdate_trigger]", "span[name=VStartDate]");
	//显示开始日期日历
	show_calender("span[name=project_version_releasedate_trigger]", "span[name=VReleaseDate]");
	//显示发布日期控件
	
	create_version_press_enter();
	//回车创建版本
	create_version_click();
	//点击箭头创建版本
	
	delete_version();
	//删除版本
	
	update_version_number();
	
	//创建模块
	create_module_press_enter();
	
	//点击创建
	create_module_click();

	//删除模块
	delete_module();
	
	//更新模块名称
	update_module_name();
	
	//更新模块描述
	update_module_desc();
    
	function init_page() {
		/*初始化页面元素*/
		$("div[name=member-list]").hide();
		$("div[name=project-role-list]").hide();
		$("input[name=popmenu_memeber_role_search]").parent().hide();
		$("span[name=version_update_loader]").hide();
		$("#project_info_container").css('max-height',(window_height-150)+"px");
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

	function show_member_add_dialog() {
		$("span[name=project-add-member]").click(function() {
			var project_id=$("#project_id").attr("projectid");
			$("#popup-dialog-container").load("/project/"+project_id+"/settings/member/add_dialog",function(){
			   $("#project-add-member-dialog").modal('show');
			   init_member_add_dialog();
			   select_user_2_memberlist();
				switch_2_member_import_view();
				
				switch_2_member_add_view();
				
				invite_member();
				
				close_member_add_dialog();
			});
		});
			

	}
	
	function init_member_add_dialog()
	{
		 var project_id=$("#project_id").attr("projectid");
	   	   var cookie_key="project_"+project_id+"_member_ids";
	   	   var cookie_path="/project/"+project_id+"/settings/member";
		setCookie(cookie_key,null,cookie_path);
		$("#add-member-view").show();
	    $("#import-member-view").hide();
	    $("#add-member-dialog-add-button").parent().parent().addClass("fortesting_view_edit_active");
	    $("#add-member-dialog-import-button").parent().parent().removeClass("fortesting_view_edit_active");
	    $("#source-user-list").jqxListBox({multiple: true,theme:theme,
	      	 width: 230, height: 250,itemHeight:50,
	      	 searchMode: 'containsignorecase'
	      	 });
	       $("#member-user-list").jqxListBox({multiple: true,theme:theme,
	      	 width: 230, height: 250,itemHeight:50,
	      	 searchMode: 'containsignorecase'
	      	 });
	       
	       $("select[name=ProjectID]").jqxDropDownList({
	   		theme : 'bootstrap',
	   		width : 300,
	   		height : 33
	   	});
	}
	
    function select_user_2_memberlist()
    {
    	$("#add_member_button").click(function(){
    	   	  var project_id=$("#project_id").attr("projectid");
    	   	   var items = $("#source-user-list").jqxListBox('getSelectedItems');
    	   	   var cookie_key="project_"+project_id+"_member_ids";
    	   	   var cookie_path="/project/"+project_id+"/settings/member";
    	   	   for(var i = 0, l = items.length; i < l; i++) {
    	   		  var item=items[i];
    	   		  $("#member-user-list").jqxListBox("addItem",item);
    	      	  $("#source-user-list").jqxListBox("removeItem",item);
    	      	  var old_value=getCookie(cookie_key);
    	      	  var new_value="";
    	      	  if(old_value!=null)
    	      	  {
    	      		  new_value=old_value+","+item.value
    	      	  }
    	      	  else
    	      	  {
    	      		  new_value=item.value;
    	      	  }
    	      	  setCookie(cookie_key,new_value,cookie_path);
    	   	   }
    	    });
    }
    
    function switch_2_member_add_view()
    {
    	$("#add-member-dialog-add-button").click(function(){
       	    $("#add-member-view").show();
       	    $("#import-member-view").hide();
       	    $(this).parent().parent().addClass("fortesting_view_edit_active");
       	    $("#add-member-dialog-import-button").parent().parent().removeClass("fortesting_view_edit_active");
        });
    }
    
    function switch_2_member_import_view()
    {
    	$("#add-member-dialog-import-button").click(function(){
    	    $("#add-member-view").hide();
    	    $("#import-member-view").show();
    	   $(this).parent().parent().addClass("fortesting_view_edit_active");
    	  $("#add-member-dialog-add-button").parent().parent().removeClass("fortesting_view_edit_active");
    	    
     });
    }
	
	
    
    

	function invite_member() {
		$("#member_adddialog_confirm_button").click(function(){
			var project_id=$("#project_id").attr("projectid");
			var cookie_key="project_"+project_id+"_member_ids";
			var cookie_path="/project/"+project_id+"/settings/member";
			var userids=getCookie(cookie_key);
			var is_add_member=$("#add-member-dialog-add-button").parent().parent().hasClass("fortesting_view_edit_active");
			if(is_add_member)
				{
				  add_member(project_id,cookie_key,cookie_path);
				}
			else{
				var from_project_id=$("select[name=ProjectID]").jqxDropDownList('getSelectedItem').value;
				import_member(project_id,cookie_key,cookie_path,from_project_id);
			}
			$("#project-add-member-dialog").modal('hide');
			window.location.href=window.location.href;
		});
		
	}
	
	function close_member_add_dialog()
	{
		$("#member_adddialog_close_button").click(function(){
			var project_id=$("#project_id").attr("projectid");
			var cookie_key="project_"+project_id+"_member_ids";
			var cookie_path="/project/"+project_id+"/settings/member";
			setCookie(cookie_key,null,cookie_path);
			window.location.href=window.location.href;
		});
		
	}
	
	
	function import_member(project_id,cookie_key,cookie_path,from_project) {
		$.post("/project/"+project_id+"/settings/member"+ "/import", {
			"from_project" : from_project
		}, function(data, status) {
			if (data == "True") 
			{
				load_project_member();
			} else {
				init_notification('error', data, true);
			}
		});
		setCookie(cookie_key,null,cookie_path);
	}
	
	function add_member(project_id,cookie_key,cookie_path)
	{
		var userids=getCookie(cookie_key).replace("null,","");
		$.post("/project/"+project_id+"/settings/member"+ "/add", {
			"user_ids" : userids
		}, function(data, status) {
			if (data == "True") 
			{
				load_project_member();
			} else {
				init_notification('error', data, true);
			}
		});
		setCookie(cookie_key,null,cookie_path);
	}
	
	function load_project_member()
	{

		$("#project_member_list").load(rootUri+"/get_member_list",function(){
			$("div[name=project-role-list]").hide();
			show_member_role_popmenu();
            select_member_role_item();
            remove_member();

		});
	}

	function remove_member() {
		$("a[name=project_remove_member]").click(function() {
			var labelid = $(this).parent().parent().parent().find("span[name=userid]").attr("userid");
			$("#object_delete_confirm").modal('show');
			// $("#operation_prompt_dialog").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');

				$.post(rootUri + "/remove", {
					"PMMember" : labelid
				}, function(data, status) {
					if (data == "True") {
						window.location.href = rootUri;
					} else {
						init_notification('error', data, true);
					}
				});
			});
		});
	}

	function show_member_role_popmenu() {
		$("span[name=project-member-role]").click(function() {
			var popmenu = $(this).parent().find("div[name=project-role-list]");
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

	function select_member_role_item() {
		var role_items = $("input[name=popmenu_memeber_role_search]").parent().nextAll();
		role_items.each(function() {
			$(this).click(function(e) {
				e.stopPropagation();
				var labelid = $(this).attr('labelid');
				var text = $(this).text().trim();
				var background = $(this).children("i:eq(1)").css('color');
				var firstChild = $(this).children("i:eq(0)");
				var classname = firstChild.attr('class');
				if (classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) {
					// firstChild.removeClass('fa-check');
					// var removedlabel = $(this).parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
					// removedlabel.remove();
				} else {
					uncheck_all_member_role($(this), role_items);
					firstChild.addClass('fa-check');
					var insertElement = "<span class='label label-default visible-lg-inline-block' labelid='" + labelid + "' style='background-color:" + background + "; opacity:0.5'>" + text + "</span>";
					var insertedElement = $(this).parent().parent().parent().parent().parent().find('span:eq(0)');
					$(insertElement).insertAfter(insertedElement);
				}
				set_member_role($(this));
			});
		});
	}

	function set_member_role(currentitem) {
		var labelid = "";
		var memberid = "";
		$(currentitem).parent().parent().parent().parent().parent().find("span[labelid]").each(function() {
			labelid = labelid + $(this).attr("labelid").trim();
			memberid = $(this).parent().parent().parent().find("span[name=userid]").attr("userid");
		});
		if (labelid != "" && memberid != "") {
			$.post(rootUri + "/" + memberid + "/update_role", {
				"PMRoleID" : labelid
			}, function(data, status) {
				if (data == "True") {
					init_notification('success', "修改保存成功！", true);
				} else {
					init_notification('error', data, true);
				}
			});
		}
	}

	function uncheck_all_member_role(currentitem, role_group) {
		role_group.each(function() {
			if ($(this) != currentitem && currentitem.parent().parent().parent().parent().parent().html() == $(this).parent().parent().parent().parent().parent().html()) {
				var labelid = $(this).attr('labelid');
				var firstChild = $(this).children("i:eq(0)");
				var classname = firstChild.attr('class');
				if (classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) {
					firstChild.removeClass('fa-check');
					var removedlabel = $(this).parent().parent().parent().parent().parent().find("span[labelid=" + labelid + "]");
					removedlabel.remove();
				}

			}
		});
	}


    function init_project_dorpdown()
    {
    	try
    	{
    		$("select[name=PBPlatform]").jqxDropDownList({
		theme : theme,
		width : 300,
		height : 33
	});

	$("select[name=PBLead]").jqxComboBox({
		theme : 'bootstrap',
		width : 300,
		height : 33,
		autoComplete : true,
		searchMode:'containsignorecase'
	});
	
	$("select[name=Product]").jqxDropDownList({
		theme : 'bootstrap',
		width : 300,
		height : 33
	});

    	}
    	catch(e)
    	{
    		console.log(e.message);
    	}
  
    }

	
	
	
	
	function save_project_changes() {
		$("#save_project").click(function() {

			$.post(rootUri + "/edit", $('#project-edit-form').serialize(), function(data, status) {
				if (data == "True") {
					init_notification('success', "修改保存成功！", true);
				} else {
					init_notification('error', data, true);
				}
			});
		});
	}

	function delete_project() {
		$("#project_delete_button").click(function() {
			$("#object_delete_confirm").modal('show');
			// $("#operation_prompt_dialog").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');

				$.post(rootUri + "/delete", function(data, status) {
					if (data == "True") {
						window.location.href = "/project";
					} else {
						init_notification('error', data, true);
					}
				});
			});
		});
	}

	function add_webhook() {
		$("#project_add_webhook").click(function() {
			if (validate_webhook()) {
				$.post(rootUri + "/create", $('#project_webhook_form').serialize(), function(data, status) {
					console.log(status);
					if (data == "True") {
						window.location.href = rootUri;
					} else {
						init_notification("error", data, false);
					}
				});
			}
		});
	}

	function save_webhook() {
		$("#project_save_webhook").click(function() {
			if (validate_webhook()) {
				$.post(rootUri, $('#project_webhook_form').serialize(), function(data, status) {
					if (data != "") 
					{
						init_notification("error", data, false);
					}
				});
			}
		});
	}

	function validate_webhook() {
		var hook_url = $("#project_webhook_url"), hook_label = $("#project_hook_label");
		allFields = $([]).add(hook_url).add(hook_label);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(hook_url, "WebHook Url不能为空");
		valid = valid && check_object_is_null(hook_label, "标签 不能为空");
		return valid;
	}

	function delete_webhook() {
		$("button[name=project_delete_webhook]").click(function() {
			var webhookid = $(this).parent().parent().find("td[name=project_webhookid]").text().trim();
			$("#object_delete_confirm").modal('show');
			// $("#operation_prompt_dialog").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');

				$.post(rootUri + "/" + webhookid + "/remove", function(data, status) {
					if (data == "True") {
						window.location.href = rootUri;
					} else {
						init_notification('error', data, true);
					}
				});
			});
		});
	}
	
	// function init_webhook_form_default_button()
	// {
		 // var checked_value=$('div[name=WHIsDefault]').attr('isdefault')=="False"?false:true;;
		 // $('div[name=WHIsDefault]').jqxSwitchButton({theme:'metro' ,height: 27, width: 60,  checked: checked_value,onLabel:'默认' });
	// }
	
	function init_webhook_list_default_button()
	{
		$('div[name=project_webhook_default]').each(function()
		{
			var checked_value=$(this).attr('isdefault')=="False"? false:true;
		    $(this).jqxSwitchButton({theme:'metro',height:20, width: 60,  checked: checked_value,onLabel:'默认'});
			
		});
	
	}
	
	function set_webhook_default()
	{
	   $("i[name=project_webhook_default]").click(function (event) 
	   {
           var is_default=$(this).val();
           var webhookid = $(this).parent().parent().find("td[name=project_webhookid]").text().trim();
           $.post(rootUri + "/" + webhookid + "/set_default",{"WHIsDefault":is_default}, function(data, status) {
					if (data == "True") {
						window.location.href = rootUri;
					} else {
						init_notification('error', data, true);
					}
		   });
       });
	}
	
	
	function perform_webhook()
	{
	   $("button[name=project_webhook_perform]").click(function () 
	   {
           var webhookid = $(this).parent().parent().find("td[name=project_webhookid]").text().trim();
           $.post("/project/webhook/" + webhookid + "/perform",function(data, status) {
					if (data == "True") {
					    init_notification('success',"测试请求已经发送成功", true);
					} else {
						init_notification('error', data, true);
					}
		   });
       });
	}
	

	//初始化提示框信
	function init_notification(template, data, autlClose) {
		$("#operation_notification").jqxNotification({
			width : 250,
			// position : "bottom-right",
			opacity : 0.8,
			autoOpen : false,
			animationOpenDelay : 300,
			autoClose : autlClose,
			template : template,
			appendContainer: "#notification_container",
		});
		$("#operation_notification_message").empty();
		$("#operation_notification_message").append(data);
		$("#operation_notification").jqxNotification("open");
	}

	function check_object_is_null(o, message) {
		if (!(o.val().length > 0)) {
			o.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		} else {
			return true;
		}
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
 	
 	
 	
 //###########################################版本相关#############################################
 	
 	function update_version_number() {
		$("span[name=project_version_number]").blur(function() {
			var loader = $(this).parent().find("span[name=version_update_loader]");
			// loader.show();
			console.log("dsfds");
			var version_id = $(this).parent().parent().find("span[name=project_version_id]").text().replace('#', '');
            console.log(version_id);
			var version_number = $(this).text().trim();
            console.log(version_number);
			if (version_number != "") {
                $.post(rootUri + "/" + version_id + "/update_version", {
                    "VVersion": version_number
                }, function (data, status) {
                    if (data == "True") {
                        loader.hide();
                    } else {
                        loader.hide();
                        init_notification('error', data);
                    }
                });
            }
		});
	}

	function delete_version() {
		$("span[name=project_version_delete]").click(function() {
			var version_id = $(this).parent().parent().parent().parent().children("div:eq(0)").find("span[name=project_version_id]").text().replace('#', '');
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post(rootUri + "/" + version_id + "/delete", function(data, status) {
					if (data == "True") {
						location = location;
					} else {
						init_notification('error', data);
					}
				});
			});
		});

	}

	function create_version_press_enter() {
		$("#project_add_version").keydown(function(e) {
			if (e.keyCode == 13) {
				submit_version_info($(this).val());
			}

		});
	}

	function create_version_click() {
		$("span[name=project_create_version]").click(function() {
			var version_value = $("#project_add_version").val();
			submit_version_info(version_value);
		});
	}

	function submit_version_info(version_value) {
		if (version_value.length > 0) {
			console.log(rootUri);
			$.post(rootUri + "/create", {
				"VVersion" : version_value.trim()
			}, function(data, status) {
				if (data == "True") {
					location = location;
				} else {
					init_notification('error', data, true);
				}
			});
		} else {
			init_notification('error', "版本号不能为空", true);
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
				update_date($(this).parent().find(target), selecteddate);
			});
		});

	}

	function update_date(target, date_time) {
		var loader = $(target).parent().parent().parent().find("span[name=version_update_loader]");
		loader.show();
		var version_id = $(target).parent().parent().parent().parent().find("span[name=project_version_id]").text().replace('#', '');
		var target_name = $(target).attr('name');
		var parameters={};
		parameters[target_name]=date_time;
		$.post(rootUri + "/" + version_id + "/update_date",parameters, function(data, status) {
			if (data == "True") {
				loader.hide();
			} else {
				loader.hide();
				init_notification('error', data,true);
			}
		});
	}

//#####################################模块相关##################################################

	function update_module_name() {
		$("span[name=project_module_name]").blur(function() {
			var module_id = $(this).parent().find("span[name=project_module_id]").text().replace('#', '');
			var module_name = $(this).text().trim();
			if (module_name != "") {
				$.post(rootUri + "/" + module_id + "/update_name", {
					"field_name" :"Name",
					"field_value" :module_name,
				}, function(data, status) {
					if (data == "True") {
						init_notification('success',"模块名称更新成功！");
					} else {
						init_notification('error', data);
					}
				});
			}
		});
	}
	
	function update_module_desc() {
		$("span[name=project_module_desc]").blur(function() {
			var module_id = $(this).parent().parent().parent().find("span[name=project_module_id]").text().replace('#', '');
			var desc = $(this).text().trim();

			if (desc != "") {
				$.post(rootUri + "/" + module_id + "/update_desc", {
					"field_name" :"Description",
					"field_value" :desc,
				}, function(data, status) {
					if (data == "True") {
						init_notification('success',"模块名称更新成功！");
					} else {
						init_notification('error', data);
					}
				});
			}
		});
	}

	function delete_module() {
		$("span[name=project_module_delete]").click(function() {
			var module_id = $(this).parent().parent().parent().parent().children("div:eq(0)").find("span[name=project_module_id]").text().replace('#', '');
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post(rootUri + "/" + module_id + "/delete", function(data, status) {
					if (data == "True") {
						location = location;
					} else {
						init_notification('error', data);
					}
				});
			});
		});

	}

	function create_module_press_enter() {
		$("#project_add_module").keydown(function(e) {
			if (e.keyCode == 13) {
				submit_module_info($(this).val());
			}

		});
	}

	function create_module_click() {
		$("span[name=project_create_module]").click(function() {
			var module_value = $("#project_add_module").val();
			submit_module_info(module_value);
		});
	}

	function submit_module_info(module_value) {
		if (module_value.length > 0) {
			console.log(rootUri);
			$.post(rootUri + "/create", {
				"Name" : module_value.trim()
			}, function(data, status) {
				if (data == "True") {
					location = location;
				} else {
					init_notification('error', data, true);
				}
			});
		} else {
			init_notification('error', "模块名称不能为空", true);
		}

	}
    

});
