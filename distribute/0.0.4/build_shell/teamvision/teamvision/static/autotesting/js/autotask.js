$(document).ready(function() {

	var currnetpageindex = 1;
	var searchkeyword="ALL";
	var autotaskid=0;
	var theme='arctic';

	loadList("getlist", "autotask",currnetpageindex,"ALL");
     
    loadautotasktoolbar();
    
    searchautotask();

 
	//加载对象列表容器
	function loadList(listmethod, objectType, pageindex, searchkeyword) {
		//加载列表
		$("#autotasklistcontainer").load("/autotesting/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			searchkeyword : searchkeyword
		}, function(data, status) {
			showrowmenu();
			row_menu_event_handle();
			clickrowstart();
			clickrowstop();
			// //加载测试进度
			// loadprogress();
			// //点击行编辑按钮弹出编辑窗口
			// clickrowedit();
			// //点击复选框
			// clickcheckbox();
// 
			// //双击行
			// doubleclickrow();
			// mouseroverdatarow();
			// // $("span[class=testjobidcontent]").each(function(){
				// // $(this).hide();
			// // });
			// $("span[class=testjobsubmitidcontent]").each(function(){
				// $(this).hide();
			// });                
		});

	}
	
	
	//show row operation menu
	function showrowmenu()
	{
		var contextMenu = $("#autotaskrowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=autotaskrowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=autotaskidcontent]");
                	    autotaskid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=autotaskrowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function row_menu_event_handle()
	{
		$("li[name=autotaskrowoperationedit]").click(function(){
			disable_autotask_toolbar();
			edit_autotask(autotaskid);
		});
		$("li[name=autotaskrowoperationdelete]").click(function(){
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" +autotaskid + "的自动化任务吗？");
			$("#dialog-confirmdelete").dialog("open");
		});
		$("li[name=autotaskrowoperationdetail]").click(function(){
		});
		$("li[name=autotaskrowoperationreport]").click(function(){
			
		});
		$("li[name=autotaskrowoperationcopy]").click(function(){
			$.post("/autotesting/autotask/copyautotask",{autotaskid:autotaskid},function(data,status){
				loadList("getlist", "autotask",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
		});
	}


	//点击checkbox

	function clickcheckbox() {
		$("[name = selectautotask]:checkbox").bind("click", function() {
			var $chk = $("[name = selectautotask]:checkbox");
			// $("#autotaskselectall").attr("checked", $chk.length == $chk.filter(":checked").length);
		});
		// $("#autotaskselectall").bind("click", function() {
			// var $chk = $("[name = selectautotask]:checkbox");
			// if ($chk.filter(":checked").length == $chk.length) {
				// $("[name = selectautotask]:checkbox").attr("checked", false);
			// } else {
				// $("[name = selectautotask]:checkbox").attr("checked", true);
			// }
		// });
	}

	//双击测试计划行
	function doubleclickrow() {
		$("li[class=testjobdatarow]").dblclick(function() {
			jobid = $(this).find("span[class=testjobidcontent]").text().trim();
			openEditJobDialog(jobid);

		});
	}

	//点击 行编辑按钮
	function clickrowstart() {
		$("button[name=autotaskrowrun]").click(function() {
			var autotaskid = $(this).parent().parent().find("span[class=autotaskidcontent]").text().trim();
			$.post("/autotesting/autotask/starttask",{autotaskid:autotaskid},function(data,status)
			{
				loadList("getlist", "autotask",currnetpageindex,get_search_keyword());
				popupmessage(data);
			});
		});
	}
	
	//弹出提示信息
	function popupmessage(data)
	{
		$("#messageNotification").jqxNotification({
                width: 250, position: "bottom-right", opacity: 0.9,
                autoOpen: false, animationOpenDelay: 300, autoClose: false, template: "info"
        });
        $("#autotask_messagecontent").empty();
        $("#autotask_messagecontent").append(data);
        $("#messageNotification").jqxNotification("open");
	}
	
	
	//点击 行编辑按钮
	function clickrowstop() {
		$("button[name=autotaskrowstop]").click(function() {
			var autotaskid = $(this).parent().parent().find("span[class=autotaskidcontent]").text().trim();
			$.post("/autotesting/autotask/stoptask",{autotaskid:autotaskid},function(data,status)
			{
				loadList("getlist", "autotask",currnetpageindex,get_search_keyword());
				popupmessage(data);
			});
		});
	}


	

	//鼠标滑过数据行
	function mouseroverdatarow() {
		$("li[class=autotaskdatarow]").mouseover(function() {
			$(this).addClass("mouseroverdatarow");
		});
		$("li[class=autotaskdatarow]").mouseout(function() {
			$(this).removeClass("mouseroverdatarow");
		});
	}
	
	
	
	//加载自动化任务工具栏
	function loadautotasktoolbar() {
		$("#autotasktoolbar").jqxToolBar({theme:theme,
			tools : "button | custom",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					case 0:
						tool.jqxButton({width:80});
						tool.text("添加");
						tool.on("click",function(event){
							disable_autotask_toolbar();
							click_add_autotask();
						});
						break;
					case 1:
					    var searchbox=$("<div id='autotasksearchbox'><input id='autotasksearchinput'  type='text'/><div id='autotasksearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    tool.append(searchbox);
					    // var source ={
                            // datatype: "json",
                            // datafields:[{name:'autotaskname'}],
                            // url: '/autotesting/autotask/get_taskname_list'
                            // };
                        // var dataAdapter = new $.jqx.dataAdapter(source);
					    searchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						break;
				}
			}
		});
	}
	
	//auto task 创建
	
	
	
	function create_autotask(autotaskid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#autotask_nameInput', message: '任务名称 是必填项!', action: 'keyup, blur', rule: 'required' },
                       { input: '#autotask_nameInput', message: '任务名称已经存在!', action: 'keyup, blur', rule: validate_autotask_name },
                       { input: '#autotask_testcasecombo', message: '测试用例是必选项！', action: 'keyup, blur', rule: validate_autotask_testcase },
                       { input: '#autotask_project_combo', message: '项目是必选项 ', action: 'keyup, blur', rule: validate_autotask_project }
                       ];
                       
		    $("#autotask_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#autotask_create").css('visibility', 'visible');
            $('#autotasksendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#autotask_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#autotask_create_backbutton").on('click',function(){
            	$('#autotask_create_form').jqxValidator('hide');
            	loadautotaskpage();
            }); 
              init_autotask_name(autotaskid);
              init_autotask_project(autotaskid);
              // init_autotask_testconfig(autotaskid,0);
              init_autotask_testcase(autotaskid);
              // init_autotask_tasktype(autotaskid);
              init_autotask_agent(autotaskid);
              init_autotask_splittask(autotaskid);
              init_autotask_viewscope(autotaskid);
              
              change_project_handler(autotaskid);
            
            $("#autotask_advance_button").jqxButton({theme:theme, width: '80'});
            $("#autotask_advance_button").on('click',function(){
                 $("tr[class=autotask_advance]").toggle();
            });
            
            $('#autotasksendButton').on('click', function () {
                $('#autotask_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#autotask_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(autotaskid==0)
            	 {
            	 	send_createtask_request();
            	 }
            	 else
            	 {
            	 	send_edittask_request(autotaskid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_autotask_name(autotaskid)
	{
		$.post("/autotesting/autotask/init_autotask_formcontrol",{autotaskid:autotaskid,controlname:"TASKNAME"},function(data,status){
			 $("#autotask_nameInput").jqxInput({theme:theme,placeHolder:"请输入任务名称!", width: 350, height: 25});
            if(data!="")
          {
        	$("#autotask_nameInput").jqxInput("val",data);
          }       			
		});
	}
	
	function validate_autotask_name()
	{
		var autotaskname=$("#autotask_nameInput").jqxInput("val");
		var result=false;
		if(autotaskid!=0)
		{
			result=true;
		}
		else
		{
		  $.ajax({  
                async:false,
                type: "POST",  
                url: "/autotesting/autotask/check_name_exits",  
                data: "autotaskname="+autotaskname,  
                success: function(data,status)
                {  
                    if(data!="True")
                    {
                    	result=true;
                    }
                }  
            });	
		}
          return result;
	}
	
	
	
	//初始化测试配置控件
	
	function init_autotask_testconfig(autotaskid,projectid)
	{
		$.post("/autotesting/autotask/init_autotask_formcontrol",{autotaskid:autotaskid,controlname:"TESTCONFIG",projectid:projectid},function(data,status){
			var autotasktype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotask_testconfigcombo").jqxComboBox({theme:theme,selectedIndex:selectedIndex,source: autotasktype_source, width: 350, height: 25,displayMember:'text',valueMember:'memberid',searchMode: 'contains',autoComplete:true});
			for(var i in autotasktype_source)
			{
				if(autotasktype_source[i].selected==1)
				{
					var selectItem=$("#autotask_testconfigcombo").jqxComboBox('getItem',Number(i));
					$("#autotask_testconfigcombo").jqxComboBox('selectItem',selectItem);
					break;
				}
				
			}           
			});		
		// var countries =[{text:"All",value:0},{text:"A",value:1},{text:"B",value:2},{text:"C",value:3},{text:"D",value:4},];
	}
	
	
	
	//autotask_config validate function
	
	function validate_autotask_config()
	{
		var result=false;
		var item = $("#autotask_testconfigcombo").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
	}
	//初始化测试配置控件
	
	function init_autotask_testcase(autotaskid)
	{
		$.post("/autotesting/autotask/init_autotask_formcontrol",{autotaskid:0,controlname:"TESTCASE"},function(data,status){
			var autotasktype_source =eval("(" + data + ")");
			var selectedIndex=0;
			for(var i in autotasktype_source)
			{
				if(autotasktype_source[i].selected==1)
				{
					selectedIndex=i;
					break;
				}
				
			}
		});
		var countries =[{text:"All",value:0,isselected:false},{text:"A",value:1,isselected:false},{text:"B",value:2,isselected:false},{text:"C",value:3,isselected:true},{text:"D",value:4,isselected:true}];
        $("#autotask_testcasecombo").jqxComboBox({theme:theme,selectedIndex:0,source: countries, multiSelect: false, width: 350, height: 25,displayMember:'text',valueMember:'value',searchMode: 'contains',autoComplete:true});           
	}
	
	
	//autotask_testcase validate function
	
	function validate_autotask_testcase()
	{
		var result=false;
		var item = $("#autotask_testcasecombo").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
   
   //初始化测试任务类型控件
	
	function init_autotask_tasktype(autotaskid)
	{
		$.post("/autotesting/autotask/init_autotask_formcontrol",{autotaskid:autotaskid,controlname:"TASKTYPE"},function(data,status){
			var autotasktype_source =eval("(" + data + ")");
			var selectedIndex=0;
			for(var i in autotasktype_source)
			{
				if(autotasktype_source[i].selected==1)
				{
					selectedIndex=i;
					break;
				}
				
			}
        $("#autotask_tasktypecombo").jqxComboBox({theme:theme,selectedIndex:selectedIndex,source:autotasktype_source, multiSelect: false, width: 350, height: 25,displayMember:'text',valueMember:'memberid',searchMode: 'contains',autoComplete:true});
		});
	}
	
	
	//autotask_type validate function
	
	function validate_autotask_tasktype()
	{
		var result=false;
		var item = $("#autotask_tasktypecombo").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }

   
  // 初始化autotask_assgin_agent
  function init_autotask_agent(autotaskid)
	{
		$.post("/autotesting/autotask/init_autotask_formcontrol",{autotaskid:autotaskid,controlname:"TASKAGENT"},function(data,status){
			var autotasktype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotask_agent_combo").jqxComboBox({theme:theme,source:autotasktype_source, multiSelect:false, width: 350, height: 25,displayMember:'text',valueMember:'memberid',searchMode: 'contains',autoComplete:true});
			for(var i in autotasktype_source)
			{
				if(autotasktype_source[i].selected==1)
				{
					var selectItem=$("#autotask_agent_combo").jqxComboBox('getItem',Number(i));
					$("#autotask_agent_combo").jqxComboBox('selectItem',selectItem);
					break;
				}
				
			}
		});           
	}

 //初始化项目组合框
  function init_autotask_project(autotaskid)
	{
		$.post("/autotesting/autotask/init_autotask_formcontrol",{autotaskid:autotaskid,controlname:"TASKPROJECT"},function(data,status){
			var autotaskproject_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotask_project_combo").jqxComboBox({theme:theme,selectedIndex:selectedIndex,source: autotaskproject_source, multiSelect:false, width: 350, height: 25,displayMember:'text',valueMember:'memberid',searchMode: 'contains',autoComplete:true});
			for(var i in autotaskproject_source)
			{
				if(autotaskproject_source[i].selected==1)
				{
					var selectItem=$("#autotask_project_combo").jqxComboBox('getItem',Number(i));
					$("#autotask_project_combo").jqxComboBox('selectItem',selectItem);
					// selectedIndex=i;
					break;
				}
				
			}
			var projectid= $("#autotask_project_combo").jqxComboBox('getSelectedItem').value;
   	  	    init_autotask_testconfig(autotaskid,projectid);
		});           
	}
	
    //TASK TYPE change event
   function change_project_handler(autotaskid)
   {
   	  $("#autotask_project_combo").on("change",function(){
   	  	 var projectid= $("#autotask_project_combo").jqxComboBox('getSelectedItem').value;
   	  	 init_autotask_testconfig(autotaskid,projectid);
   	  });
   	  
   	  
   }
	
  //autotask_type validate function
	
	function validate_autotask_project()
	{
		var result=false;
		var item = $("#autotask_project_combo").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
	
   //初始化任务拆分选项
   
   function init_autotask_splittask(autotaskid)
	{
		$.post("/autotesting/autotask/init_autotask_formcontrol",{autotaskid:autotaskid,controlname:"TASKSPLIT"},function(data,status){
			var selectedIndex=0;
			if(data=="True")
			{
				selectedIndex=1;
			}
			var countries =[{text:"否",value:0},{text:"是",value:1}];
            $("#autotask_splittask_dropdownlist").jqxDropDownList({theme:theme,source: countries, width: 350, height: 25,selectedIndex:selectedIndex,displayMember:'text',valueMember:'value'});           
		});
	}
	
   //发送创建任务请求
   function send_createtask_request()
   {
   	  var autotask_field=$('#autotask_create_form').serialize();
   	  $.post("/autotesting/autotask/create",$('#autotask_create_form').serialize(),function(data,status){
          loadautotaskpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_edittask_request(autotaskid)
   {
   	  var autotask_field=$('#autotask_create_form').serialize();
   	  $.post("/autotesting/autotask/edit",$('#autotask_create_form').serialize()+"&autotaskid="+autotaskid,function(data,status){
          loadautotaskpage();
   	  });
   	  
   }
   

 
     
    //初始化任务拆分选项
   
   function init_autotask_viewscope(autotaskid)
	{
		$.post("/autotesting/autotask/init_autotask_formcontrol",{autotaskid:autotaskid,controlname:"TASKVIEWSCOPE"},function(data,status){
			var selectedIndex=0;
			if(data=="1")
			{
				selectedIndex=1;
			}
			var countries =[{text:"所有人可见",value:0},{text:"仅自己可见",value:1}];
            $("#autotask_viewscope_dropdownlist").jqxDropDownList({theme:theme,source: countries, width: 350, height: 25,selectedIndex:selectedIndex,displayMember:'text',valueMember:'value'}); 
			});          
	}
     
	//点击添加自动化任务按钮
	
	function click_add_autotask()
	{
		$("#middleContainer").load("/autotesting/autotask/create", function() {
			  create_autotask(0);
		});
	}
	
	//编辑自动化任务
	function edit_autotask(autotaskid)
	{
		$("#middleContainer").load("/autotesting/autotask/edit", function() {
			  create_autotask(autotaskid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_autotask_toolbar()
	{
		$("#autotasktoolbar").jqxToolBar("disableTool",0, true);
	    $("#autotasktoolbar").jqxToolBar("disableTool",1, true);
		$("#autotasktoolbar").jqxToolBar("disableTool",2, true);
		$("#autotasktoolbar").jqxToolBar("disableTool",3, true);
	}
	
    
	loadpagenation(get_search_keyword());
	function loadpagenation(searchkeyword) 
	{
		$.post("/autotesting/autotask/get_autotask_page_counts", {
			searchkeyword : searchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					searchkeyword = $('#autotasksearchinput').val();
					if (searchkeyword == "") 
					{
						 searchkeyword = "ALL";
					}
					loadList("getlist", "autotask", page,searchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadautotaskpage() {
		$("#middleContainer").load("/autotesting/autotask/index", function() {
			$.getScript("/static/autotesting/js/autotask.js");
			loadautotasktoolbar();
		});
	}
	
	//复制提测项目
	function copyautotask() {
		$("#header_copy").click(function() {
			var $chk = $("[name = selectautotask:checkbox");
			var checkedlength = $chk.filter(":checked").length;
			if (checkedlength > 1) {
				$("#dialog-confirm").empty();
				$("#dialog-confirm").append("抱歉，不支持批量复制！！");
				$("#dialog-confirm").dialog("open");
			} else if (checkedlength < 1) {
				$("#dialog-confirm").empty();
				$("#dialog-confirm").append("请选择一项要复制的数据！");
				$("#dialog-confirm").dialog("open");
			} else {
				autotaskid = $chk.filter(":checked").parent().find("span[class=autotaskidcontent]").text().trim();
				$.get("/autotesting/autotask/copy_autotask", {
					id : autotaskid
				}, function(data, status) {
					$("#dialog-confirm").empty();
					$("#dialog-confirm").append(data);
					$("#dialog-confirm").dialog("open");
					searchkeyword = $('#autotasksearchinput').val();
					if (searchkeyword == "") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "autotask", currnetpageindex, searchkeyword);
				});
			}
		});
	}
	
	//search submition
	function searchautotask() {
		//点击搜索按钮
		$("#autotasksearchbutton").click(function() 
		{
			search_autotask_bykeyword();
		});
		
		$('#autotasksearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_autotask_bykeyword();
				}
			});
	}
	
	//search submition
	function search_autotask_bykeyword()
	{
		    searchkeyword = $('#autotasksearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}

			loadpagenation(searchkeyword);
			loadList("getlist", "autotask", 1, searchkeyword);
	}
	
	//获取当前搜索关键字
	function get_search_keyword()
	{
		searchkeyword = $('#autotasksearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}
		return searchkeyword;
	}
	
	//删除任务确认
	
	function delete_autotask() {
		$("button[name=rowdelete]").click(function(data, status) {
			currentsubmitionid = $(this).parent().parent().find("span[class=testsubmitionidcontent]").text().trim();
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" + currentsubmitionid + "的提测项吗？");
			$("#dialog-confirmdelete").dialog("open");
		});
	}
	
	$("#dialog-confirmdelete").dialog({
			autoOpen : false,
			height : 200,
			width : 300,
			modal : true,
			buttons : {
				"是" : function() {
					$(this).dialog("close");
					$.post("/autotesting/autotask/deleteautotask",{autotaskid:autotaskid},function(data,status){
				loadList("getlist", "autotask",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
				},
				"否" : function() {
					$(this).dialog("close");
				}
			},
			close : function() {
			}
		});
	


});
