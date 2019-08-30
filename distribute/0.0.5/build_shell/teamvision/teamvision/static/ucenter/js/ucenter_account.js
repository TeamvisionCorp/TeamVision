$(document).ready(function() {
	var theme = 'bootstrap';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	
	upload_avatar_file();
	select_system_avatar();
	save_avatar();
	save_user_info();
	change_password();


    function change_password()
    {
    	$("#save_password").click(function(){
    		if(validate_password())
    		{
    		  $.post("/ucenter/account/change_password",$("#user_password_form").serialize(),function(data,status){
    		  	if (data == "True") {
						init_notification('success', "密码修改成功", true);
					} else {
						init_notification('error', data, true);
					}
    		  });	
    		}
    	});
    }
    
    
    function validate_password()
    {
    	var old_password = $("#old_password"), new_password = $("#new_password"), confirm_password = $("#confirm_password");
		allFields = $([]).add(old_password).add(new_password).add(confirm_password);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(old_password, "请输入当前密码");
		valid = valid && check_object_is_null(new_password, "请输入新密码");
		valid = valid && check_object_is_null(confirm_password, "请再次输入新密码确认");
		valid = valid && confirm_password_equal(new_password,confirm_password, "新密码两次输入不一致，请重新输入");
		return valid;
    }
    
    /*检查两次密码输入是否一致*/
    function confirm_password_equal(new_password,confirm_password,message)
    {
    	if(new_password.val()!=confirm_password.val())
    	{
    		new_password.parent().parent().addClass("has-error");
    	    confirm_password.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
    	}
    	else
    	{
    		return true;
    	}
    }
	

	function upload_avatar_file() {

		$(".avatar_upload_input").change(function() {
			var file_path = $(this).val();
			var user_id = $("#user_id").val();
			if (file_path) 
			{
				$("#upload_user_avatar").trigger("click");
			}
			// $("mark[name=filepath]").text($(this).val());
		});

	}

	function select_system_avatar() {

		$("img[name=system_user_avatar]").click(function() {
			$("#user_avatar").attr("src", $(this).attr('src'));
			$("img[name=system_user_avatar]").removeClass('selected_avatar');
			$(this).addClass('selected_avatar');
		});
	}

	function save_avatar() {
		$("#save_user_avatar").click(function() {
			var user_avatar = $("#user_avatar").attr("src");
			$.post("/ucenter/account/update_avatar", {
				"avatar" : user_avatar
			}, function(data, status) {
			});

		});

	}

	function save_user_info() {
		$("#save_user_info").click(function() {
			if (validate_user_info()) {
				$.post("/ucenter/account/update_user_info", $('#user_info_form').serialize(), function(data, status) {
					if (data == "True") {
						init_notification('success', "用户信息保存成功", true);
					} else {
						init_notification('error', data, true);
					}
				});

			}

		});
	}

	function validate_user_info() {
		var last_name = $("#last_name"), first_name = $("#first_name"), email = $("#email");
		allFields = $([]).add(last_name).add(first_name).add(email);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(last_name, "姓氏不能为空");
		valid = valid && check_object_is_null(first_name, "名字不能为空");
		valid = valid && check_object_is_null(email, "用户邮箱不能为空");
		return valid;
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

	function check_object_is_null(o, message) 
	{
		if (!(o.val().length > 0)) 
		{
			o.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		} 
		else 
		{
			return true;
		}
	}

});
