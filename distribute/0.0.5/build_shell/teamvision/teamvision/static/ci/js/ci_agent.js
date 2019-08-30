$(document).ready(function() {
	var theme = 'bootstrap';

	init_page();
	select_menu_item();
	show_tag_popmenu();

	//初始化task 相关页面
	function init_page() {
		/*初始化页面元素*/
		try {
			$("span[name=loader]").hide();
			$("div[name=project-task-tags]").hide();
		} catch(e) {

		}
	}


	//show select menu
	function show_tag_popmenu() {
		$("span[name=add_tag]").click(function() {
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

	


	function select_menu_item() {
		$("input[name=context_search_input]").parent().nextAll().each(function() {
			$(this).click(function(e) {
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
				} else {
					firstChild.addClass('fa-check');
					add_item($(this), labelid, background, text, item_role);
				}

				menu_item_change_trigger($(this), item_role);

			});
		});
	}

	function menu_item_change_trigger(currentitem, role) {
		if (role == "tag-inline") {
			set_task_tag($(currentitem));
		}

	}

	

	function set_task_tag(target) {
		var labelid = "";
		$(target).parent().parent().parent().parent().parent().children("span[labelid]").each(function() {
			labelid = labelid + $(this).attr("labelid").trim() + ",";
		});
		var task_id = $(target).parent().parent().parent().parent().parent().parent().find("span[name=ci_task_id]").text().replace('#', '');
		update_task_property("Tags", labelid, task_id, false);
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

	function add_item(currentitem, labelid, background, text, role) {
		if (role == "tag-inline") {
			var insertElement = "<span class='label label-default visible-lg-inline-block' labelid='" + labelid + "' style='background-color:" + background + "; opacity:0.5;font-size:8px !important;'>" + text + "</span>";
			var insertedElement = currentitem.parent().parent().parent().parent().parent().children('span:eq(0)');
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
			var ci_task_id = $("#ci_config_task").attr("task_id");
			$.ajax({
				url : "/ci/task/" + ci_task_id + "/config/save_task_config",
				type : "post",
				dataType : "json",
				data : {
					section : section_config_data
				},
				success : function(data) {
					alert(data);
				}
			});
		});

	}

	//get section config

	function get_section_config(section_id) {
		var widgetIdsSerialized = $("#" + section_id).jqxSortable("serialize", {
			key : "ci_plugin"
		});
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
			data["is_enable"]=$("#" + id).find("span[name=ci_plugin_enabled]:eq(0)").text();
			data["plugin_id"] = $("#" + id).attr('plugin_id');
			if (section_id == "ci_basic_info_items") {
				data["agent_condations"] = get_basic_agent_filter_condations();
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
			str += items[i].value;
			if (i < items.length - 1) {
				str += ",";
			}
		}
		alert(str);
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
	click_plugin_enalbe();
	function click_plugin_enalbe()
	{
		$("span[name=ci_plugin_enabled]").click(function(){
			if($(this).text()=="On")
			{
			  $(this).text("Off");
			  $(this).css("background","gray");
			}
			else
			{
				$(this).text("On");
				$(this).css("background","green");
			}
		});
	}

	/*################################### 通用方法 #############################*/
	//初始化combobox
	function init_combo_box(element_name, is_multi) {
		$("select[name=" + element_name + "]").jqxComboBox({
			theme : theme,
			width : 300,
			height : 33,
			autoComplete : true,
			searchMode : 'containsignorecase',
			multiSelect : is_multi
		});
	}

});
