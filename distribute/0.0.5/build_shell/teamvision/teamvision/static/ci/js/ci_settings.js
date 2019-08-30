$(document).ready(function() {
	var theme = 'bootstrap';

	init_page();
	create_credential();
	save_credential();
	delete_credential();
	create_server();
	save_server();
	delete_server();
	show_create_agent_dialog();
	show_edit_agent_dialog();
	create_task_tag_click();
	create_task_tag_press_enter();
	update_task_tag_name();
	// select_menu_item();
	// show_tag_popmenu();

	//初始化task 相关页面
	function init_page() {
		/*初始化页面元素*/
			init_dropdown_list("CredentialType");
		    init_dropdown_list("Credential");
			hide_sshkey_box();
			change_credential_type();

	}
	
	
	function hide_sshkey_box()
	{
		try{
		    
		    var value=$("#CredentialType").jqxDropDownList('getSelectedItem').value;
		if(value==1)
		{
			$("#ssh_key").hide();
		}
		else
		{
			$("#ssh_key").show();
		}
		   	
		}
		catch(e)
		{
			console.log(e);
		}
		
	}
	
	
	function change_credential_type()
	{
		$("#CredentialType").on('change',function(event){
			var item = event.args.item;
			hide_sshkey_box();
		});
	
		
	}
	
	
	function create_credential()
	{
		$("#ci_add_credential").click(function(){
			$.post("/ci/settings/credentials/credential_create", $('#ci_credential_create_form').serialize(), function(data, status) {
					if (data == "True") 
					{
						window.location.href=window.location.href;
					} else {
						init_notification('error', data);
					}
				});
		});
	}
	
	
	function save_credential()
	{
		$("#ci_save_credential").click(function(){
			$.post("/ci/settings/credentials/credential_edit", $('#ci_credential_create_form').serialize(), function(data, status) {
					if (data == "True") 
					{
						window.location.href="/ci/settings/credentials";
					} else {
						init_notification('error', data);
					}
				});
		});
	}
	
	
	function delete_credential()
	{
		$("span[name=delete_credential]").click(function(){
			var ci_credentialid=$($(this).parent().parent().find("td[name=ci_credentialid]")[0]).text();
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post("/ci/settings/credentials/"+ci_credentialid+"/delete", function(data, status) {
					if (data == "True") 
					{
						location = location;
					} else {
						init_notification('error', data,true);
					}
				});
			});
		});
	}
	
	
	
	//server 相关配置
	
	function create_server()
	{
		$("#ci_add_server").click(function(){
			$.post("/ci/settings/servers/server_create", $('#ci_server_create_form').serialize(), function(data, status) {
				
					if (data == "True") 
					{
						window.location.href=window.location.href;
					} else {
						init_notification('error', data);
					}
				});
		});
	}
	
	
	function save_server()
	{
		$("#ci_save_server").click(function(){
			$.post("/ci/settings/servers/server_edit", $('#ci_server_create_form').serialize(), function(data, status) {
					if (data == "True") 
					{
						window.location.href="/ci/settings/servers";
					} else {
						init_notification('error', data);
					}
				});
		});
	}
	
	
	function delete_server()
	{
		$("span[name=delete_server]").click(function(){
			var ci_serverid=$($(this).parent().parent().find("td[name=ci_serverid]")[0]).text();
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.post("/ci/settings/servers/"+ci_serverid+"/delete", function(data, status) {
					if (data == "True") 
					{
						location = location;
					} else {
						init_notification('error', data,true);
					}
				});
			});
		});
	}
	
	
/*#######################################agent创建###########################################*/

function show_create_agent_dialog()
{
	$("#ci_agent_add").click(function(){
		$("#popup-dialog-container").load("/ci/settings/agent/0/create_dialog",function(){
			$("#new_ci_agent_popup_dialog").modal('show');
			init_dropdown_list('OS',false);
			init_dropdown_list('AgentTags',true);
			submit_agent_form();
			
		});
	});
}

function show_edit_agent_dialog()
{
	$("span[name=ci-agent_title]").click(function(){
		var agent_id=$(this).attr('agent_id');
		$("#popup-dialog-container").load("/ci/settings/agent/"+agent_id+"/create_dialog",function(){
			$("#new_ci_agent_popup_dialog").modal('show');
			init_dropdown_list('OS',false);
			init_dropdown_list('AgentTags',true);
			submit_agent_form();
			
		});
	});
	
}


