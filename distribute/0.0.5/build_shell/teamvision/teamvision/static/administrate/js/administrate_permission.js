$(document).ready(function() {
	var theme = 'metro';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	var window_height=$(window).height();
	$(".admin-panel-body-nonbackground").css('max-height',(window_height-200)+"px");
    create_new_permission();
    delete_permission();
    update_permission_title();
    update_permission_description();
	
	
	function create_new_permission() {

		$("#admin_permission_add").click(function() {
			$("#popup-dialog-container").load("/administrate/permission/create_dialog", function() {
				$("#newpermission-popup-dialog").modal('show');
				$("#permission_type").jqxDropDownList({theme:'bootstrap'});
				submit_create_permission_form();
			});
		});

	}

	function submit_create_permission_form() {
		$("#permission_create_button").click(function() {

			if (validate_permission()) {
				$("#newpermission-popup-dialog").modal('hide');
				$.post("/administrate/permission/create", $('#permission_create_form').serialize(), function(data, status) {
					if (data == "True") 
					{
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
	
	
	
	
	function update_permission_title() {
		$("span[name=permission_name]").blur(function() 
		{
			var permission_name=$(this).text().trim();
			if (permission_name!="") {
				var permission_id=$(this).parent().find("input[name=permission_id]").val();
				$.post("/administrate/permission/"+permission_id+"/update_name",{"permission_name":permission_name}, function(data, status) {
					if (data == "True") 
					{
						init_notification("success","名称更新成功", true);
					} 
					else 
					{
						init_notification("error", data, false);
					}
				});
			}
		});
	}
	
	
	function update_permission_description() {
		$("span[name=permission_desc]").blur(function() 
		{
			var permission_desc=$(this).text().trim();
			if (permission_desc!="") {
				var permission_id=$(this).parent().parent().children("div:eq(0)").find("input[name=permission_id]").val();
				$.post("/administrate/permission/"+permission_id+"/update_desc",{"permission_desc":permission_desc}, function(data, status) {
					if (data == "True") 
					{
						init_notification("success","权限描述更新成功", true);
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
	function delete_permission() {
		$("span[name=permission_delete]").click(function()
		 {
			var permission_id = $(this).parent().parent().children("div:eq(0)").find("input[name=permission_id]").val().trim();
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post("/administrate/permission/delete",{"permission_id":permission_id},function(data, status) {
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
	
	

	function validate_permission() {
		var permission_title = $("#permission_title"), permission_key = $("#codename"), permission_desc= $("#permission_desc");
		allFields = $([]).add(permission_title).add(permission_key).add(permission_desc);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(permission_title, "权限名称不能为空");
		valid = valid && check_permission_rule(permission_key,/^[A-Z]{5,50}/,"权限Key为5-50个大写字母，下划线的组合");
		valid = valid && check_permission_filed_exists("codename",permission_key,"权限Key已经存在");
		valid = valid && check_permission_rule(permission_desc,/[\s\S]*/,"权限描述为5-255个字符");
		return valid;
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
	
	function check_permission_rule(permission_filed,rule,message)
	 {
		if (rule.test(permission_filed.val())) {
			return true;
		} else 
		{
			permission_filed.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		}

	}
	
	function check_permission_filed_exists(filed_name, filed, message) {
		var result=true;
		var filed_value = filed.val().trim();
		$.ajax({
			async : false,
			type : "POST",
			url : "/administrate/permission/check_value_exists",
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
