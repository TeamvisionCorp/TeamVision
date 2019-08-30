$(document).ready(function() {

	var currnetpageindex = 1;
	var searchkeyword="ALL";
	var autotestconfigid=0;
	var theme='arctic';

	loadList("getlist", "autotestconfig",currnetpageindex,"ALL");
     
    loadautotestconfigtoolbar();
    
    searchautotestconfig();

 
	//加载对象列表容器
	function loadList(listmethod, objectType, pageindex, searchkeyword) {
		//加载列表
		$("#autotestconfiglistcontainer").load("/autotesting/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			searchkeyword : searchkeyword
		}, function(data, status) {
			showrowmenu();
			row_menu_event_handle();
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
		var contextMenu = $("#autotestconfigrowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=autotestconfigrowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=autotestconfigidcontent]");
                	    autotestconfigid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=autotestconfigrowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function row_menu_event_handle()
	{
		$("li[name=autotestconfigrowoperationedit]").click(function(){
			disable_autotestconfig_toolbar();
			edit_autotestconfig(autotestconfigid);
		});
		$("li[name=autotestconfigrowoperationdelete]").click(function(){
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" +autotestconfigid + "的自动化任务吗？");
			$("#dialog-confirmdelete").dialog("open");
		});
		$("li[name=autotestconfigrowoperationdetail]").click(function(){
		});
		$("li[name=autotestconfigrowoperationreport]").click(function(){
			
		});
		$("li[name=autotestconfigrowoperationcopy]").click(function(){
			$.post("/autotesting/autotestconfig/copyautotestconfig",{autotestconfigid:autotestconfigid},function(data,status){
				loadList("getlist", "autotestconfig",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
		});
	}


	//点击checkbox

	function clickcheckbox() {
		$("[name = selectautotestconfig]:checkbox").bind("click", function() {
			var $chk = $("[name = selectautotestconfig]:checkbox");
			// $("#autotestconfigselectall").attr("checked", $chk.length == $chk.filter(":checked").length);
		});
		// $("#autotestconfigselectall").bind("click", function() {
			// var $chk = $("[name = selectautotestconfig]:checkbox");
			// if ($chk.filter(":checked").length == $chk.length) {
				// $("[name = selectautotestconfig]:checkbox").attr("checked", false);
			// } else {
				// $("[name = selectautotestconfig]:checkbox").attr("checked", true);
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
	function clickrowedit() {
		$("button[name=rowedit]").click(function() {
			jobid = $(this).parent().parent().find("span[class=testjobidcontent]").text().trim();
			openEditJobDialog(jobid);
		});
	}


	

	//鼠标滑过数据行
	function mouseroverdatarow() {
		$("li[class=autotestconfigdatarow]").mouseover(function() {
			$(this).addClass("mouseroverdatarow");
		});
		$("li[class=autotestconfigdatarow]").mouseout(function() {
			$(this).removeClass("mouseroverdatarow");
		});
	}
	
	
	
	//加载自动化任务工具栏
	function loadautotestconfigtoolbar() {
		$("#autotestconfigtoolbar").jqxToolBar({theme:theme,
			tools : "button | custom",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					case 0:
						tool.jqxButton({width:80});
						tool.text("添加");
						tool.on("click",function(event){
							disable_autotestconfig_toolbar();
							click_add_autotestconfig();
						});
						break;
					case 1:
					    var searchbox=$("<div id='autotestconfigsearchbox'><input id='autotestconfigsearchinput'  type='text'/><div id='autotestconfigsearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    tool.append(searchbox);
					    // var source ={
                            // datatype: "json",
                            // datafields:[{name:'autotestconfigname'}],
                            // url: '/autotesting/autotestconfig/get_taskname_list'
                            // };
                        // var dataAdapter = new $.jqx.dataAdapter(source);
					    searchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						break;
				}
			}
		});
	}
	
	//auto task 创建
	
	
	
	function create_autotestconfig(autotestconfigid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#autotestconfig_nameInput', message: '任务名称 是必填项!', action: 'keyup, blur', rule: 'required' },
                       { input: '#autotestconfig_nameInput', message: '配置名称已经存在！', action: 'keyup, blur', rule: validate_autotestconfig_name },
                       { input: '#autotestconfig_codeURLInput', message: '代码地址是必填项!', action: 'keyup, blur', rule: 'required' },
                       { input: '#autotestconfig_tasktypedropdownlist', message: '测试任务类型是必填项！', action: 'keyup, blur', rule:validate_autotestconfig_tasktype},
                       { input: '#autotestconfig_projectcombo', message: '测试项目是必选项!', action: 'keyup, blur', rule: validate_autotestconfig_project },
                       { input: '#autotestconfig_projectversioncombo', message: '测试用例是必选项！', action: 'keyup, blur', rule: validate_autotestconfig_projectversion },            
                       { input: '#autotestconfig_runtiming_input', message: '测试用例是必选项！', action: 'keyup, blur', rule:'required' }
                       ];
                       
		    $("#autotestconfig_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#autotestconfig_create").css('visibility', 'visible');
            $('#sendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#autotestconfig_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#autotestconfig_create_backbutton").on('click',function(){
            	$('#autotestconfig_create_form').jqxValidator('hide');
            	loadautotestconfigpage();
            }); 

              init_autotestconfig_name(autotestconfigid);
              // init_autotestconfig_os(autotestconfigid);
              // init_autotestconfig_osversion(autotestconfigid);
              init_autotestconfig_tasktype(autotestconfigid);
              // init_autotestconfig_browser(autotestconfigid);
              // init_autotestconfig_testingenv(autotestconfigid);
              init_autotestconfig_runtiming(autotestconfigid);
              init_autotestconfig_project(autotestconfigid);
              // init_autotestconfig_projectversion(autotestconfigid,0);
              init_autotestconfig_splittask(autotestconfigid);
              init_autotestconfig_viewscope(autotestconfigid);
              init_autotestconfig_codeurl(autotestconfigid);
              init_autotestconfig_driver(autotestconfigid);
              init_autotestconfig_driverargs(autotestconfigid);
              
              change_project_handler(autotestconfigid);
              change_tasktype_handler(autotestconfigid);
            $("#autotestconfig_advance_button").jqxButton({theme:theme, width: '80'});
            $("#autotestconfig_advance_button").on('click',function(){
                 $("tr[class=autotestconfig_advance]").toggle();
            });
            
            $('#sendButton').on('click', function () 
            {
                $('#autotestconfig_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#autotestconfig_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(autotestconfigid==0)
            	 {
            	 	send_createautotestconfig_request();
            	 }
            	 else
            	 {
            	 	send_editautotestconfig_request(autotestconfigid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_autotestconfig_name(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGNAME"},function(data,status){
			 $("#autotestconfig_nameInput").jqxInput({theme:theme,placeHolder:"请输入任务名称!", width: 350, height: 25});
            if(data!="")
          {
        	$("#autotestconfig_nameInput").jqxInput("val",data);
          }       			
		});
	}
	
	function validate_autotestconfig_name()
	{
		var autotestconfigname=$("#autotestconfig_nameInput").jqxInput("val");
		var result=false;
		if(autotestconfigid!=0)
		{
			result=true;
		}
		else
		{
			$.ajax({  
                async:false,
                type: "POST",  
                url: "/autotesting/autotestconfig/check_name_exits",  
                data: "autotestconfigname="+autotestconfigname,  
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
	
	
	
	//初始化代码地址
	
	//初始化任务名称字段
	function init_autotestconfig_codeurl(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGCODEURL"},function(data,status){
			 $("#autotestconfig_codeURLInput").jqxInput({theme:theme,placeHolder:"请输入测试代码地址!", width: 350, height: 25});
            if(data!="")
          {
        	$("#autotestconfig_codeURLInput").jqxInput("val",data);
          }       			
		});
	}
	
	//初始化测试配置os
	
	function init_autotestconfig_os(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGOS"},function(data,status){
			var autotestconfigtype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotestconfig_OSdropdownlist").jqxDropDownList({theme:theme,selectedIndex:0,source: autotestconfigtype_source, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in autotestconfigtype_source)
			{
				if(autotestconfigtype_source[i].selected==1)
				{
					var selectItem=$("#autotestconfig_OSdropdownlist").jqxDropDownList('getItem',Number(i));
					$("#autotestconfig_OSdropdownlist").jqxDropDownList('selectItem',selectItem);
					break;
				}
				
			}
			var osid= $("#autotestconfig_OSdropdownlist").jqxDropDownList('getSelectedItem').value;
   	  	    init_autotestconfig_osversion(autotestconfigid,osid);
			});		           
	}
	
	
	//autotestconfig_config validate function
	
	function validate_autotestconfig_os()
	{
		var result=false;
		var item = $("#autotestconfig_OSdropdownlist").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
	}
	
	 //os change event
   function change_os_handler(autotestconfigid)
   {
   	  $("#autotestconfig_OSdropdownlist").on("change",function(){
   	  	 var osid= $("#autotestconfig_OSdropdownlist").jqxDropDownList('getSelectedItem').value;
   	  	 init_autotestconfig_osversion(autotestconfigid,osid);
   	  });
   	  
   	  
   }
	
	//初始化测试配置os
	
	function init_autotestconfig_osversion(autotestconfigid,os)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGOSVERSION",os:os},function(data,status){
			var autotestconfigtype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotestconfig_OSVersiondropdownlist").jqxDropDownList({theme:theme,selectedIndex:0,source: autotestconfigtype_source, width: 350, height: 25,displayMember: 'text',valueMember:'value'});
			for(var i in autotestconfigtype_source)
			{
				if(autotestconfigtype_source[i].selected==1)
				{
					var selectItem=$("#autotestconfig_OSVersiondropdownlist").jqxDropDownList('getItem',Number(i));
					$("#autotestconfig_OSVersiondropdownlist").jqxDropDownList('selectItem',selectItem);
					break;
				}
				
			}
			});		           
	}
	
	
	//autotestconfig_config validate function
	
	function validate_autotestconfig_osversion()
	{
		var result=false;
		var item = $("#autotestconfig_OSVersioncombo").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
	}
	//初始化测试配置控件
	
	function init_autotestconfig_browser(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGBROWSER"},function(data,status){
			var autotestconfigtype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotestconfig_browser_dropdownlist").jqxComboBox({theme:theme,selectedIndex:0,source:autotestconfigtype_source,multiSelect:true, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in autotestconfigtype_source)
			{
				if(autotestconfigtype_source[i].selected==1)
				{
					var selectItem=$("#autotestconfig_browser_dropdownlist").jqxComboBox('getItem',Number(i));
					$("#autotestconfig_browser_dropdownlist").jqxComboBox('selectItem',selectItem);
				}
				
			}
		});           
	}
	
	

   
   //初始化测试任务类型控件
	
	function init_autotestconfig_tasktype(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGTASKTYPE"},function(data,status){
			var autotestconfigtype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotestconfig_tasktypedropdownlist").jqxDropDownList({theme:theme,selectedIndex:selectedIndex,source:autotestconfigtype_source, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in autotestconfigtype_source)
			{
				if(autotestconfigtype_source[i].selected==1)
				{
					// selectedIndex=i;
				    var selectItem=$("#autotestconfig_tasktypedropdownlist").jqxDropDownList('getItem',Number(i));
					$("#autotestconfig_tasktypedropdownlist").jqxDropDownList('selectItem',selectItem);
					break;
				}
				
			}
		    show_optional_field();
		});
	}
	
	
	//autotestconfig_type validate function
	
	function validate_autotestconfig_tasktype()
	{
		var result=false;
		var item = $("#autotestconfig_tasktypedropdownlist").jqxDropDownList('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
   
   //TASK TYPE change event
   function change_tasktype_handler(autotestconfigid)
   {
   	  $("#autotestconfig_tasktypedropdownlist").on("change",function(){
   	  	 show_optional_field(autotestconfigid);
   	  });
   }
   
   //show or hide optional filed
   function show_optional_field(autotestconfigid)
   {
   	var item = $("#autotestconfig_tasktypedropdownlist").jqxDropDownList('getSelectedItem');
   	  	 switch(item.label)
   	  	 {
   	  	 	case 'WebUI':
   	  	 	    $("#autotestconfig_browser").show();
   	  	 	    $("#autotestconfig_testingenv").show();
   	  	 	    $("#autotestconfig_os").hide();
   	  	 	    $("#autotestconfig_osversion").hide();
   	  	 	       	     init_autotestconfig_browser(autotestconfigid);
         init_autotestconfig_testingenv(autotestconfigid);
   	  	 	    break;
   	  	 	case 'APPUI':
   	  	 	    $("#autotestconfig_browser").hide();
   	  	 	    $("#autotestconfig_testingenv").hide();
   	  	 	    $("#autotestconfig_os").show();
   	  	 	    $("#autotestconfig_osversion").show();
   	  	 	    init_autotestconfig_os(autotestconfigid);
   	  	 	    change_os_handler(autotestconfigid);
   	  	 	    break;
   	  	 	default:
   	  	 	     $("#autotestconfig_browser").hide();
   	  	 	    $("#autotestconfig_testingenv").hide();
   	  	 	    $("#autotestconfig_os").hide();
   	  	 	    $("#autotestconfig_osversion").hide();
   	  	 	    break;
   	  	 	    
   	  	 }
   }

   
  // 初始化autotestconfig_assgin_agent
  function init_autotestconfig_testingenv(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGTESTINGENV"},function(data,status){
			var autotestconfigtype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotestconfig_testingenv__dropdownlist").jqxDropDownList({theme:theme,selectedIndex:0,source: autotestconfigtype_source, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in autotestconfigtype_source)
			{
				if(autotestconfigtype_source[i].selected==1)
				{
					var selectItem=$("#autotestconfig_testingenv__dropdownlist").jqxDropDownList('getItem',Number(i));
					$("#autotestconfig_testingenv__dropdownlist").jqxDropDownList('selectItem',selectItem);
					break;
				}
				
			}
		});           
	}

  function validate_autotestconfig_testingenv()
	{
		var result=false;
		var item = $("#autotestconfig_testingenv_combo").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
	}
 //初始化项目组合框
  function init_autotestconfig_project(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGPROJECT"},function(data,status){
			var autotestconfigproject_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotestconfig_projectcombo").jqxComboBox({theme:theme,selectedIndex:selectedIndex,source: autotestconfigproject_source, multiSelect:false, width: 350, height: 25,displayMember:'text',valueMember:'memberid',searchMode: 'contains',autoComplete:true});
			for(var i in autotestconfigproject_source)
			{
				if(autotestconfigproject_source[i].selected==1)
				{
					var selectItem=$("#autotestconfig_projectcombo").jqxComboBox('getItem',Number(i));
					$("#autotestconfig_projectcombo").jqxComboBox('selectItem',selectItem);
					// selectedIndex=i;
					break;
				}
				
			}
			var projectid= $("#autotestconfig_projectcombo").jqxComboBox('getSelectedItem').value;
			init_autotestconfig_projectversion(autotestconfigid,projectid);
		});           
	}
	
	
	
	 //TASK project change event
   function change_project_handler(autotestconfigid)
   {
   	  $("#autotestconfig_projectcombo").on("change",function(){
   	  	 var projectid= $("#autotestconfig_projectcombo").jqxComboBox('getSelectedItem').value;
   	  	 init_autotestconfig_projectversion(autotestconfigid,projectid);
   	  });
   	  
   	  
   }
	
  //autotestconfig_project validate function
	
	function validate_autotestconfig_project()
	{
		var result=false;
		var item = $("#autotestconfig_projectcombo").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
   
   
   //初始化项目组合框
  function init_autotestconfig_projectversion(autotestconfigid,projectid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGVERSION",projectid:projectid},function(data,status){
			var autotestconfigproject_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotestconfig_projectversioncombo").jqxComboBox({theme:theme,selectedIndex:selectedIndex,source: autotestconfigproject_source, multiSelect:false, width: 350, height: 25,displayMember:'text',valueMember:'memberid',searchMode: 'contains',autoComplete:true});
			for(var i in autotestconfigproject_source)
			{
				if(autotestconfigproject_source[i].selected==1)
				{
					var selectItem=$("#autotestconfig_projectversioncombo").jqxComboBox('getItem',Number(i));
					$("#autotestconfig_projectversioncombo").jqxComboBox('selectItem',selectItem);
					break;
				}
				
			}
		});           
	}
	
