$(document).ready(function() {
	
	
	var currnetpageindex = 1;
	var searchkeyword="ALL";
	var testprojectid=0;
	var theme='arctic';
	alert("est");
	load_testproject_List("getlist", "testproject",currnetpageindex,"ALL");
    
    loadtestprojecttoolbar();
    searchtestproject();

	//加载对象列表容器
	function load_testproject_List(listmethod, objectType, pageindex, searchkeyword) {
		//加载列表
		$("#testprojectlistcontainer").load("/functiontesting/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			searchkeyword : searchkeyword
		}, function(data, status) {
			show_testproject_rowmenu();
			testproject_row_menu_event_handle();
		});

	}
	
	
	//show row operation menu
	function show_testproject_rowmenu()
	{
		var contextMenu = $("#testprojectrowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=testprojectrowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=testprojectidcontent]");
                	    testprojectid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=testprojectrowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function testproject_row_menu_event_handle()
	{
		$("li[name=testprojectrowoperationedit]").click(function(){
			disable_testproject_toolbar();
			edit_testproject(testprojectid);
		});
		$("li[name=testprojectrowoperationdelete]").click(function(){
			
			$("#test_project_dialog-confirmdelete").empty();
			$("#test_project_dialog-confirmdelete").append("确定要删除ID为" +testprojectid + "的项目吗？");
			$("#test_project_dialog-confirmdelete").dialog("open");
		});
		$("li[name=testprojectrowoperationversion]").click(function(){
			init_version_page(testprojectid);
		});
		
		$("li[name=testprojectrowoperationcopy]").click(function(){
			$.post("/functiontesting/testproject/copytestproject",{testprojectid:testprojectid},function(data,status){
				load_testproject_List("getlist", "testproject",currnetpageindex,get_testprojct_searchkeyword());
				load_testproject_pagenation(get_testprojct_searchkeyword());
			});
		});
	}

	//双击测试计划行
	function clickrowedit() {
		$("button[name=testprojectrowedit]").click(function() {
			testprojectid = $(this).parent().parent().find("span[class=testprojectidcontent]").text().trim();
			disable_testproject_toolbar();
			edit_testproject(testprojectid);

		});
	}
	
	
	function loadtestprojecttoolbar()
	{
		$("#testprojecttoolbar").jqxMenu({theme:theme,
			animationShowDuration : 300,
			animationHideDuration : 200,
			animationShowDelay : 200,
			showTopLevelArrows: true,
			height:35,
			autoOpen:false
			
		});
		$("#testprojecttoolbar").css('visibility', 'visible');
		$("#testprojectsearchbox").jqxInput({theme:theme, placeHolder: "请输入项目ID或者名称", height: 23, width: 250, minLength: 1});
		 $('#testprojecttoolbar').on('itemclick', function (event) {
		 	var itemtext=event.target.id;
		 	  switch(itemtext)
		 	{
		 		case "testproject_add_project":
		 		     disable_testproject_toolbar();
					 click_add_testproject();
		 		     break;
		 		case "testproject_add_version":
		 		click_add_projectversion();
		 		disable_testproject_toolbar();
		 		     break; 
		 		case "testproject_view_project":
		 		     break; 
		 	    case "testproject_view_version":
		 		     break; 
		 	}	
  });
		
	}

	//auto task 创建
	
	function create_testproject(testprojectid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#testproject_nameInput', message: '项目名称是必填项!', action: 'keyup, blur', rule:'required' },
                       { input: '#testproject_keyInput', message: '项目标示是必填项!', action: 'keyup, blur', rule:'required' },
                       //{ input: '#testproject_lead_combo', message: 'Job名称是必填项', action: 'keyup, blur', rule: 'required' }
                       ];
                       
		    $("#testproject_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#testproject_create").css('visibility', 'visible');
            $('#testprojectsendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#testproject_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#testproject_create_backbutton").on('click',function(){
            	$('#testproject_create_form').jqxValidator('hide');
            	loadtestprojectpage();
            }); 

              init_testproject_name(testprojectid);
              init_testproject_key(testprojectid);
              init_testproject_lead(testprojectid);
           
           $('#testprojectsendButton').on('click', function () {
                $('#testproject_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#testproject_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(testprojectid==0)
            	 {
            	 	send_createtask_request();
            	 }
            	 else
            	 {
            	 	send_edittask_request(testprojectid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_testproject_name(testprojectid)
	{
		$.post("/functiontesting/testproject/init_testproject_formcontrol",{testprojectid:testprojectid,controlname:"TESTPROJECTNAME"},function(data,status)
		{
			$("#testproject_nameInput").jqxInput({theme:theme, placeHolder:"请输入项目名称！", width: 350, height: 25});
			if(data!="")
          {
        	 $("#testproject_nameInput").jqxInput("val",data);
          }       		
		});
	}


	function init_testproject_key(testprojectid)
	{
		$.post("/functiontesting/testproject/init_testproject_formcontrol",{testprojectid:testprojectid,controlname:"TESTPROJECTKEY"},function(data,status)
		{
			$("#testproject_keyInput").jqxInput({theme:theme, placeHolder:"请输入项目标示！", width: 350, height: 25});
			if(data!="")
          {
        	 $("#testproject_keyInput").jqxInput("val",data);
          }       		
		});
	}
	
	function validate_testproject_name()
	{
		var testprojectname=$("#testproject_nameInput").jqxInput("val");
		var result=false;
		if(testprojectid!=0)
		{
			result=true;
		}
		else
		{
		  $.ajax({  
                async:false,
                type: "POST",  
                url: "/functiontesting/testproject/check_name_exits",  
                data: "testprojectname="+testprojectname,  
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
	
	function init_testproject_lead(testprojectid)
	{
		$.post("/functiontesting/testproject/init_testproject_formcontrol",{testprojectid:testprojectid,controlname:"TESTPROJECTLEAD"},function(data,status){
			var testproject_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#testproject_lead_combo").jqxComboBox({theme:theme,source: testproject_source, multiSelect: false, width: 350, height: 25,displayMember:'text',valueMember: 'memberid', searchMode:'contains',autoComplete:true});
			for(var i in testproject_source)
			{
				if(testproject_source[i].selected==1)
				{
					var selectedItem=$("#testproject_lead_combo").jqxComboBox('getItem',Number(i));
			        $("#testproject_lead_combo").jqxComboBox('selectItem',selectedItem);
					break;
				}
				
			}
         });
	}

              
   //发送创建任务请求
   function send_createtask_request()
   {
   	  var testproject_field=$('#testproject_create_form').serialize();
   	  $.post("/functiontesting/testproject/create",$('#testproject_create_form').serialize(),function(data,status){
          loadtestprojectpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_edittask_request(testprojectid)
   {
   	  var testproject_field=$('#testproject_create_form').serialize();
   	  $.post("/functiontesting/testproject/edit",$('#testproject_create_form').serialize()+"&testprojectid="+testprojectid,function(data,status){
          loadtestprojectpage();
   	  });
   	  
   }
   
	//点击添加自动化任务按钮
	
	function click_add_testproject()
	{
		$("#middleContainer").load("/functiontesting/testproject/create", function() {
			  create_testproject(0);
		});
	}
	
	//编辑自动化任务
	function edit_testproject(testprojectid)
	{
		$("#middleContainer").load("/functiontesting/testproject/edit", function() {
			  create_testproject(testprojectid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_testproject_toolbar()
	{
		$("#testprojecttoolbar").jqxToolBar("disableTool",0, true);
	    $("#testprojecttoolbar").jqxToolBar("disableTool",1, true);
		$("#testprojecttoolbar").jqxToolBar("disableTool",2, true);
		$("#testprojecttoolbar").jqxToolBar("disableTool",3, true);
	}
	
    
	load_testproject_pagenation(get_testprojct_searchkeyword());
	function load_testproject_pagenation(searchkeyword) 
	{
		$.post("/functiontesting/testproject/get_testproject_page_counts", {
			searchkeyword : searchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					load_testproject_List("getlist", "testproject", page,searchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadtestprojectpage() {
		$("#middleContainer").load("/functiontesting/testproject/index", function() {
			$.getScript("/static/testjob/js/testproject.js");
			loadtestprojecttoolbar();
		});
	}
	
	// 清理左右 栏自动化任务页面
	function load_projectversion_page() {
		$("#middleContainer").load("/functiontesting/projectversion/index", function() 
		{
			$.getScript("/static/testjob/js/projectversion.js");
	    });
	   }
	//search job
	function searchtestproject() {
		//点击搜索按钮
		$("#testprojectsearchbutton").click(function() 
		{
			search_testproject_bykeyword();
		});
		
		$('#testprojectsearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_testproject_bykeyword();
				}
			});
	}
	
	//search job
	function search_testproject_bykeyword()
	{
			load_testproject_pagenation(searchkeyword);
			load_testproject_List("getlist", "testproject", 1, get_testprojct_searchkeyword());
	}
	
	//获取当前搜索关键字
	function get_testprojct_searchkeyword()
	{
		searchkeyword = $('#testprojectsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}
		return searchkeyword;
	}
	
	//删除任务确认
	
	$("#test_project_dialog-confirmdelete").dialog({
			autoOpen : false,
			height : 200,
			width : 300,
			modal : true,
			buttons : {
				"是" : function() 
				{
					$(this).dialog("close");
					$.post("/functiontesting/testproject/deletetestproject",{testprojectid:testprojectid},function(data,status){
				         load_testproject_List("getlist", "testproject",currnetpageindex,get_testprojct_searchkeyword());
				         load_testproject_pagenation(get_testprojct_searchkeyword());
			      });
				},
				"否" : function() {
					$(this).dialog("close");
				}
			},
			close : function() {
			}
		});
	
	
	$("#test_project_dialog-confirm").dialog({
			autoOpen : false,
			height : 200,
			width : 300,
			modal : true,
			buttons : {
				OK : function() {
					$(this).dialog("close");
				}
			},
			close : function() {
			}
		});
		
/*********** *****************************************************************************************************************************************/
/****************************************************************************************************************************************************/
/***********************************************************项目版本相关 JS*****************************************************************************************/
/****************************************************************************************************************************************************/
/****************************************************************************************************************************************************/


var pvpageindex = 1;
	var pvsearchkeyword="ALL";
	var projectversionid=0;
	var projectid=0;
	
	
	function init_version_page(projectid)
	{
		projectid=projectid;
		$("#middleContainer").load("/functiontesting/projectversion/index", function() 
		{
		load_projectversion_List("getlist", "projectversion",pvpageindex,"ALL",projectid);
        load_projectversion_toolbar();  
        // searchprojectversion();
        load_projectversion_pagenation(get_projectversion_searchkeyword());
		});
	}

   
 
	//加载对象列表容器
	function load_projectversion_List(listmethod, objectType, pageindex, pvsearchkeyword,projectid) {
		//加载列表
		$("#projectversionlistcontainer").load("/functiontesting/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			pvsearchkeyword : pvsearchkeyword,
			projectid,projectid
		}, function(data, status) {
			// show_projectversion_rowmenu();
			// projectversion_row_menu_event_handle();    
			projectversion_clickrowedit();          
		});

	}
	
	
	//show row operation menu
	function show_projectversion_rowmenu()
	{
		var contextMenu = $("#projectversionrowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=projectversionrowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=projectversionidcontent]");
                	    projectversionid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=projectversionrowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function projectversion_row_menu_event_handle()
	{
		$("li[name=projectversionrowoperationedit]").click(function(){
			disable_projectversion_toolbar();
			edit_projectversion(projectversionid);
		});
		$("li[name=projectversionrowoperationdelete]").click(function(){
			
			$("#test_project_dialog-confirmdelete").empty();
			$("#test_project_dialog-confirmdelete").append("确定要删除ID为" +projectversionid + "的项目吗？");
			$("#test_project_dialog-confirmdelete").dialog("open");
		});
		$("li[name=projectversionrowoperationdetail]").click(function(){
		});
		
		$("li[name=projectversionrowoperationcopy]").click(function(){
			$.post("/functiontesting/projectversion/copyprojectversion",{projectversionid:projectversionid},function(data,status){
				load_projectversion_List("getlist", "projectversion",pvpageindex,get_projectversion_searchkeyword());
				load_projectversion_pagenation(get_projectversion_searchkeyword());
			});
		});
	}



	//双击测试计划行
	function projectversion_clickrowedit() {
		$("button[name=projectversionrowedit]").click(function() {
			projectversionid = $(this).parent().parent().find("span[class=projectversionidcontent]").text().trim();
			disable_projectversion_toolbar();
			edit_projectversion(projectversionid);
		});
	}
	
	
	
	//加载自动化任务工具栏
	function load_projectversion_toolbar() {
		$("#projectversiontoolbar").jqxToolBar({theme:theme,
			tools : "button",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					case 0:
					     tool.jqxButton({width:80});
						tool.text("返回");
						tool.on("click",function(event){
							loadtestprojectpage();
						});
						break;
					   
					// case 1:
						// tool.jqxButton({width:80});
						// tool.text("添加");
						// tool.on("click",function(event){
							// disable_projectversion_toolbar();
							// click_add_projectversion();
						// });
						// break;
					// case 2:
					    // var projectversionsearchbox=$("<div id='projectversionsearchbox'><input id='projectversionsearchinput'  type='text'/><div id='projectversionsearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    // tool.append(projectversionsearchbox);
					    // projectversionsearchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						// break;
				}
			}
		});
	}

	
	//auto task 创建
	
	
	function create_projectversion(projectversionid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#projectversion_project_combo', message: '提测ID是必填项!', action: 'blur', rule:validate_projectversion_project },
                       { input: '#projectversion_versionInput', message: '提测ID是必填项!', action: 'keyup, blur', rule:'required' },
                       { input: '#projectversion_testers_combo', message: '提测ID是必填项!', action: 'blur', rule:validate_projectversion_testers },
                       { input: '#projectversion_developers_combo', message: '提测ID是必填项!', action: 'blur', rule:validate_projectversion_developers },
                       //{ input: '#projectversion_lead_combo', message: 'Job名称是必填项', action: 'keyup, blur', rule: 'required' }
                       ];
                       
		    $("#projectversion_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#projectversion_create").css('visibility', 'visible');
            $('#projectversionsendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#projectversion_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#projectversion_create_backbutton").on('click',function(){
            	$('#projectversion_create_form').jqxValidator('hide');
            	loadtestprojectpage();
            }); 

              init_projectversion_project(projectversionid);
              init_projectversion_version(projectversionid);
              init_projectversion_testers(projectversionid);
              init_projectversion_developers(projectversionid);
              init_projectversion_pms(projectversionid);
            
           $('#projectversionsendButton').on('click', function () {
                $('#projectversion_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#projectversion_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(projectversionid==0)
            	 {
            	 	send_createprojectversion_request();
            	 }
            	 else
            	 {
            	 	send_editprojectversion_request(projectversionid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_projectversion_project(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"PVPROJECT"},function(data,status)
		{
			var projectversion_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#projectversion_project_combo").jqxComboBox({theme:theme,source: projectversion_source, multiSelect:false, width: 350, height: 25,displayMember:'text',valueMember: 'memberid', searchMode:'contains',autoComplete:true});
			for(var i in projectversion_source)
			{
				if(projectversion_source[i].selected==1)
				{
					var selectedItem=$("#projectversion_project_combo").jqxComboBox('getItem',Number(i));
			        $("#projectversion_project_combo").jqxComboBox('selectItem',selectedItem);
					break;
				}
				
			}
		});
	}
	
	
	function validate_projectversion_project()
	{
		var result=false;
		var item = $("#projectversion_project_combo").jqxComboBox('getSelectedItems');
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }


	function init_projectversion_version(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"PVVERSION"},function(data,status)
		{
			$("#projectversion_versionInput").jqxInput({theme:theme, placeHolder:"请输入版本号！", width: 350, height: 25});
			if(data!="")
          {
        	 $("#projectversion_versionInput").jqxInput("val",data);
          }       		
		});
	}
		
	
	
	//初始化测试配置控件
	
	function init_projectversion_testers(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"PVTESTERS"},function(data,status){
			var projectversion_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#projectversion_testers_combo").jqxComboBox({theme:theme,source: projectversion_source, multiSelect: true, width: 350, height: 25,displayMember:'text',valueMember: 'memberid', searchMode:'contains',autoComplete:true});
			for(var i in projectversion_source)
			{
				if(projectversion_source[i].selected==1)
				{
					var selectedItem=$("#projectversion_testers_combo").jqxComboBox('getItem',Number(i));
			        $("#projectversion_testers_combo").jqxComboBox('selectItem',selectedItem);
				}
				
			}
         });
	}
	
	function validate_projectversion_testers()
	{
		var result=false;
		var item = $("#projectversion_testers_combo").jqxComboBox('getSelectedItems');
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
	
	
	
	
   
   //初始化测试任务类型控件
	
	function init_projectversion_developers(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"PVDEVELOPERS"},function(data,status)
		{
			var projectversion_source =eval("(" + data + ")");
			var selectedIndex=0;
		$("#projectversion_developers_combo").jqxComboBox({theme:theme,source: projectversion_source, multiSelect: true, width: 350, height: 25,displayMember:'text',valueMember: 'memberid', searchMode:'contains',autoComplete:true});
			for(var i in projectversion_source)
			{
				if(projectversion_source[i].selected==1)
				{
					var selectedItem=$("#projectversion_developers_combo").jqxComboBox('getItem',Number(i));
			        $("#projectversion_developers_combo").jqxComboBox('selectItem',selectedItem);
				}
				
			}
         });
	}
	
	function validate_projectversion_developers()
	{
		var result=false;
		var item = $("#projectversion_developers_combo").jqxComboBox('getSelectedItems');
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
	
	
	

   
  // 初始化新增功能
  function init_projectversion_pms(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"PVPMS"},function(data,status)
		{
			var projectversion_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#projectversion_products_combo").jqxComboBox({theme:theme,source: projectversion_source, multiSelect: true, width: 350, height: 25,displayMember:'text',valueMember: 'memberid', searchMode:'contains',autoComplete:true});
			for(var i in projectversion_source)
			{
				if(projectversion_source[i].selected==1)
				{
					var selectedItem=$("#projectversion_products_combo").jqxComboBox('getItem',Number(i));
			        $("#projectversion_products_combo").jqxComboBox('selectItem',selectedItem);
				}
				
			}
         });
	}
   
              
   //发送创建任务请求
   function send_createprojectversion_request()
   {
   	  var projectversion_field=$('#projectversion_create_form').serialize();
   	  $.post("/functiontesting/projectversion/create",$('#projectversion_create_form').serialize(),function(data,status){
          loadtestprojectpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_editprojectversion_request(projectversionid)
   {
   	  var projectversion_field=$('#projectversion_create_form').serialize();
   	  $.post("/functiontesting/projectversion/edit",$('#projectversion_create_form').serialize()+"&projectversionid="+projectversionid,function(data,status){
          init_version_page(Number(data));
   	  });
   	  
   }
   

 
     
  
	//点击添加自动化任务按钮
	
	function click_add_projectversion()
	{
		$("#middleContainer").load("/functiontesting/projectversion/create", function() {
			  create_projectversion(0);
		});
	}
	
	//编辑自动化任务
	function edit_projectversion(projectversionid)
	{
		$("#middleContainer").load("/functiontesting/projectversion/edit", function() {
			  create_projectversion(projectversionid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_projectversion_toolbar()
	{
		$("#projectversiontoolbar").jqxToolBar("disableTool",0, true);
	    $("#projectversiontoolbar").jqxToolBar("disableTool",1, true);
		$("#projectversiontoolbar").jqxToolBar("disableTool",2, true);
	}
	
	function load_projectversion_pagenation(pvsearchkeyword) 
	{
		$.post("/functiontesting/projectversion/get_projectversion_page_counts", {
			pvsearchkeyword : pvsearchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					pvpageindex = page;
					load_projectversion_List("getlist", "projectversion", page,pvsearchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadprojectversionpage(projectid) {
		$("#middleContainer").load("/functiontesting/projectversion/index", function() {
			init_version_page(projectid);
			load_projectversion_toolbar();
		});
	}
	
	//复制提测项目
	function copyprojectversion() {
		$("#header_copy").click(function() {
			var $chk = $("[name = selectprojectversion:checkbox");
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
				projectversionid = $chk.filter(":checked").parent().find("span[class=projectversionidcontent]").text().trim();
				$.get("/functiontesting/projectversion/copy_projectversion", {
					id : projectversionid
				}, function(data, status) 
				{
					$("#dialog-confirm").empty();
					$("#dialog-confirm").append(data);
					$("#dialog-confirm").dialog("open");
					pvsearchkeyword = $('#projectversionsearchinput').val();
					if (pvsearchkeyword == "") {
						pvsearchkeyword = "ALL";
					}
					load_projectversion_List("getlist", "projectversion", pvpageindex, pvsearchkeyword);
				});
			}
		});
	}
	
	//search job
	function searchprojectversion() {
		//点击搜索按钮
		$("#projectversionsearchbutton").click(function() 
		{
			search_projectversion_bykeyword();
		});
		
		$('#projectversionsearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_projectversion_bykeyword();
				}
			});
	}
	
	//search job
	function search_projectversion_bykeyword()
	{
		    pvsearchkeyword = $('#projectversionsearchinput').val().trim();
			if (pvsearchkeyword == "") {
				pvsearchkeyword = "ALL";
			}

			load_projectversion_pagenation(pvsearchkeyword);
			load_projectversion_List("getlist", "projectversion", 1, pvsearchkeyword);
	}
	
	//获取当前搜索关键字
	function get_projectversion_searchkeyword()
	{
		pvsearchkeyword = $('#projectversionsearchinput').val().trim();
			if (pvsearchkeyword == "") {
				pvsearchkeyword = "ALL";
			}
		return pvsearchkeyword;
	}
	
	//删除任务确认
	
	
	$("#t_project_dialog-confirmdelete").dialog({
			autoOpen : false,
			height : 200,
			width : 300,
			modal : true,
			buttons : {
				"是" : function() 
				{
					$(this).dialog("close");
					$.post("/functiontesting/projectversion/deleteprojectversion",{projectversionid:projectversionid},function(data,status){
				         load_projectversion_List("getlist", "projectversion",pvpageindex,get_projectversion_searchkeyword());
				         load_projectversion_pagenation(get_projectversion_searchkeyword());
			      });
				},
				"否" : function() {
					$(this).dialog("close");
				}
			},
			close : function() {
			}
		});
	
	
	$("#t_project_dialog-confirm").dialog({
			autoOpen : false,
			height : 200,
			width : 300,
			modal : true,
			buttons : {
				OK : function() {
					$(this).dialog("close");
				}
			},
			close : function() {
			}
		});
	


});
