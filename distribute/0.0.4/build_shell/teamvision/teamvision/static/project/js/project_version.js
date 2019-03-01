$(document).ready(function() {

	var rootUri = window.location.href;
	init_page();

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
	//更新版本号

	function init_page() {
		$("span[name=version_update_loader]").hide();
	}

	function update_version_number() {
		$("span[name=project_version_number]").blur(function() {
			var loader = $(this).parent().find("span[name=version_update_loader]");
			loader.show();
			var version_id = $(this).parent().parent().find("span[name=project_version_id]").text().replace('#', '');
			var version_number = $(this).find("span[name=VVersion]").text().trim();
			if (version_number != "") {
				$.post(rootUri + "/" + version_id + "/update_version", {
					"VVersion" : version_number
				}, function(data, status) {
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

	/*点击元素之外的地方隐藏控件*/
	function hide_control_byclick_page(hide_object, trigger) {

		trigger.click(function(e)
		{
			e.stopPropagation();
			e.preventDefault();
		});

		$(document).on('click', function(e) {
			if ($(e.target).html() != hide_object.html() && $(e.target).html() != "") {
				hide_object.hide();
			}
		});
	}

});
