$(document).ready(function() {
	var theme = 'metro';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	var window_height=$(window).height();
	$(".admin-panel-body-nonbackground").css('max-height',(window_height-200)+"px");
    create_new_user();
    delete_user();
    submit_edit_user_form();
    update_user_group();
    reset_user_password();
	// init_page();

	// show_tag_popmenu();

	// select_menu_item();


	// click_check();
	
	// show_member_popmenu("span[name=task-add-owner]");
	// show_member_popmenu("span[name=task_edit_owner]");
	
	// delete_task();
	
	
	
	function create_new_user() {

		$("#admin_user_add").click(function() {
			$("#popup-dialog-container").load("/administrate/user/create_dialog", function() {
				$("#newuser-popup-dialog").modal('show');
				submit_create_user_form();
			});
		});

	}

	function submit_create_user_form() {
		$("#user_create_button").click(function() {

			if (validate_user(true)) {
				$("#newuser-popup-dialog").modal('hide');
				$.post("/administrate/user/create", $('#user_create_form').serialize(), function(data, status) {
					if (data == "True") 
					{
						// load_user_list();
						window.location.href=rootUri;
					} 
					else 
					{
						init_notification("error", data, false);
					}
				});
			}
		});
	}
	
	function submit_edit_user_form() {
		$("#edit_user_save_user").click(function() 
		{
			if (validate_user(false)) {
				var user_id=$("#edit_user_id").val();
				$.post("/administrate/user/"+user_id+"/edit_post", $('#edit_user_form').serialize(), function(data, status) {
					if (data == "True") 
					{
						init_notification("success","用户信息更新成功", true);
					} 
					else 
					{
						init_notification("error", data, false);
					}
				});
			}
		});
	}
	
	
	function update_user_group() {
		$("#edit_user_save_auth").click(function() 
		{
			if (validate_user(false)) {
				var user_id=$("#edit_user_id").val();
				$.post("/administrate/user/"+user_id+"/update_group", $('#update_user_group').serialize(), function(data, status) {
					if (data == "True") 
					{
						init_notification("success","权限设置成功", true);
					} 
					else 
					{
						init_notification("error", data, false);
					}
				});
			}
		});
	}
	
	function reset_user_password() {
		$("#edit_user_reset_password").click(function() 
		{
			if (validate_password()) 
			{
				var user_id=$("#edit_user_id").val();
				$.post("/administrate/user/"+user_id+"/reset_password", $('#reset_user_password').serialize(), function(data, status) {
					if (data == "True") 
					{
						init_notification("success","密码重置成功", true);
					} 
					else 
					{
						init_notification("error", data, false);
					}
				});
			}
		});
	}
	

	//删除任务
	function delete_user() {
		$("span[name=user_delete]").click(function()
		 {
			var user_email = $(this).parent().parent().children("div:eq(1)").find("span[name=user_email]").text().trim();
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post("/administrate/user/delete",{"email":user_email},function(data, status) {
					if (data == "True") 
					{
						window.location.href=rootUri;
					} else {
						init_notification('error', data,true);
					}
				});
			});
		});

	}
	
	
	
	function load_user_list()
	{
	    $("#user_list").load("/administrate/user/user_list",{"filter":"all"},function()
	    {
	    	
	    });	
	}
	

	function validate_user(is_create) {
		var user_email = $("#email"), new_password = $("#new_password"), confirm_password = $("#confirm_password"),last_name=$("#last_name"),first_name=$("#first_name");
		allFields = $([]).add(user_email).add(new_password).add(confirm_password).add(last_name).add(first_name);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(user_email, "用户邮箱不能为空");
		if(is_create)
		{
		  valid = valid && check_user_filed_exists("email",user_email, "该邮箱已经存在");
		  valid = valid && check_object_is_null(new_password, "请输入新密码");
		  valid = valid && check_object_is_null(confirm_password, "请再次输入新密码确认");
		  valid = valid && confirm_password_equal(new_password,confirm_password, "新密码两次输入不一致，请重新输入");	
		}
		valid = valid && check_object_is_null(last_name, "姓氏不能为空");
		valid = valid && check_object_is_null(first_name, "名字不能为空");
		return valid;
	}
	
	
	function validate_password() {
		var new_password = $("#new_password"), confirm_password = $("#confirm_password");
		allFields = $([]).add(new_password).add(confirm_password);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
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
	
	
	function check_object_is_null(o, message) {
		if (!(o.val().length > 0)) {
			o.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		} else {
			return true;
		}
	}
	
	function check_user_filed_exists(filed_name, filed, message) {
		var result=true;
		var filed_value = filed.val().trim();
		$.ajax({
			async : false,
			type : "POST",
			url : "/administrate/user/check_value_exists",
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
	
});