//autotestconfig_projectversion validate function
	
	function validate_autotestconfig_projectversion()
	{
		var result=false;
		var item = $("#autotestconfig_projectcombo").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
	
   //初始化任务拆分选项
   
   function init_autotestconfig_splittask(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGSPLIT"},function(data,status){
			var selectedIndex=0;
			if(data=="True")
			{
				selectedIndex=1;
			}
			var countries =[{text:"否",value:0},{text:"是",value:1}];
            $("#autotestconfig_splittask_dropdownlist").jqxDropDownList({theme:theme,source: countries, width: 350, height: 25,selectedIndex:selectedIndex,displayMember:'text',valueMember:'value'});           
		});
	}
	
	
	//初始化执行driver
	 function init_autotestconfig_driver(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGDRIVER"},function(data,status){
			var autotestconfigproject_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autotestconfig_driver_dropdownlist").jqxComboBox({theme:theme,selectedIndex:selectedIndex,source: autotestconfigproject_source, multiSelect:false, width: 350, height: 25,displayMember:'text',valueMember:'memberid',searchMode: 'contains',autoComplete:true});
			for(var i in autotestconfigproject_source)
			{
				if(autotestconfigproject_source[i].selected==1)
				{
					var selectItem=$("#autotestconfig_driver_dropdownlist").jqxComboBox('getItem',Number(i));
					$("#autotestconfig_driver_dropdownlist").jqxComboBox('selectItem',selectItem);
					break;
				}
				
			}
		});
	}
	
	// 初始化新增功能
  function init_autotestconfig_driverargs(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGDRIVERARGS"},function(data,status)
		{
			$("#autotestconfig_driverargs_testarea").jqxEditor({
				theme:theme,
                height: 200,
                width: 350,
                tools: 'bold'
            });
			if(data!="")
             {
        	  $("#autotestconfig_driverargs_testarea").jqxEditor("val",data);
             }       		
		});           
	}

	
   //发送创建任务请求
   function send_createautotestconfig_request()
   {
   	  var autotestconfig_field=$('#autotestconfig_create_form').serialize();
   	  $.post("/autotesting/autotestconfig/create",$('#autotestconfig_create_form').serialize(),function(data,status){
          loadautotestconfigpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_editautotestconfig_request(autotestconfigid)
   {
   	  var autotestconfig_field=$('#autotestconfig_create_form').serialize();
   	  $.post("/autotesting/autotestconfig/edit",$('#autotestconfig_create_form').serialize()+"&autotestconfigid="+autotestconfigid,function(data,status){
          loadautotestconfigpage();
   	  });
   	  
   }
   

 
     
    //初始化任务拆分选项
   
   function init_autotestconfig_viewscope(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGVIEWSCOPE"},function(data,status){
			var selectedIndex=0;
			if(data=="1")
			{
				selectedIndex=1;
			}
			var countries =[{text:"所有人可见",value:0},{text:"仅自己可见",value:1}];
            $("#autotestconfig_viewscope_dropdownlist").jqxDropDownList({theme:theme,source: countries, width: 350, height: 25,selectedIndex:selectedIndex,displayMember:'text',valueMember:'value'}); 
			});          
	}
	
	
	//初始化任务拆分选项
   
   function init_autotestconfig_runtiming(autotestconfigid)
	{
		$.post("/autotesting/autotestconfig/init_autotestconfig_formcontrol",{autotestconfigid:autotestconfigid,controlname:"AUTOTESTCONFIGRUNTIMING"},function(data,status){
            $("#autotestconfig_runtiming_input").jqxDateTimeInput({ width: '350px', height: '25px', formatString: 'HH:mm:ss', showCalendarButton: false,allowNullDate: true});
              if(data!="")
            {
        	   $("#autotestconfig_runtiming_input").jqxDateTimeInput("val",data);
            }       			
			});          
	}
     
	//点击添加自动化任务按钮
	
	function click_add_autotestconfig()
	{
		$("#middleContainer").load("/autotesting/autotestconfig/create", function() {
			  create_autotestconfig(0);
		});
	}
	
	//编辑自动化任务
	function edit_autotestconfig(autotestconfigid)
	{
		$("#middleContainer").load("/autotesting/autotestconfig/edit", function() {
			  create_autotestconfig(autotestconfigid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_autotestconfig_toolbar()
	{
		$("#autotestconfigtoolbar").jqxToolBar("disableTool",0, true);
	    $("#autotestconfigtoolbar").jqxToolBar("disableTool",1, true);
		$("#autotestconfigtoolbar").jqxToolBar("disableTool",2, true);
		$("#autotestconfigtoolbar").jqxToolBar("disableTool",3, true);
	}
	
    
	loadpagenation(get_search_keyword());
	function loadpagenation(searchkeyword) 
	{
		$.post("/autotesting/autotestconfig/get_autotestconfig_page_counts", {
			searchkeyword : searchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					searchkeyword = $('#autotestconfigsearchinput').val();
					if (searchkeyword == "") 
					{
						 searchkeyword = "ALL";
					}
					loadList("getlist", "autotestconfig", page,searchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadautotestconfigpage() {
		$("#middleContainer").load("/autotesting/autotestconfig/index", function() {
			$.getScript("/static/autotesting/js/autotestconfig.js");
			loadautotestconfigtoolbar();
		});
	}
	
	//复制提测项目
	function copyautotestconfig() {
		$("#header_copy").click(function() {
			var $chk = $("[name = selectautotestconfig:checkbox");
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
				autotestconfigid = $chk.filter(":checked").parent().find("span[class=autotestconfigidcontent]").text().trim();
				$.get("/autotesting/autotestconfig/copy_autotestconfig", {
					id : autotestconfigid
				}, function(data, status) {
					$("#dialog-confirm").empty();
					$("#dialog-confirm").append(data);
					$("#dialog-confirm").dialog("open");
					searchkeyword = $('#autotestconfigsearchinput').val();
					if (searchkeyword == "") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "autotestconfig", currnetpageindex, searchkeyword);
				});
			}
		});
	}
	
	//search submition
	function searchautotestconfig() {
		//点击搜索按钮
		$("#autotestconfigsearchbutton").click(function() 
		{
			search_autotestconfig_bykeyword();
		});
		
		$('#autotestconfigsearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_autotestconfig_bykeyword();
				}
			});
	}
	
	//search submition
	function search_autotestconfig_bykeyword()
	{
		    searchkeyword = $('#autotestconfigsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}

			loadpagenation(searchkeyword);
			loadList("getlist", "autotestconfig", 1, searchkeyword);
	}
	
	//获取当前搜索关键字
	function get_search_keyword()
	{
		searchkeyword = $('#autotestconfigsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}
		return searchkeyword;
	}
	
	//删除任务确认
	
	function delete_autotestconfig() {
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
					$.post("/autotesting/autotestconfig/deleteautotestconfig",{autotestconfigid:autotestconfigid},function(data,status){
				loadList("getlist", "autotestconfig",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
				},
				"否" : function() {
					$(this).dialog("close");
				}
			},
			close : function() {
				allFields.removeClass("ui-state-error");
			}
		});
	


});
