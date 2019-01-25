$(document).ready(function() {
	var theme = 'bootstrap';

	init_page();
	create_service_press_enter();
    create_service_click();
    upload_file();
    // add_replace_config();
    // remove_replace_config();
    save_service_basic();
    save_service_replace_config();
    delete_service_file();

	//初始化service 相关页面
	function init_page() {
		/*初始化页面元素*/
		try {
			copy_service();
			delete_service();
			show_service_row_operation_group();
			init_dropdown_list("ci_service_project");
		} catch(e) {

		}
	}
	
	
	
	//copy service
	function copy_service()
	{
		$("span[name=service_copy]").click(function() {
			var ci_service_id = $($(this).parent().parent().parent().find("span[name=ci_service_id]")[0]).text().replace('#', '');
			$.get("/ci/service/" + ci_service_id+"/copy", function(data, status) {
				if (data == "True") {
					$("#ci_task_container").load("/ci/task/get_task_list", {
						"task_id" : ci_task_id,
						"sub_nav_action" : sub_nav_action
					}, function(data, status) {
						init_page();
					});
				} else {
					init_notification('error', data, true);
				}
			});
		});
		
	}
	
	//delete service
	function delete_service()
	{
		$("span[name=service_delete]").click(function() {
			var ci_service_id = $($(this).parent().parent().parent().find("span[name=ci_service_id]")[0]).text().replace('#', '');
			$("#object_delete_confirm").modal('show');
			$("#object_delete_confirm_button").click(function() {
				$("#object_delete_confirm").modal('hide');
				$.get("/ci/service/" + ci_service_id+"/delete", function(data, status) {
					if (data == "True") {
						init_page();
					} else {
						init_notification('error', data, true);
					}
				});
			});
		});
	}
	
	
	
	function create_service_press_enter() {
		$("#ci_add_service").keydown(function(e) {
			if (e.keyCode == 13) {
				submit_service($(this).val());
			}

		});
	}

	function create_service_click() {
		$("span[name=ci_create_service]").click(function() {
			var service_name = $("#ci_add_service").val();
			submit_service(service_name);
		});
	}
	
	
	function delete_service_file() {
		$("span[name=delete_service_file]").click(function() {
			var service_id = $("#ci_service_id").val();
			var service_file_id=$($(this).parent().parent().find("td[name=ci_service_fileid]")[0]).text();
			$.post("/ci/service/delete_file/"+service_file_id,{"service_id":service_id},function(data,status){
				if (data=="True") {
					window.location.href=window.location.href;
				} else {
					init_notification('error', data, true);
				}
			});
		});
	}
	
	
	//添加替换配置输入框
	
	// function add_replace_config()
	// {
		// $("#add_replace_config").click(function(){
			// var controll_html="<div class='input-group' style='margin-bottom:15px;'>\
			// <span class='input-group-addon' name='delete_replace_config'><i class='cursor-hand fa fa-fw fa-trash-o fa-lg' style='color:red'></i></span>\
			// <input type='text' class='form-control input-md'  name='replace_config' placeholder='被替换文件的路径' value=''></div>";
			// $("#replace_config_container").append(controll_html);
			// remove_replace_config();
		// });
	// }
	
	// 删除替换配置
	function remove_replace_config()
	{
		$("span[name=delete_replace_config]").click(function(){
			$(this).parent().remove();
		});
	}
	
	function submit_service(service_name) {
		if (service_name.length > 0) {
			$.post("/ci/service/create", {
				"ServiceName" : service_name.trim()
			}, function(data, status) {
				if (data!="0") {
					window.location.href="/ci/service/"+data+"/config";
				} else {
					init_notification('error', data, true);
				}
			});
		} else {
			init_notification('error', "服务名称不能为空", true);
		}

	}
     
     
    function upload_file() {

		$(".file_upload_input").change(function() {
			var file_path = $(this).val();
			var user_id = $("#service_id").val();
			if (file_path) 
			{
				$("#upload_service_file").trigger("click");
			}
			// $("mark[name=filepath]").text($(this).val());
		});

	}
 

    



	//service row operation
	function show_service_row_operation_group() {
		$(".ci_service_listview_item").mouseover(function() {
			$(this).find('div[name=service_row_operation]').show();
		});
		$(".ci_service_listview_item").mouseout(function() {
			$(this).find('div[name=service_row_operation]').hide();
		});
	}
	
	// 保存服务基本配置信息
    function save_service_basic()
	 {
	 	$("#save_service_basic_info").click(function()
	 	{   
	 	    if(validate_service())
	 	    {
	 	    	var service_id=$("#ci_service_id").val();
	 	    	$.post("/ci/service/"+service_id+"/config_post", $('#ci_service_form').serialize(), function(data, status) 
	 		{   
	 			if(data=="True")
	 			{
	 			   init_notification('success',"修改保存成功！",true);	
	 			 }	
	 			else
	 			{
	 				init_notification('error',data,true);
	 			}
			});
	 	    	
	 	    }
	 	});
	 }
	 
	 $("input[name=replace_targets]").focus(function(){
	 	$(this).removeClass('input-2-label');
	 });
	 
	 // 保存服务文件替换配置
    function save_service_replace_config()
	 {
	 	$("input[name=replace_targets]").blur(function()
	 	{  
	 		$(this).addClass('input-2-label');
	 	    	var service_id=$("#ci_service_id").val();
	 	    	var replace_targets=$(this).val();
	 	    	if(replace_targets=='输入替换文件路径,多个文件以逗号分隔')
	 	    	{
	 	    		replace_targets="";
	 	    	}
	 	    	var file_id=$(this).parent().parent().find("td[name=ci_service_fileid]").text();
	 	    	var file_name=$(this).parent().parent().find("td[name=file_name]").text();
	 	    	$.post("/ci/service/"+service_id+"/replace_config_post",
	 	    	{'file_id':file_id,'file_name':file_name,'replace_targets':replace_targets}, 
	 	    	function(data, status) 
	 		{   
	 			if(data=="True")
	 			{
	 			   init_notification('success',"修改保存成功！",true);	
	 			 }	
	 			else
	 			{
	 				init_notification('error',data,true);
	 			}
			});
	 	});
	 }
	 
	 
	 //验证修改字段值
	 function validate_service() 
	{
		var service_name = $("#ServiceName"), deploy_dir=$("#DeployDir");
		allFields = $([]).add(service_name).add(deploy_dir);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(service_name, "服务名称不能为空！");
		valid = valid && check_object_is_null(deploy_dir, "部署目录不能为空");
		return valid;
	}
	
	
	

	
	function check_object_is_null(o, message) 
	{
	
		if (!($(o).val().length > 0)) 
		{
			o.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;
		} else 
		{
			return true;
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
	
	
	//初始化combobox
	function init_dropdown_list(element_name) {
		$("select[name=" + element_name + "]").jqxDropDownList({
			theme : theme,
			width : 300,
			height : 33
		});
	}

});
