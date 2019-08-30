$(document).ready(function() {
    var theme = 'bootstrap';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var latestClickEvent=null;
	var currentoPopObject = null;
	
	issue_item_click_handler();
	init_webapp(); 
	init_page();
	init_filter_panel(0);
	show_create_issue_dialog();
//	show_context_menu();
	init_detail_panel();
	hide_issue_detail_panel();
	open_save_query_dialog();
	select_filter_item();
	search_issue_item();
	refresh_issue_list();
	
	var issue_id=$("#project_issue_id").val();
	if (issue_id && issue_id!="all")
	{
		load_issue_detail(issue_id);	
	}
	
	window.addEventListener('click',function  () {
		latestClickEvent=event;
    })

	
/*******************************页面加载处理************************************/
	
	
	//初始化页面
	function init_page()
	{
		
	}
   
	
	
	//初始化webapp
	function init_webapp() {
        var parent_height = $(".web-app-view-body-default").css("height");
        $(".web-app-view-content-default").css("height", parent_height.replace("px", "") + "px");
        $(".webapp_header_leftbar_nav").hide();
        $(".issue-detail-body").css("max-height", parent_height.replace("px", "") - 220 + "px");
    }
	
	function show_create_issue_dialog()
	{
		 $("#tool_bar_new_issue").click(function(){
			$("#head_add_issue").trigger('click');
		 });
	}
	
	
	//问题列表右键菜单展现
	function show_context_menu()
	{
		// Create a jqxMenu
		var contextMenu = $("#issue_context_menu").jqxMenu({theme:'web', width: '170px',autoCloseOnClick: false, autoOpenPopup: false, mode: 'popup'});
		// open the context menu when the user presses the mouse right button.
	    $(".project_issue_listview_item").on('mousedown', function (event) {
	        var rightClick = isRightClick(event) || $.jqx.mobile.isTouchDevice();
	        if (rightClick) {
	            var scrollTop = $(window).scrollTop();
	            var scrollLeft = $(window).scrollLeft();
	            contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
	            hide_control_byclick_page($(contextMenu),$(this),null);
	            return false;
	        }
	    });
	    // disable the default browser's context menu.
	    $(".project_issue_listview_item").on('contextmenu', function (e) {
	        return false;
	    });
	
	}

	
	
	function refresh_issue_list()
	{
		$("#reload_issue_list").click(function(){
            var project_id=0;
            var user_role=0;
            try
            {
                project_id=$("select[name=Project]").jqxDropDownList("getSelectedItem").value;
            }
            catch(e)
            {
                console.log(e);
            }

            try
            {
                user_role=$($(".left_sub_meun_active")[0]).attr('user_role');
            }
            catch(e)
            {
                console.log(e);
            }
			load_issue_items(project_id,user_role);
		});
	}
	
	
	/********************************问题过滤控件处理****************************************/
	
	//初始化过滤面板
	function init_filter_panel(filter_id)
	{
		var project_id=$("#project_id").attr("projectid");
		if(project_id==null)
		{
		  project_id=0;
		}
		if(filter_id!=0)
		{
			project_id=0;
		}
		try
		{
		init_DropDownList("Team",0,false);
		init_DropDownList("Project",project_id,false);
		init_DropDownList("Version",0,true);
		init_DropDownList("Processor",0,true);
		init_DropDownList("Creator",0,true);
		project_change_handler();
		load_project_version("Version",project_id);
		load_project_member("Processor",project_id);
		load_project_member("Creator",project_id);
		issue_filter_dropdown_handler();
		issue_filter_checkbox_dropdown_handler();
		issue_filter_checkbox_handler();
		issue_filter_datetime_handler();
		clean_current_filter();
		var create_date=$("#input_issue_create_date").val();
		
		$("#issue_create_date").jqxDateTimeInput({
					theme:theme,
					width:"55%",
				    template:'primary',
				    height:33,
				    formatString:"yyyy-MM-dd",
				    	selectionMode: 'range',
				    	value:null,
				    	readonly: true,
				    	showFooter:true,
				    clearString:'Clear'
				 });
		if(create_date!=0)
		{
		var create_date_array=create_date.split("-");
		var date1 = new Date();
		date1.setFullYear(create_date_array[0],create_date_array[1]-1,create_date_array[2]);
		var date2 = new Date();
		date2.setFullYear(create_date_array[3],create_date_array[4]-1,create_date_array[5]);
		$("#issue_create_date").jqxDateTimeInput('setRange',date1,date2);
		}
		}
		catch(e)
		{
			console.log(e);
		}
	}
   
	 window.onload=function(e){
			   $.post("/project/issue/filter/clean",function(data,status){
				 
			   });
     }
	
	
	//弹出保存筛选对话框
	function open_save_query_dialog()
	{
		$("#issue_filter_save_button").click(function(){
			var query_id=$("#current_issue_query").val();
			var project_id=$("select[name=Project]").jqxDropDownList('getSelectedItem').value;
			$("#popup-dialog-container").load("/project/"+project_id+"/issue_filter/"+query_id+"/save_dialog", function() {
				$("#issue-query-save-dialog").modal('show');
				save_issue_filter();
				$("#issue_filter_save_as").click(function(){
					if($(this).attr("checked"))
					{
						$(this).removeAttr("checked");
					}
					else
					{
						$(this).attr("checked","true");	
					}
				});
			});
		});
		
	}
	
	//保存问题过滤器
    function save_issue_filter()
    {
    	   $("#issue_query_create_button").click(function(){
    		   if(validate_issue_query())
    			 {
    			   var filter_name=$("#IssueQueryTitle").val();
    			   var filter_id=$("#query_id").val();
    			   var save_as=$("#issue_filter_save_as").attr("checked");
    			   if(save_as)
    				   {
    				   filter_id=0;
    				   }
    			   var project_id=$("select[name=Project]").jqxDropDownList("getSelectedItem").value;
    			   $.post("/project/"+project_id+"/issue_filter/"+filter_id+"/create",{"filter_name":filter_name},function(data,status){ 
    				   if(data!="0")
    	    		        	{
    	    		          	load_issue_filter();
    	    		          	set_selected_filter(data,filter_name);
    	    		          	$("#issue-query-save-dialog").modal('hide');
    	    		        	}
    				   else{
    					   init_notification('error',"保存筛选器失败",false);	  
    				   }
    	    	       })
    			 }
    	   });
    	   
    }
    
    
    //加载问题过滤器列表
    function load_issue_filter()
    {
    	   $("#issue_filter_menu").load("/project/issue_filter/get_list",function(data,status){
    		   select_filter_item();
    	   });
    }
    //选择问题过滤器
    function select_filter_item()
    {
    	   $(".issue_filter_item").click(function(){
    		   var filter_id=$(this).attr('label');
    		   var filter_name=$($(this).find("a")[0]).text();
    		   set_selected_filter(filter_id,filter_name);
    		   update_filter_cache(filter_id);
    		   load_filter_panel(filter_id);
    	   });
    	
    }
    
    //根据选择的筛选器加载筛选器面板
    function load_filter_panel(filter_id)
    {
    	  $(".issue-filter-panel-body").load("/project/issue/filter/"+filter_id+"/filter_panel",function(){
    		  init_filter_panel(filter_id);
    	  });
    }
 
    //选择筛选器后，更新服务端筛选值
    function update_filter_cache(filter_id)
    {
       var project_id=$("select[name=Project]").jqxDropDownList("getSelectedItem").value;
    	   $.post("/project/"+project_id+"/issue/filter/"+filter_id+"/cache",{"values":""},function(data,status){
			if(data=="True")
			{
				load_issue_items(project_id,0);
			}
		});
    }
   
    //更新当前问题过滤器
    function set_selected_filter(filter_id,filter_name)
    {
    	   $($("#current_issue_query_menu").find("span")[0]).text(filter_name);
    	   $("#current_issue_query").val(filter_id);
    }
    
    function validate_issue_query() {
		var query_name = $("#IssueQueryTitle"),ci_task_project=$("#ci_task_project");
		allFields = $([]).add(query_name);
		var valid = true;
		allFields.parent().parent().removeClass("has-error");
		valid = valid && check_object_is_null(query_name, "筛选器名称不能为空！");
		valid = valid && check_object_length(query_name,10,"筛选器名称不能超过10个字符");
		return valid;
	}

   function clean_current_filter()
   {
	   $("#issue_filter_clear_button").click(function(){
		   $.post("/project/issue/filter/clean",function(data,status){
			   window.location.reload();
		   });
	   });
   }
    
   
// 单选下拉框，选择过滤
	
	function issue_filter_dropdown_handler()
	{
	$(".dropdown_filter").on('change',function (event){

	    var args = event.args;
	    if (args) 
	    {
	    	var item = args.item;
	      var value = item.value;
	      values=$(this).attr('id')+":"+value;
	      cache_issue_filter(values);
	     }
	});
	}
	
	//带checkbox的下拉框，选择过滤
	
	function issue_filter_checkbox_dropdown_handler()
	{
		
	$(".dropdown_filter").on('checkChange', function (event)
			{
			    if (event.args) {
			    var checkedItems = $(this).jqxDropDownList('getCheckedItems');
			    var checkedValues="";
			    $(checkedItems).each(function(index,checkedItem){
			    	   checkedValues=checkedValues+checkedItem.value+","
			    	   
			    });
			    values=$(this).attr('id')+":"+checkedValues;
			    cache_issue_filter(values);
			}
			});
	
	}
	
	//多选框，选择过滤
	
	function issue_filter_checkbox_handler()
	{
	
	$(".checkbox_filter").click(function(event){
		var checked_values="";
		var field_name=$(this).parent().attr("field_name");
		if($(this).attr("checked"))
		{
			$(this).removeAttr("checked");
		}
		else
		{
			$(this).attr("checked","true");	
		}
		$(this).parent().parent().parent().find(".checkbox_filter:checked").each(function(index,item){
			checked_values=checked_values+$(item).attr("value")+",";
		});
		values=field_name+":"+checked_values
		cache_issue_filter(values);
	});
	}
	
	//时间范围过滤
	function issue_filter_datetime_handler()
	{
	$('#issue_create_date').on('valueChanged', function (event) 
	{  
	    var jsDate = event.args.date; 
	    var type = event.args.type; // keyboard, mouse or null depending on how the date was selected.
	    var date_values=$(this).jqxDateTimeInput('getText');
		var field_name=$(this).attr("field_name");
		cache_issue_filter(field_name+":"+date_values);
	}); 
	
	}
	
	//上传过滤参数，并重新加载问题列表
	function cache_issue_filter(filter_values)
	{
		var project_id=$("select[name=Project]").jqxDropDownList("getSelectedItem").value;
		$.post("/project/"+project_id+"/issue/filter/0/cache",{"values":filter_values},function(data,status){
			if(data=="True")
			{
				load_issue_items(project_id,0);
			}
		});
	}
	
	//清除项目相关过滤条件
	function clean_filter_depend_project()
	{
		var version_filter="Version_s:";
		var processor_filter="Processor_s:";
		var creator_filter="Creator_s:";
		cache_issue_filter(version_filter);
		cache_issue_filter(processor_filter);
		cache_issue_filter(creator_filter);
		
	}
	

	
	/*******************************************问题列表*********************************************/
	

	//展现右侧面板
	
	function show_right_panel()
	{
			var issue_detail_panel=$(".web-app-view-right-panel-default");
			$(".web-app-view-right-panel-default").show(500);
			$('.issue-filter').hide(500);	
	}
	
	
	function search_issue_item()
	{
		$("#issue_search_box").keydown(function(event){
			 if (event.keyCode == 13)
			 {
				 var project_id=0;
                 var user_role=0;
				 try
				 {
					 project_id=$("select[name=Project]").jqxDropDownList("getSelectedItem").value;
				 }
				 catch(e)
				 {
					 console.log(e);
				 }

                 try
                 {
                     user_role=$($(".left_sub_meun_active")[0]).attr('user_role');
                 }
                 catch(e)
                 {
                     console.log(e);
                 }
				 
				 var search_word=$(this).val().trim();
					$.post("/project/"+project_id+"/issue/search/cache",{"search_word":search_word},function(data,status){
						if(data=="True")
						{
							load_issue_items(project_id,user_role);
						}
					});
			
	         }
		});
	}
	
	function issue_item_click_handler()
	{
		$(".project_issue_listview_item").click(function(){
			var issue_id=$(this).attr("issue_id");
			$(".project_issue_listview_item").removeClass("project_issue_selected_item");
			$(this).addClass("project_issue_selected_item");
			load_issue_detail(issue_id);
		});
	}
	
	function load_issue_detail(issue_id)
	{
		$("#webapp_right_panel").load("/project/issue/"+issue_id+"/detail",function(){
			init_detail_panel();
			show_right_panel();
		});
	}
	
	//隐藏右侧面板
	function hide_issue_detail_panel()
	{
		$(document).on('click', function(e)
		{
		   var hide_object=$(".web-app-view-right-panel-default");

			if (!parentHasClass(e.target,"project_issue_listview_item") && !parentHasClass(e.target,"web-app-view-right-panel-default") && !parentHasClass(e.target,'modal'))
			{
				if(!parentHasClass(e.target,'jqx-listbox'))
				{
                    hide_object.hide(500);
                    $('.issue-filter').show(500);
				}
			}
		});
	}
	
	//通过点击面板隐藏按钮，关闭面板
	function hide_issue_detail_panel_by_close_button()
	{
		$("#close-detail-panel").click(function(){
			$(".web-app-view-right-panel-default").hide(500);
			$('.issue-filter').show(500);
		});
	}
	
	
	//初始化详情面板
	function init_detail_panel()
	{
		try
		{
		$('#issue-desc-content-view').jqxEditor({theme:theme,tools: 'bold italic underline | outdent indent | ul ol  | left center right' });
	     $(".jqx-editor-toolbar-container").css("width","300px");	
	      show_detail_topic_dropdown_menu();
	 	  show_detail_field_dropdown_menu();
	 	  init_desc_editor();
	 	  select_menu_item();
	 	  edit_issue_title();
	 	  add_issue_comment();
	 	  open_issue_attachments_upload_dialog();
	 	  open_issue_operation_dialog();
	 	  delete_issue_attachment();
	 	 view_issue_attachment();
	 	 popmenu_search('member-search');
	 	hide_issue_detail_panel_by_close_button();
            var parent_height = $(".web-app-view-body-default").css("height");
            $(".issue-detail-body").css("max-height", parent_height.replace("px", "") - 200 + "px");
	 	$('[data-toggle="tooltip"]').tooltip();
		}
		catch(e)
		{
		   console.log(e);
		}
	}
	
	
//	var href=window.location.href;
//	var zz=/\/project\/\d{1,9}\/issue\/\w{3,9}/;
//	if(zz.test(href))
//	{
//		var issue_id=href.match(zz);
//		show_right_panel();
//		load_issue_detail(3);
//	}
	//删除问题附件
	function delete_issue_attachment()
	{
		$("span[name=detail_attachment_delete]").click(function(){
			var file_id=$(this).parent().parent().parent().find("span[name=attachment_info]").attr("file_id");
			$($(this).parent().parent().parent()).hide();
			$.post("/project/issue/delete_file/"+file_id,function(data,status){
				if(data=="True")
				{
					init_notification("success","附件已经成功删除",true);
				}
				else
				{
					init_notification("error",data,false);
				}
			})
		});
	}
	
	//浏览附件
	function view_issue_attachment()
	{
		$("span[name=attachment_info]").click(function(){
			var file_id=$(this).attr("file_id");
			var issue_id=$(".project_issue_selected_item").attr("issue_id");
			$("#popup-dialog-container").load("/project/issue/"+issue_id+"/attachment/"+file_id+"/view", function() {
				$("#issue-attachment-viewer").modal('show');
				$("#isue-attachment-viewer-dialog").css("width",window.screen.width*0.9+"px");
				issue_viewer_close_handler();
			});
		});
	}
	
	//问题处理窗口关闭处理
	function issue_viewer_close_handler()
	{
		$("#issue-attachment-viewer").on('hidden.bs.modal', function (e){
			var issue_id=$("#issue-attachment-viewer #issue_id").val();
				$(".project_issue_selected_item").each(function(index,item){
					if($(item).attr("issue_id")==issue_id)
					{
						$(item).trigger('click');
					}
				});
			
		});
	}
	
	
	//打开解决问题，关闭问题，reopen问题窗口
	
	function open_issue_operation_dialog()
	{
		$(".issue-detail-operation").click(function(){
			var operation_type=$(this).attr("operation_type");
			var issue_id=$(".project_issue_selected_item").attr("issue_id");
			if(issue_id==null)
			{
				issue_id=$("#project_issue_id").val();
			}
			$("#popup-dialog-container").load("/project/issue/"+issue_id+"/open_issue_operation_dialog/"+operation_type, function() {
				$("#issue-operation-dialog").modal('show');
				issue_operation_dialog_close_handler();
				try
				{
					init_DropDownList("Solution",0,false);
				}
				catch(e)
				{
					console.log(e);
				}
				save_operation_result(operation_type);
			});
		});
	}
	
	//问题处理窗口关闭处理
	function issue_operation_dialog_close_handler()
	{
		$("#issue-operation-dialog").on('hidden.bs.modal', function (e){
			var issue_id=$("#issue-operation-dialog #issue_id").val();
				$(".project_issue_selected_item").each(function(index,item){
					if($(item).attr("issue_id")==issue_id)
					{
						$(item).trigger('click');
					}
				});
			
		});
	}
	
	//关闭，重新打开，解决问题
	function save_operation_result(operation_type)
	{
		$("#issue_operation_ok_button").click(function(){
			var comment=$("#issue_operation_comment").val();
			var issue_id=$("#issue-operation-dialog #issue_id").val();
			var solution="";
			try
			{
				solution=$("select[name=Solution]").jqxDropDownList("getSelectedItem").value;	
			} 
			catch(e)
			{
				solution="";
				console.log(e);
			}
			$.post("/project/issue/"+issue_id+"/save_issue_operation_result/"+operation_type,
				{"solution":solution,'comments':comment},
				function(){
					$("#issue-operation-dialog").modal('hide');
				
			});
		});
		
	}
	
	
	
	/***************************** 附件上传相关*****************************/
	//点击上传，弹出上传附件窗口
	function open_issue_attachments_upload_dialog()
	{
		$("#issue-detail-upload-file-button").click(function(){
			var issue_id=$(".project_issue_selected_item").attr("issue_id");
			if(issue_id==null)
			{
				issue_id=$("#project_issue_id").val();
			}
			$("#popup-dialog-container").load("/project/issue/"+issue_id+"/open_upload_file_dialog", function() {
				$("#issue-upload-attachments-dialog").modal('show');

				upload_file_dialog_close_handler("issue_file_upload_form",issue_id);
				switch_2_upload_local_view();
				switch_2_upload_mobile_view();
				init_issue_file_upload("issue_file_upload_form");
			});
		});
	}
	
	//文件上传窗口关闭处理
	
	function upload_file_dialog_close_handler(formName,issue_id)
	{
		$("#issue-upload-attachments-dialog").on('hidden.bs.modal', function (e){
			var attachments=$("#"+formName+" #upload_files").val();
			$.post("/project/issue/"+issue_id+"/cached_attachment/save",{"cache_key":attachments},function(){
				$(".project_issue_selected_item").each(function(index,item){
					if($(item).attr("issue_id")==issue_id)
					{
						$(item).trigger('click');
					}
				});
			});
			
		});
	}
	
    function switch_2_upload_local_view()
    {
    	$("#upload-dialog-local-button").click(function(){
       	    $("#add-member-view").show();
       	    $("#import-member-view").hide();
       	    $(this).parent().parent().addClass("fortesting_view_edit_active");
       	    $("#upload-dialog-mobile-button").parent().parent().removeClass("fortesting_view_edit_active");
        });
    }
    
    function switch_2_upload_mobile_view()
    {
    	$("#upload-dialog-mobile-button").click(function(){
    	    $("#add-member-view").hide();
    	    $("#import-member-view").show();
    	   $(this).parent().parent().addClass("fortesting_view_edit_active");
    	  $("#upload-dialog-local-button").parent().parent().removeClass("fortesting_view_edit_active");
    	    
     });
    }
    
    //初始化文件上传控件
	function init_issue_file_upload(formName)
	{
		 $("form[name="+formName+"]").dropzone({ 
         	
     	    url:'/project/issue/cached_attachment',         
         method:'post',
         paramName:'attachment',
         addRemoveLinks: true,
         maxFiles: 10,
         maxFilesize: 10,
         width:"100%",
         height:"100%",
         uploadMultiple: true,
         parallelUploads: 10,
//         acceptedFiles: ".pdf, .doc,.txt,.docx,.xlsx,.xls,.sql",
         success: function(file, response, e) {
             results=response.split(",");
             if(results[1]=="null")
            	 {
            	     file.id=results[0];
            	     var attachments=$("#"+formName+" #upload_files").val();
                 $("#"+formName+"  #upload_files").attr("value",attachments+results[0]+",");
            	 }
             else
            	 {
            	   init_notification("error",results[1],false);
            	 }
         },
		 removedfile: function(file,e){
			 
			 $.post("/project/issue/cached_attachment/remove",{"cache_key":file.id},function(data,status){
				 if(data=="True")
					{
					   file.previewElement.remove();
					}
					else
					{
						init_notification('error',data,false);				
					}
			 });
		 }
     });

	}
	
	
	/***************************** 问题字段更新初始化*****************************/
	
	//回车或者点击发布，添加动态信息
	function add_issue_comment()
	{
	   $("#issue_comment_add_button").click(function(){
		   var comments=$("#issue_comment_input").val();
		   add_issue_comments(comments);
	   });
	   $("#issue_comment_input").keydown(function(e){
           if ((e.keyCode || e.which) == 13) {
        	   var comments=$(this).val();
        	   add_issue_comments(comments);
           } 
	   });
	}
	
	
	//初始化问题描述控件
	function init_desc_editor()
	{
	
     $('#issue-desc-content-view').focus(function(){
    	    $("#issue-desc-save-view").show();
     });
   
	$("#issue-desc-save-button").click(function(){
		$("#issue-desc-content-view").show(100);
		$("#issue-desc-save-view").hide(100);
		var desc=$("#issue-desc-content-view").jqxEditor('val');
		var field=$("#issue-desc-content-view").attr("field_name");
		update_issue_field(field,desc,desc);
		
	});
	
	$("#issue-desc-cancel-button").click(function(){
		$("#issue-desc-content-view").show(100);
		$("#issue-desc-save-view").hide(100);
	});
	
	}
	

	
	
	//问题详情也展示固定字段下拉菜单
	function show_detail_topic_dropdown_menu()
	{
		$(".issue-detail-topic-content").click(function(){
			   $(this).find(".dorpdown_option_menu").show();
			   hide_control_byclick_page($(".dorpdown_option_menu"),$(this));
		});
	 
	}
	
	//选择菜单选项
	function select_menu_item()
	{
		$(".option-item").click(function(){
			var item_id=$(this).attr('labelid');
			var field_name=$(this).parent().parent().parent().parent().attr("field_name");
			var menu_role=$(this).parent().attr("role");
			var old_text=$(this).parent().parent().parent().parent().find("span[name=field-text]").text().trim();
			var new_text=$(this).find("span[name=item-text]").text().trim();
			$(this).parent().children().each(function(index,element){
				$(element).find('span:eq(2)').find('i').removeClass('fa-check');
			});
			$(this).find('span:eq(2)').find('i').addClass('fa-check');
			
			if(field_name=="OSVersion")
			{
				var os_id=$(this).parent().parent().parent().parent().attr("os_id");
				item_id=item_id+","+os_id
			}
			update_issue_field(field_name,item_id,new_text);
			update_text_byselect_menu_item(this,menu_role,item_id,field_name);
		});
	}
	
	//选择菜单项后，更新显示值
	function update_text_byselect_menu_item(selected_item,menu_role,item_id,field_name)
	{
		var item_icon=$(selected_item).find("span[name=item-icon]").find("i:eq(0)");
		var item_text=$(selected_item).find("span[name=item-text]").text().trim();
		$(selected_item).parent().parent().parent().parent().find("span[name=field-text]").text(item_text);
		$(selected_item).parent().parent().parent().parent().find("span[name=field-icon]").find("i:eq(0)").attr("class",$(item_icon).attr("class"));
		load_os_version_menu(field_name,item_id);
		if(field_name=="DeviceOS")
		{
			$("#issue_device_os_version").parent().attr("os_id",item_id);
		}
		
	}
	
	//加载device os version
	function load_os_version_menu(field_name,item_id)
	{
	  if(field_name=="DeviceOS")
	    {
		   $("#issue_device_os_version").load("/project/os/"+item_id+"/os_version_menu",function(){
			   select_menu_item();
		   });
		}
		
	}
	
	//编辑问题title
	function edit_issue_title()
	{
	  $(".issue-detail-title").blur(function(){
		  var title=$(this).text();
		  var field=$(this).attr("field_name");
		  update_issue_field(field,title,title);
	  });
	}

	
	
    //更新下拉字段值
	function update_issue_field(field,value,new_text)
	{
		if(field!="DeviceOS")
		{
		var issue_id=$(".project_issue_selected_item").attr("issue_id");
		$.post("/project/issue/"+issue_id+"/update",{'field':field,'value':value,'new_text':new_text},function(data,status){
			if(data=="True")
			{
				init_notification('success',"属性更新成功！",true);
			}
			else
			{
				init_notification('error',data,false);				
			}
		});
		}
	}
	
	
	//添加comments
	function add_issue_comments(comments)
	{

		var issue_id=$(".project_issue_selected_item").attr("issue_id");
		$.post("/project/issue/"+issue_id+"/comments/add",{'comments':comments},function(data,status){
			if(data=="True")
			{
				init_notification('success',"属性更新成功！",true);
			}
			else
			{
				init_notification('error',data,false);				
			}
		});
	}

	
	//显示参数组类型选择下拉框
	function show_detail_field_dropdown_menu()
	{
		$(".issue-detail-field-dropdown-menu").click(function(){
			   $(this).find(".dorpdown_option_menu").show();
			   hide_control_byclick_page($(".dorpdown_option_menu"),$(this));
		});
	 
	}

 
   
	
    /****公共方法***********************************************************************/
	
	function load_issue_items(project_id,user_role)
	{
		if(project_id==null)
		{
		  project_id=0;
		}
		$("#issue_item_container").load("/project/"+project_id+"/issue/list",{'user_role':user_role},function(){
                reinit_issue_list();
		});

	}


	//issue list初始化
	function reinit_issue_list()
	{
        init_webapp();
        issue_item_click_handler();
//			show_context_menu();
        init_detail_panel();
        hide_issue_detail_panel();
        init_issue_filter_height();
        $('[data-toggle="tooltip"]').tooltip();
        search_issue_item();
        refresh_issue_list();
        scroll_bottom_load_issue();
	}

	
	scroll_bottom_load_issue();
	function scroll_bottom_load_issue()
	{
		$(".issue-item-panel-body").scroll(function(){
		    var issueContainerHeight = $(this).height();
		    var containerScrollHeight = $(this)[0].scrollHeight;
		    var containerScrollTop = $(this)[0].scrollTop; 
		    if(containerScrollTop + issueContainerHeight >=containerScrollHeight-40)
		    {
		      var issue_items=$(".project_issue_listview_item")
		    	  if(containerScrollHeight<=840 ||issue_items.length>=10)
		    	{
				load_more_issue(issue_items.length);	  
		    	}
		    }
		  });
	}
	
	function load_more_issue(page_size)
	{
		var project_id=null;
		var user_role=0;
		try
		{
			user_role=$(".left_sub_meun_active").first().attr("user_role");
			project_id=$("select[name=Project]").jqxDropDownList("getSelectedItem").value;
		}
		catch(e)
		{
			console.log(e);
		}
		
		if(project_id==null)
		{
		  project_id=0;
		}
		$.post("/project/"+project_id+"/issue/list_more/"+page_size,{'user_role':user_role},function(data,status){
			if(data!="")
			{
				$("#issue_item_list").append(data);	
			}
			else
			{
				init_notification("warning","符合条件的问题已经加载完毕！",true);
			}
			
			init_webapp();
			issue_item_click_handler();
//			show_context_menu();
			init_detail_panel();
			hide_issue_detail_panel();
			init_issue_filter_height();
			$('[data-toggle="tooltip"]').tooltip();
		});
		
	}

    function popmenu_search(menu_name) {
        $("input[name="+menu_name+"]").keyup(function() {
            var inputKeyword = $(this).val().trim();
            var contextItems = $(this).parent().nextAll();
            for (var i = 0; i < contextItems.length; i++) {
                var currentItemText = $(contextItems[i]).text().trim();
                if (inputKeyword.trim() == "") {
                    $(contextItems[i]).show();
                } else {
                    if (currentItemText.toUpperCase().indexOf(inputKeyword.toUpperCase()) >= 0) {
                        $(contextItems[i]).show();
                    } else {
                        $(contextItems[i]).hide();
                    }

                }
            }
        });
    }
	
	
	function init_issue_filter_height()
    {
     	var container_height=$(".web-app-view-body-default").css("height");
     	if(container_height)
     		{
     		  var height1=container_height.replace("px","");
     		$(".issue-filter-panel-body").css("max-height",(height1-70)+"px"); 
     		$(".issue-item-panel-body").css("max-height",(height1-70)+"px"); 
     		$(".issue-item-panel-body").css("height",(height1-70)+"px"); 
     		
     		}
    }

	
	
	
	
    function project_change_handler()
	{ 
		$("#Project").on('change', function (event){
		    var args = event.args;
		    if (args) {
		    	var item = args.item;
		    var value = item.value;
			 load_project_version("Version",value);
			 load_project_member("Processor",value);
			 load_project_member("Creator",value);
			 clean_filter_depend_project();
//			 $(".checkbox_filter").removeAttr("checked");
			
		}
		});
	}
  //根据project 变更version可选值
	function load_project_version(version_controll,project_id)
	{
		if(project_id!=0)
		{
		$("select[name="+version_controll+"]").load("/project/fortesting/"+project_id+"/project_version_list",{"default_none":"0"},function(data,status){
				$("select[name="+version_controll+"]").jqxDropDownList('loadFromSelect', version_controll+'_s_jqxDropDownList');
				$("select[name="+version_controll+"]").jqxDropDownList({
					theme : theme,
					width : "100%",
					height : 33,
					selectedIndex:1
				});
				
		});
		}
	}
	
	function load_project_member(controll,project_id)
	{
		if(project_id!=0)
		{
		$("select[name="+controll+"]").load("/project/"+project_id+"/member/project_member_dropdownlist",function(data,status){
				$("select[name="+controll+"]").jqxDropDownList('loadFromSelect', controll+'_s_jqxDropDownList');
				$("select[name="+controll+"]").jqxDropDownList({
					theme : theme,
					width : "100%",
					height : 33,
					selectedIndex:0
				});
		});
		}
	}
	
	
    //带复选框的下拉框选择item
	function check_dropdown_item(controll_name,seleceted_values)
	{
		var checked_values=seleceted_values.split(",");
	       for(i=0;i<checked_values.length;i++)
	    	   {
	    	     if(checked_values[i]!="")
	    	    	 {
	    	    	      console.log(3);
	    	    	      console.log(controll_name);
	    	    	      console.log(checked_values[i]);
	    	    	       var item = $("select[name="+controll_name+"]").jqxDropDownList('getItemByValue',checked_values[i]);
	      		   console.log(item.label);
	    	    	       $("select[name="+controll_name+"]").jqxDropDownList('checkItem',item);
	    	    	 }     
	    	   }
	}
	
	//获取选中item信息并更新
	function set_ajax_field_status(controll,filter_id)
	{
		$.get("/project/issue/filter/"+filter_id+"/filter_ui_config",function(data,status){
		    if(data!="")
		    	{
		         var field_config_list=data.split(";")
		         for(i=0;i<field_config_list.length;i++)
		        	 {
	    	        	 if(field_config_list[i]!="")
	    	        		{
	    	        		    field_config=field_config_list[i];
	    	        			try
	    	        		    {
	    	        		       var field_name=field_config.split(":")[0];
	    	        	    	       var value=field_config.split(":")[1];
	    	        	    	       if(controll==field_name.replace("_s",""))
	    	        	    	    	   {
	    	        	    	    	   check_dropdown_item(controll,value);
	    	        	    	    	   }
	    	        		    }
	    	        		    catch(e)
	    	        		    {
	    	        		    	    console.log(e);
	    	        		    }
	    	        		}
		        	 }
		    	}
	});
	}
	
	
	//初始化下来列表
	function init_DropDownList(name,value,checkbox)
	{
		$("select[name="+name+"]").jqxDropDownList({
			theme : theme,
			width : "100%",
			height : 33,
			checkboxes:checkbox,
			filterable:true,
		});
		if(value!=0){
			var item = $("select[name="+name+"]").jqxDropDownList('getItemByValue',value);
			$("select[name="+name+"]").jqxDropDownList('selectItem', item);
		}	
	}
	//初始化组合框
	function init_comboBox(name,value)
	{
		$("select[name="+name+"]").jqxComboBox({
			theme : theme,
			width : "100%",
			height : 33,
			autoComplete : true,
			searchMode : 'containsignorecase'
		});
		if(value!=0){
			var item = $("select[name="+name+"]").jqxComboBox('getItemByValue',value);
			$("select[name="+name+"]").jqxComboBox('selectItem', item);
		}	
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
	
	//判断是否是子元素
	function isParent (obj,parentObj){ 
		while (obj != undefined && obj != null && obj.tagName.toUpperCase() != 'BODY'){ 
		if (obj == parentObj){ 
		return true; 
		} 
		obj = obj.parentNode; 
		} 
		return false; 
		}
	
	function parentHasClass (obj,className){ 
		while (obj != undefined && obj != null && obj.tagName.toUpperCase() != 'BODY'){
			console.log(obj.className);
		  if ($(obj).hasClass(className)){
		    return true;
		   }
		   obj = obj.parentNode;
		} 
		return false; 
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
	
	 function isRightClick(event) {
	        var rightclick;
	        if (!event) var event = window.event;
	        if (event.which) rightclick = (event.which == 3);
	        else if (event.button) rightclick = (event.button == 2);
	        return rightclick;
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
	 
	 function check_object_length(o,length,message)
	 {
		 if(o.val().length<=length)
			 {
			   return true;
			 }
		 else
			 {
			    o.parent().parent().addClass("has-error");
				init_notification("error", message, true);
			   return false;
			 }
	 }

});