function submit_agent_form()
{
	$("#ci_agent_create_button").click(function(){
		var agent_id=$("#ci_agent_id_create").val();
		if(validate_ci_agent())
		{
			$("#new_ci_agent_popup_dialog").modal('hide');
		$.post("/ci/settings/agent/"+agent_id+"/create",$('#ci_agent_create_form').serialize(),function(data,status){
			if(data=="True")
			{
				location = location;
			}
			else
			{
				init_notification('error', data,true);
			}
		});
		}
	});
	}


function validate_ci_agent() {
	var ci_agent_name = $("#ci_agent_name"),ci_agent_ip=$("#ci_agent_ip"),ci_agent_port=$("#ci_agent_port"),ci_agent_workspace=$("#ci_agent_workspace");
	var ci_agent_executors=$("#ci_agent_executors")
	allFields = $([]).add(ci_agent_name).add(ci_agent_ip).add(ci_agent_port).add(ci_agent_workspace).add(ci_agent_executors);
	var valid = true;
	allFields.parent().parent().removeClass("has-error");
	valid = valid && check_object_is_null(ci_agent_name, "Agent名称不能为空！");
	valid = valid && check_object_is_null(ci_agent_ip,"Agent IP不能为空");
	valid = valid && check_object_is_ip(ci_agent_ip,"Agent IP格式不正确");
	valid = valid && check_object_is_null(ci_agent_port,"Agent 端口不能为空且必须为数字");
	valid = valid && check_object_is_number(ci_agent_port,"Agent 端口不能为空且必须为数字");
	valid = valid && check_object_is_null(ci_agent_workspace,"Agent远程工作目录不能为空");
	valid = valid && check_object_is_null(ci_agent_executors,"任务执行器个数不能为空且必须为数字");
	valid = valid && check_object_is_number(ci_agent_executors,"任务执行器个数必须为非负数字");
	return valid;
}

/***********************************创建标签******************************************/

function update_task_tag_name() {
	$("span[name=tag_name]").blur(function() {
		console.log('1');
		var tag_id = $(this).parent().find("input[name=tag_id]").val();
		var tag_name = $(this).text().trim();
		if (tag_name != "") {
			$.post("/ci/settings/tag/"+tag_id+"/create", {
				"TagName" : tag_name
			}, function(data, status) {
				if (data == "True") {
				} else {
					init_notification('error', data);
				}
			});
		}
	});
}

function delete_task_tag() {
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

function create_task_tag_press_enter() {
	$("#ci_add_tag").keydown(function(e) {
		if (e.keyCode == 13) {
			submit_task_tag($(this).val());
		}

	});
}

function create_task_tag_click() {
	$("span[name=ci_add_tag]").click(function() {
		var tag_value = $("#ci_add_tag").val();
		submit_task_tag(tag_value);
	});
}

function submit_task_tag(tag_value) {
	if (tag_value.length > 0 && tag_value.length<7 ) {
		$.post("/ci/settings/tag/0/create", {
			"TagName" : tag_value.trim()
		}, function(data, status) {
			if (data == "True") {
				location = location;
			} else {
				init_notification('error', data, true);
			}
		});
	} else {
		init_notification('error', "标签名称长度必须是1-6个字符", true);
	}

}
	

/*################################### 通用方法 #############################*/
	//初始化combobox
	function init_dropdown_list(element_name,checkbox) {
			
		try
		{
		  $("select[name=" + element_name + "]").jqxDropDownList({
			theme : theme,
			width : 300,
			height : 33,
			checkboxes:checkbox
		});	
		}
		catch(e)
		{
			console.log(e);
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
	
	function check_object_is_number(o,message)
	{
		var number_rule=/^\d*$/;
		if(number_rule.test(o.val()))
		{
			return true;
		}
		else
			{
			o.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			  false;
			}
	}
	
	function check_object_is_ip(o,message)
	{
		var ip_rule=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
		if(ip_rule.test(o.val()))
		{
			return true;
		}
		else
			{
			o.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			  false;
			}
	}

});
