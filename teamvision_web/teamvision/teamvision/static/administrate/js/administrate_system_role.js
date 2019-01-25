$(document).ready(function() {
	var theme = 'metro';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	var window_height=$(window).height();
	$(".admin-panel-body-nonbackground").css('max-height',(window_height-200)+"px");
    
	create_group_press_enter();
	create_group_click();
	delete_user_group();
	update_group_permission();
	update_group_description();
	
	
	function create_group_press_enter()
	{
		$("#usergroup_name").keydown(function(e) {
			if (e.keyCode == 13) {
				submit_group_info($(this));
			}

		});
	}

	function create_group_click() 
	{
		$("span[name=usergroup_create_group]").click(function() 
		{
			var group_name = $("#usergroup_name");
			submit_group_info(group_name);
		});
	}

	function submit_group_info(group_name) {
		if (validate_usergroup(true))
		{
			$.post("/administrate/systemrole/create", 
			{
				"group_name" : group_name.val().trim()
			}, function(data, status) {
				if (data == "True") 
				{
				   // window.location.href=rootUri;
				   load_user_group_list();
				} else 
				{
					init_notification('error', data, true);
				}
			});
		}
	}
	
	function update_group_permission()
	{
		$("i[name=user_group_active_permission]").click(function()
		{
			var group_id=$("#group_id").val();
			var permission_id = $(this).parent().parent().parent().children("div:eq(0)").find("input[name=permission_id]").val().trim();
			var active=$(this).attr("active");
			if(active=="0")
			{
				active=1;
				$(this).removeClass("fa-toggle-off");
				$(this).addClass("fa-toggle-on");
			}
			else
			{
				$(this).removeClass("fa-toggle-on");
				$(this).addClass("fa-toggle-off");
				active=0;
			}
			
			$.post("/administrate/systemrole/"+group_id+"/update_permission",{"permission_id":permission_id,"active":active},function(data,status)
			{
				if (data == "True") 
					{
						load_group_permission_list();
						// load_user_group_list();
					} else {
						init_notification('error', data,true);
					}
			});
		});
	}
	
	
	function update_group_description() {
		$("span[name=user_group_description]").blur(function() 
		{
			var group_desc=$(this).text().trim();
			if (group_desc!="") {
				var groupid = $(this).parent().parent().parent().children("div:eq(0)").find("span[name=user_group_id]").attr("labelid").trim();
				$.post("/administrate/systemrole/"+groupid+"/update_description",{"group_desc":group_desc}, function(data, status) {
					if (data == "True") 
					{
						init_notification("success","用户组描述更新成功", true);
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
	function delete_user_group() {
		$("span[name=usergroup_delete]").click(function()
		 {
			var groupid = $(this).parent().parent().children("div:eq(0)").find("span[name=user_group_id]").attr("labelid").trim();
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() 
			{
				$("#object_delete_confirm").modal('hide');
				$.post("/administrate/systemrole/"+groupid+"/delete",function(data, status) {
					if (data == "True") 
					{
						window.location.href=rootUri;
						// load_user_group_list();
					} else {
						init_notification('error', data,true);
					}
				});
			});
		});

	}
	
	
	
	function load_user_group_list()
	{
	    $("#user_group_list").load("/administrate/systemrole/usergroup_list",{"filter":"all"},function()
	    {
	       delete_user_group();	
	    });	
	}
	
	function load_group_permission_list()
	{
		var group_id=$("#group_id").val();
	    $("#group_permission_list").load("/administrate/systemrole/"+group_id+"/group_permission_list",{"filter":"all"},function(data,status)
	    {
	       update_group_permission();
	    });	
	}
	

	function validate_usergroup(is_create) {
		var group_name = $("#usergroup_name");
		allFields = $([]).add(group_name);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(group_name, "用户组名称不能为空");
		valid = valid && check_user_group_filed_exists("group_name",group_name, "该用户组名已经存在");
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
	
	function check_user_group_filed_exists(filed_name, filed, message) {
		var result=true;
		var filed_value = filed.val().trim();
		$.ajax({
			async : false,
			type : "POST",
			url : "/administrate/systemrole/check_value_exists",
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
