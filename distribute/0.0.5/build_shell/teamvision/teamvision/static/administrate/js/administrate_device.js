$(document).ready(function() {
	var theme = 'metro';
	var rootUri = window.location.href;
	var window_height=$(window).height();
	
	var currentTrigger = null;
	var currentoPopObject = null;
	submit_create_device_form();
	lend_device();
	return_device();
    delete_device();
	init();
	
	
	function init(){
		$(".admin-panel-body-nonbackground").css('max-height',(window_height-200)+"px");
		$("#DeviceOS").jqxDropDownList({theme:'bootstrap'});
		$("#DeviceType").jqxDropDownList({theme:'bootstrap'});
		$("#DeviceOSVersion").jqxDropDownList({theme:'bootstrap'});
		$("#DeviceScreenSize").jqxDropDownList({theme:'bootstrap'});
		$("#device_borrowser").jqxComboBox({theme:'bootstrap'});
	}
	
	
	
	$("#DeviceOS").change(function(){
		var device_os=$(this).val();
		$("#DeviceOSVersion_jqxDropDownList").load("device/version_controll",{"device_os":device_os},function(data,status){
		$("#DeviceOSVersion").jqxDropDownList("loadFromSelect","DeviceOSVersion_jqxDropDownList");
			
		});
	});
	
	function lend_device()
	{
		$("span[name=device_lend]").click(function(){
			var device_id=$(this).parent().parent().children("div:eq(0)").find("input[name=device_id]").val();
			$("#popup-dialog-container").load("/administrate/device/confirm_dialog",{"device_id":device_id},function(){
				$("#device_borrow_confirm").modal('show');
				$("#device_borrow_confirm_button").click(function(){
					$.post("/administrate/device/lend",{"device_id":device_id},function(data,status)
					{
						if (data == "True") 
					{
						window.location.href=rootUri;
					} 
					else 
					{
						init_notification("error", data, false);
					}
				        
			        });
				});
			});
		}
			
		);
	}
	
	function return_device()
	{
		$("span[name=device_return]").click(function(){
			var device_id=$(this).parent().parent().children("div:eq(0)").find("input[name=device_id]").val();
			$("#popup-dialog-container").load("/administrate/device/confirm_dialog",{"device_id":device_id},function(){
				$("#device_borrow_confirm").modal('show');
				$("#device_borrow_confirm_button").click(function(){
					
					$.post("/administrate/device/return",{"device_id":device_id},function(data,status)
					{
						if (data == "True") 
					{
						window.location.href=rootUri;
					} 
					else 
					{
						init_notification("error", data, false);
					}
				
			        });
					
				});
			});
		}
			
		);
	}
	
	
	
	

	function submit_create_device_form() {
		$("#save_device").click(function() {
			var form_action=$("#device_create_form").attr("action").trim();
			if (validate_device()) {
				
				$.post(form_action, $('#device_create_form').serialize(), function(data, status) {
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
	
	
	

	

	//删除任务
	function delete_device() {
		$("span[name=device_delete]").click(function()
		 {
			var device_id = $(this).parent().parent().children("div:eq(0)").find("input[name=device_id]").val().trim();
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post("/administrate/device/delete",{"device_id":device_id},function(data, status) {
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
	
	

	function validate_device() {
		var device_name = $("#DeviceName"), device_number = $("#DeviceNumber");
		allFields = $([]).add(device_name).add(device_number);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(device_name, "设备名称不能为空");
		valid = valid && check_device_rule(device_name,/[\s\S]{3,50}/,"设备名称为3-100个字符");
		valid = valid && check_device_rule(device_number,/[a-z,A-Z]?\d{1,10}$/,"设备编号为10位以内的数字");
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
	
	function check_device_rule(device_filed,rule,message)
	 {
		if (rule.test(device_filed.val())) {
			return true;
		} else 
		{
			device_filed.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		}

	}
	
	function check_device_filed_exists(filed_name, filed, message) {
		var result=true;
		var filed_value = filed.val().trim();
		$.ajax({
			async : false,
			type : "POST",
			url : "/administrate/device/check_value_exists",
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
