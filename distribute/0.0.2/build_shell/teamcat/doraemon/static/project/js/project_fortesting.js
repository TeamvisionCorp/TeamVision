$(document).ready(function() {
	var theme = 'bootstrap';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	
	show_right_panel();
	
	
	//展现右侧面板
	
	function show_right_panel()
	{
		$("#header-rightbar-filter").click(function(){
			$(".web-app-view-right-panel-default").toggle(500);
		});
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
	
    $("#new_fortesting_item").click(function(){
     $("#head_add_fortesting").trigger('click');
    });
    
    /***************************提测编辑浏览********************************************/
    view_edit_fortesting();


	function view_edit_fortesting() {
		$(".web-board-column-item-default").unbind('click').click(function(event) {
			var project_id=$("#project_id").attr('project_id');
			var test_application=$(this).attr('id');
			if(project_id==null)
				{
				  project_id=0;
				}
			$("#popup-dialog-container").load("/project/fortesting/get_create",{'project_id':project_id,'test_application':test_application}, function() {
				$("div[name=member-list]").hide();
				$("#fortesting_dialog_footer").hide();
				show_member_popmenu();
				select_member_item();
				$("#newfortesting-popup-dialog").modal('show');
				view_edit_click_handler();
				delete_attachment();
			});
		});
	}
	
	//删除已上传附件
	function delete_attachment()
	{
		$("div[name=fortesting_attachment_delete]").click(function(){
			var fortesting_id=$("#fortesting_id").val();
			var file_id=$(this).attr("file_id");
			$.get("/project/fortesting/"+fortesting_id+"/delete_file/"+file_id,function(data,status){
			 });
			$(this).parent().hide();
		});
	}
	
	//在查看和编辑模式之间切换
	function view_edit_click_handler()
	{
		$("#fortesting_view_part").click(function(){
			set_fortesting_view_item_status(this);
			var fortesting_id=$("#fortesting_id").val();
			$("#newfortesting-popup-dialog .modal-body").load("/project/fortesting/"+fortesting_id+"/view_part/0",function(){
				init_fortesting_view();
				$("#fortesting_dialog_footer").hide();
			});
		});
		
		$("#fortesting_edit_part").click(function(){
			set_fortesting_view_item_status(this);
			var fortesting_id=$("#fortesting_id").val();
            $("#newfortesting-popup-dialog .modal-body").load("/project/fortesting/"+fortesting_id+"/view_part/1",function(){
            	$("#fortesting_dialog_footer").show();
            	init_fortesting_edit_form();
        		submit_fortesting_form();
			});
		});
	}
	
	
	//查看模式初始化UI
	function init_fortesting_view()
	{
		$("div[name=member-list]").hide();
		show_member_popmenu();
		select_member_item();
		delete_attachment();
	}
	
	//在UI界面上标示查看和编辑模式
	function set_fortesting_view_item_status(target)
	{
		$(".fortesting_view_edit_active").each(function(){
			   $(this).removeClass("fortesting_view_edit_active");
		   });
		$(target).addClass("fortesting_view_edit_active");
	}
	
	//弹出测试人员选择菜单
	function show_member_popmenu() {
		$("#add_new_tester").click(function() {
			var popmenu = $(this).parent().find("div[name=member-list]");
			currentoPopObject = popmenu;
			currentTrigger = $(this);
			popmenu.show();
			popmenu.addClass("filed-pop-meun");
			hide_control_byclick_page(popmenu, $(this));
			popmenu_search();
		});

	}
	
	//添加或者删除测试人员
	function select_member_item() {
		$("input[name=context_search_input]").parent().nextAll().each(function() {
			$(this).click(function(e) {
				e.stopPropagation();
				var labelid = $(this).attr('labelid');
				var text = $(this).text().trim();
				var background = $(this).children("i:eq(1)").css('color');
				var firstChild = $(this).children("i:eq(0)");
				var imgChild=$(this).find("img");
				var classname = firstChild.attr('class');
				console.log(firstChild);
				if (classname.toUpperCase().indexOf('fa-check'.toUpperCase()) >= 0) {
					firstChild.removeClass('fa-check');
					remove_member(this,labelid);
				} else {
					firstChild.addClass('fa-check');
					add_member(this,labelid,text,imgChild);
				}
			});
		});
	}

	//添加测试人员
	function add_member(targetElement,labelid,text,imgChild) {
		var fortesting_id=$("#fortesting_id").val();
		$.get("/project/fortesting/"+fortesting_id+"/add_tester/"+labelid,function(data,status){
			if(data=="True")
				{
				var new_image=$(imgChild).attr("title",text);
				var ele=$("<span labelid=\""+labelid+"\" style=\"margin:2px;\"></span>");
				$(ele).append(new_image);
				$(targetElement).parent().parent().parent().after(ele);
				}
			else
				{
				init_notification('error', data,true);
				}
		});
	}

	//删除测试人员
	function remove_member(targetElement,labelid) {
		var fortesting_id=$("#fortesting_id").val();
		$.get("/project/fortesting/"+fortesting_id+"/remove_tester/"+labelid,function(data,status){
			if(data=="True")
				{
				var dis_ele=$(targetElement).parent().parent().parent().parent().find("span[labelid="+labelid+"]");
				$(dis_ele).remove();
				}
			else
				{
				init_notification('error', data,true);
				}
		});
	}
	
	//下拉弹出菜单搜索
	function popmenu_search() {
		$("input[name=context_search_input]").keyup(function() {
			var inputKeyword = $(this).val().trim();
			var contextItems = $(this).parent().nextAll();
			for (var i = 0; i < contextItems.length; i++) {
				var email=$(contextItems[i]).find("span:eq(0)").attr("email");
				var currentItemText = $(contextItems[i]).text().trim();
				if (inputKeyword.trim() == "") {
					$(contextItems[i]).show();
				} else {
					if (email.toUpperCase().indexOf(inputKeyword.toUpperCase()) >= 0) {
						$(contextItems[i]).show();
					} else {
						$(contextItems[i]).hide();
					}

				}
			}
		});
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
	
    //初始化提测编辑页面
	function init_fortesting_edit_form()
	{
        try
        {
        	   init_editor("TestingFeature");
        	   init_editor("TestingAdvice");
        	   init_file_upload();
        	   init_datetime_input();
        	   init_DropDownList("ProjectModule",0);
        	  
        }
        catch(ex)
        {
        	   console.log(ex);
        }
	}
	
	
	function init_datetime_input()
	{
		$("#fortesting-edit-form #ExpectCommitDate").jqxDateTimeInput({ "width": 300, "height": 25,"formatString":"yyyy-MM-dd",readonly: true});
 	   $('#fortesting-edit-form #ExpectCommitDate').on('valueChanged', function (event) {
         
            var date =$("#fortesting-edit-form #ExpectCommitDate").jqxDateTimeInput("getText");
            $('#fortesting-edit-form #ExpectCommitDate_jqxDateTimeInput').attr("value",date);
        });
	}
	
	function init_editor(editor_id)
	{
		  $('#fortesting-edit-form #'+editor_id).jqxEditor({
        	  height: 200,
        	  width: 700,
        	  theme: theme,
        	  tools: 'bold italic underline | ul ol | html',
        	  lineBreak: 'div'
        	});
        
        $(".jqx-editor-content").css('height','159px');
	}
	
	function init_comboBox(name)
	{
		$("select[name="+name+"]").jqxComboBox({
			theme : theme,
			width : 300,
			height : 33,
			autoComplete : true,
			searchMode : 'containsignorecase'
		});
	}
	
	function init_file_upload()
	{
		 $("form[name=fortesting-edit-form]").dropzone({ 
         	
     	    url:'/project/fortesting/upload_attachment',         
         method:'post',
         paramName:'attachment',
         addRemoveLinks: true,
         maxFiles: 10,
         maxFilesize: 10,
         uploadMultiple: true,
         parallelUploads: 10,
//         acceptedFiles: ".pdf, .doc,.txt,.docx,.xlsx,.xls,.sql",
         success: function(file, response, e) {
     
             file.id=response;
             var attachments=$("#fortesting-edit-form #upload_files").val();
    
             $("#fortesting-edit-form #upload_files").attr("value",attachments+file.id+",");
         },
		 removedfile: function(file,e){
			 file.previewElement.remove();
			 var file_id=file.id;
			 $.get("/project/fortesting/0/delete_file/"+file_id,function(data,status){
				 var attachments=$("#fortesting-edit-form #upload_files").val();
	             $("#fortesting-edit-form #upload_files").attr("value",attachments.replace(file.id+",","")); 
			 });
		 }
     });
     
     $("form[name=fortesting-edit-form]").click(function(){
     	     $(this).parent().parent().css('height','200px');
     });
	}

	//提交提测编辑
	function submit_fortesting_form() {
		$("#save_fortesting").click(function() {
			if (validate_fortesting()) {
				var fortesting_id=$("#fortesting_id").val();
				$("#newfortesting-popup-dialog").modal('hide');
				$.post("/project/fortesting/"+fortesting_id+"/edit", $('#fortesting-edit-form').serialize(), function(data, status) {
					if (data == "True") {
						init_notification('success', "提测创建成功！");
					    var project_id=$("#ProjectID").val();
					    location.reload();
					} else {
						init_notification('error', data);
					}
				});
			}
			
		});
	}
	
	
	function load_fortesting_items(project_id)
	{
		$("#wait_for_commit").load('/project/fortesting/'+project_id+"/fortesting_items/1",function(){
			board_item_ajax_handler();
		});
		$("#commited").load('/project/fortesting/'+project_id+"/fortesting_items/2",function(){
			board_item_ajax_handler();
		});
		$("#intesting").load('/project/fortesting/'+project_id+"/fortesting_items/3",function(){
			board_item_ajax_handler();
		});
		$("#testfinished").load('/project/fortesting/'+project_id+"/fortesting_items/4",function(){
			board_item_ajax_handler();
		});
		$("#archived").load('/project/fortesting/'+project_id+"/fortesting_items/5",function(){
			board_item_ajax_handler();
		});
	}
	
	
	//board item ajax load
	
	function board_item_ajax_handler()
	{
		view_edit_fortesting();
		board_column_item_change_handler(item_status_changed);
		set_column_status();
	}
	

	//提测编辑页面字段验证
	function validate_fortesting() {
		var project = $("#ProjectID"), version = $("#fortesting-edit-form #VersionID"), newfeature = $("#fortesting-edit-form #TestingFeature"), advice = $("#fortesting-edit-form #TestingAdvice");
		var topic=$("#Topic");
		allFields = $([]).add(project).add(version).add(newfeature).add(advice).add(topic);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(project, "项目不能为空！");
		valid = valid && check_object_is_null(version, "版本不能为空！");
		valid = valid && check_object_is_null(topic, "提测主题不能为空！");
		valid = valid && check_editor_is_null(newfeature, "提测内容为必填项");
		valid = valid && check_editor_is_null(advice, "测试建议为必填项");
		return valid;
	}
	
	//编辑器字段空值检测
	function check_editor_is_null(editor,message)
	{
		var value=$(editor).jqxEditor('val');
		if(value.length<=1)
		{
			editor.parent().parent().addClass("has-error");
			init_notification("error", message, true);
			return false;	
		}
		else
			{
			  return true;
			}
	}
	
	/******************************************Board item status change handler******************************************/

	init_board();
	board_column_item_change_handler(item_status_changed);
	
	function item_status_changed(column_status,item_id,item)
	{
		console.log(1);
		var project_id=$("#project_id").attr("projectid");
		if(project_id==null)
			{
			  project_id=0;
			}
		if(column_status=="commited")
		  {
			   commited_handler(item_id,item,project_id);
		  }
		if(column_status=="wait_for_commit")
		  {
			update_fortesting_status(item_id,1,project_id,"");
			
		  }
		if(column_status=="intesting")
		  {
			intesting_handler(item_id,item,project_id);
		  }
		if(column_status=="testfinished")
		  {
			testingfinished_handler(item_id,item,project_id);
		  }
		if(column_status=="archived")
		  {
			archived_handler(item_id,item,project_id);
		  }
		
	}
	
	
	function intesting_handler(fortesting_id,item,project_id)
	{
		var item_notify_status=$(item).find("#"+fortesting_id).attr("notify_status");
		var notify_status_array=item_notify_status.split(",");
		var message="开始测试通知已经发出";
		var call_back_func=function(){
			$("#intesting").load('/project/fortesting/'+project_id+"/fortesting_items/3");
		   }
		if(notify_status_array[2]=="0")
		{
			$("#popup-dialog-container").load("/project/fortesting/get_confirm_dialog",function(){
				init_intesting_date_controll();
			$("#fortesting_starttesting_confirm").modal('show');
			$("#object_starttesting_confirm_button").click(function() {
				if($('#intesting_date_controll').jqxValidator('validate'))
				{
					$("#fortesting_starttesting_confirm").modal('hide');
					var start_date=$('#testing_start_date').val().trim();
					var end_date=$('#testing_end_date').val().trim();
					$.post("/project/fortesting/"+fortesting_id+"/update_testingdate",{"start_date":start_date,"end_date":end_date},function(data,status){
						if(data=="True")
			 			{
								update_fortesting_status(fortesting_id,3,project_id,message);
			 			}
			 			else
			 			{
			 				init_notification('error',data,true);
			 			}
					});
				}
			});	
			$("button[name=confirm_cancel_button]").click(function(){
				load_fortesting_items(project_id);
			});
			});
		}
		else
			{
			   update_fortesting_status(fortesting_id,3,project_id,message);
			}
		
		
			
	}
	
	
	function init_intesting_date_controll()
	{
 	   	
      	$('#intesting_date_controll').jqxValidator({
	     rules: [

	     {
	         input: '#testing_start_date',
	         message: '测试开始时间不能为空',
	         action: 'blur',
	         rule: function () {
	        	    var result = $('#testing_start_date').val().trim();
	        	    if(result==""){
	        	    	   return false;
	        	    }
	        	    return true;
	         }

	     },  {
	         input: '#testing_start_date',
	         message: '请输入正确的日期格式，例如 2017-12-12',
	         action: 'blur',
	         rule: function () {
	        	    var date = $('#testing_start_date').val().trim();
	        	    var result=date.match(/^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2})$/); 
	        	    if(result==null){
	        	    	   return false;
	        	    }
	        	    return true;
	        	}
	        	                        

	     }, 
	     {
	         input: '#testing_end_date',
	         message: '测试截止时间不能为空',
	         action: 'blur',
	         rule: function () {
	        	    var result = $('#testing_end_date').val().trim();
	        	    if(result==""){
	        	    	   return false;
	        	    }
	        	    return true;
	     }}, {
	         input: '#testing_end_date',
	         message: '请输入正确的日期格式，例如 2017-12-12',
	         action: 'blur',
	         rule: function () {
	        	    var date = $('#testing_end_date').val().trim();
	        	    var result=date.match(/^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2})$/); 
	        	    if(result==null){
	        	    	   return false;
	        	    }
	        	    return true;
	        	}
	        	                        

	     }
	     ]
	 });
	}
	function testingfinished_handler(fortesting_id,item,project_id)
	{
		var message="测试完成通知已经发出！";
		var item_notify_status=$(item).find("#"+fortesting_id).attr("notify_status");
		var notify_status_array=item_notify_status.split(",");
		var call_back_func=function(){
			$("#testfinished").load('/project/fortesting/'+project_id+"/fortesting_items/4");
		   }
		if(notify_status_array[3]=="0")
		{
			update_fortesting_status(fortesting_id,4,project_id,message);
		}
		else
			{
			   update_fortesting_status(fortesting_id,4,project_id,message);
			}
		
			
	}
	
	function archived_handler(fortesting_id,item,project_id)
	{
		var item_notify_status=$(item).find("#"+fortesting_id).attr("notify_status");
		var notify_status_array=item_notify_status.split(",");
		var message="发布完成通知已发出！";
		var call_back_func=function(){
			$("#archived").load('/project/fortesting/'+project_id+"/fortesting_items/5");   
		   }
		if(notify_status_array[4]=="0")
		{
			update_fortesting_status(fortesting_id,5,project_id,message);
		}
		else
		{
		    update_fortesting_status(fortesting_id,5,project_id,message);
		}

		
			
	}
	
	function commited_handler(fortesting_id,item,project_id)
	{

		var item_notify_status=$(item).find("#"+fortesting_id).attr("notify_status");
		var notify_status_array=item_notify_status.split(",");
		var message="提测通知已经发出，提测成功！";
		var call_back_func=function(){
			   $("#commited").load('/project/fortesting/'+project_id+"/fortesting_items/2");	  
		   }
		if(notify_status_array[1]=="0")
		{
			$("#popup-dialog-container").load("/project/fortesting/get_confirm_dialog",function(){
				init_intesting_date_controll();
				$("#fortesting_commit_confirm").modal('show');
				$("#object_commit_confirm_button").click(function() {
					$("#fortesting_commit_confirm").modal('hide');
					update_fortesting_status(fortesting_id,2,project_id,message);
				});	
				$("button[name=confirm_cancel_button]").click(function(){
//					location.reload();
					load_fortesting_items(project_id);
				});
			});
		}
		else
			{
			   update_fortesting_status(fortesting_id,2,project_id,message);
			}
		
	}

	
	function update_fortesting_status(fortesting_id,status,project_id,message)
	{
		$.post("/project/fortesting/"+fortesting_id+"/update_status/"+status,function(data,status){
	   	  	  if(data=="True")
	 			{
	   	  		    if(message!="")
	   	  		    	{
	   	  		       init_notification('success',message,true);
	   	  		    	}
	   	  		    load_fortesting_items(project_id);
	 			}
	 			else
	 			{
	 				init_notification('error',data,true);
	 			}
	   	  	
	   	  });	
	}
	
	
	function board_column_item_change_handler(handler)
    {
    	 $('.web-board-column-item-container').on('stop', function (e) {
    	     var trigger=e.currentTarget.id;
    	    	   $(".web-board-column-item-container").each(function(e){
    	    		   if($(this).attr('id')!=trigger)
    	    			   {
    	    			     var new_item_list=$(this).jqxSortable("toArray").sort();
    	    			     var old_item_list=column_status_map[($(this).attr('id'))];
    	    			     var result="0";
    	    			     if(old_item_list.length!=new_item_list.length)
    	    			    	 {
    	    			    	 var flag=false;
    	    			    	    for(i in new_item_list)
    	    			    	    	{
    	    			    	    	  for(j in old_item_list)
    	    			    	    		{

    	    			    	    		  if(new_item_list[i]==old_item_list[j])
    	    			    	    			{
    	    			    	    			   flag=true;
    	    			    	    			   break;
    	    			    	    			}
    	    			    	    		  else
    	    			    	    			  {
    	    			    	    			   flag=false;
    	    			    	    			  }
    	    			    	    		}
    	    			    	    	   if(!flag)
    	       			    	    	{
    	       			    	    	  result=new_item_list[i];
    	       			    	    	  break;
    	       			    	    	}
    	    			    	    	}
    	    			    	    var column_id=$(this).attr('id');
    	    			    	    console.log("result is :"+result);
    	    			    	    console.log("column is :"+column_id);
    	    			    	    handler(column_id,result,this);
    	    			    	 }
    	    			   }
    	    	   });
    	    	   set_column_status();
    	    	   $(".web-board-column-item-container").jqxSortable("cancel");
    	    });
    }

	var column_status_map={};
    set_column_status();
    
    function set_column_status()
    {
    	$('.web-board-column-item-container').each(function(){
    		var column_id=$(this).attr('id');
    		column_status_map[column_id]=$("#"+column_id).jqxSortable('toArray').sort();
    	});
    }
    
    function init_board()
	{
		 $(".web-board-column-item-container").jqxSortable({connectWith: ".web-board-column-item-container"});
		 var parent_height=$(".web-app-view-body-default").css("height");

		 $(".web-board-column-item-container").css("height",parent_height.replace("px","")-50+"px");
	}
	
	/************************通用函数**************************/
	
	
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
   
	
	function init_DropDownList(name,value)
	{
		$("select[name="+name+"]").jqxDropDownList({
			theme : theme,
			width : "100%",
			height : 33,
		});
		if(value!=0){
			var item = $("select[name="+name+"]").jqxDropDownList('getItemByValue',value);
			$("select[name="+name+"]").jqxDropDownList('selectItem', item);
		}	
	}
});
