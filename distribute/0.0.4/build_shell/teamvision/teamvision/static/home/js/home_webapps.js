$(document).ready(function() {
	var rootUri = window.location.href;
	show_create_app_dialog();
	submit_webapp_form();
	remove_webapp();
	webapp_item_mouserover();

	function show_create_app_dialog() {
		$("#home_webapp_add").click(function() {

			$("#webapp-create-dialog").modal('show');
		});
	}
	
	function webapp_item_mouserover() {
		$("div[name=home-webapp-item]").mouseover(function() {
			$(this).addClass("home_project_hover");
			$(this).find("i[name=home_webapp_remove]").show();
		});

		$("div[name=home-webapp-item]").mouseout(function() {
			$(this).removeClass("home_project_hover");
			$(this).find("i[name=home_webapp_remove]").hide();
		});

	}

	function remove_webapp() {
		$("i[name=home_webapp_remove]").click(function(e) {
			var webapp_id = $(this).parent().parent().attr("id");
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post("/home/webapps/remove", {
					"webapp_id" : webapp_id
				}, function(data, status) {
					if (data == "True") {
						window.location.href = rootUri;
					} else {
						init_notification("error", data, false);
					}
				});
			});
			e.stopPropagation();
		});
	}

	function submit_webapp_form() {
		$("#webapp_create_button").click(function() {

			if (validate_webapp()) {
				$("#webapp-create-dialog").modal('hide');
				$.post("/home/webapps/create", $('#home_webapp_create_form').serialize(), function(data, status) {
					if (data == "True") {
						window.location.href = rootUri;
					} else {
						init_notification("error", data, false);
					}
				});
			}
		});
	}

	function validate_webapp() {
		var app_title = $("#app_title"), app_key = $("#app_key"), app_url = $("#app_url");
		allFields = $([]).add(app_title).add(app_key).add(app_url);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(app_title, "请输入工具名称");
		valid = valid && check_object_is_null(app_key, "请输入工具key");
		valid = valid && check_app_key(app_key, "工具key长度为3-10个英文字符");
		valid = valid && check_object_is_null(app_url, "请输入工具url");
		valid = valid && check_app_url(app_url, "url格式不正确,请以http开头");
		
		return valid;
	}

	function check_app_key(app_key, message) {
		var express = /^[a-zA-Z]{3,10}/;
		if (express.test(app_key.val())) {
			return true;
		} else {
			app_key.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		}

	}
	
	function check_app_url(app_url, message) {
		var express = /^http:/;
		if (express.test(app_url.val())) {
			return true;
		} else {
			app_url.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		}

	}

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

	function init_notification(template, data, autoclose) {
		$("#operation_notification").jqxNotification({
			width : 250,
			position : "bottom-right",
			opacity : 0.8,
			autoOpen : false,
			animationOpenDelay : 300,
			autoClose : autoclose,
			template : template
		});
		$("#operation_notification_message").empty();
		$("#operation_notification_message").append(data);
		$("#operation_notification").jqxNotification("open");
	}

});
