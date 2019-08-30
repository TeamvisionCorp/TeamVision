$(document).ready(function() {

	var currnetpageindex = 1;
	var searchkeyword="ALL";
	var testsubmitionid=0;
	var theme='arctic';

	loadList("getlist", "testsubmition",currnetpageindex,"ALL");
     
    loadtestsubmitiontoolbar();
    
    searchtestsubmition();

 
	//加载对象列表容器
	function loadList(listmethod, objectType, pageindex, searchkeyword) {
		//加载列表
		$("#testsubmitionlistcontainer").load("/functiontesting/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			searchkeyword : searchkeyword
		}, function(data, status) {
			showrowmenu();
			row_menu_event_handle();
			clickpackage();
			submition();
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
		var contextMenu = $("#testsubmitionrowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=testsubmitionrowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=testsubmitionidcontent]");
                	    testsubmitionid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=testsubmitionrowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function row_menu_event_handle()
	{
		$("li[name=testsubmitionrowoperationedit]").click(function(){
			disable_testsubmition_toolbar();
			edit_testsubmition(testsubmitionid);
		});
		$("li[name=testsubmitionrowoperationdelete]").click(function(){
			
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" +testsubmitionid + "的提测项目吗？");
			$("#dialog-confirmdelete").dialog("open");
		});
		$("li[name=testsubmitionrowoperationdetail]").click(function(){
		});
		
		$("li[name=testsubmitionrowoperationcopy]").click(function(){
			$.post("/functiontesting/testsubmition/copytestsubmition",{testsubmitionid:testsubmitionid},function(data,status){
				loadList("getlist", "testsubmition",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
		});
	}


	//点击checkbox

	function clickcheckbox() {
		$("[name = selecttestsubmition]:checkbox").bind("click", function() {
			var $chk = $("[name = selecttestsubmition]:checkbox");
			// $("#testsubmitionselectall").attr("checked", $chk.length == $chk.filter(":checked").length);
		});
		// $("#testsubmitionselectall").bind("click", function() {
			// var $chk = $("[name = selecttestsubmition]:checkbox");
			// if ($chk.filter(":checked").length == $chk.length) {
				// $("[name = selecttestsubmition]:checkbox").attr("checked", false);
			// } else {
				// $("[name = selecttestsubmition]:checkbox").attr("checked", true);
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
		$("li[class=testsubmitiondatarow]").mouseover(function() {
			$(this).addClass("mouseroverdatarow");
		});
		$("li[class=testsubmitiondatarow]").mouseout(function() {
			$(this).removeClass("mouseroverdatarow");
		});
	}
	
	
	
	//加载自动化任务工具栏
	function loadtestsubmitiontoolbar() {
		$("#testsubmitiontoolbar").jqxToolBar({theme:theme,
			tools : "button | custom",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					case 0:
						tool.jqxButton({width:80});
						tool.text("添加");
						tool.on("click",function(event){
							disable_testsubmition_toolbar();
							click_add_testsubmition();
						});
						break;
					case 1:
					    var searchbox=$("<div id='testsubmitionsearchbox'><input id='testsubmitionsearchinput'  type='text'/><div id='testsubmitionsearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    tool.append(searchbox);
					    // var source ={
                            // datatype: "json",
                            // datafields:[{name:'testsubmitionname'}],
                            // url: '/functiontesting/testsubmition/get_taskname_list'
                            // };
                        // var dataAdapter = new $.jqx.dataAdapter(source);
					    searchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						break;
				}
			}
		});
	}
	
	//auto task 创建
	
	
	
	function create_testsubmition(testsubmitionid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#testsubmition_productnamecombo', message: '产品名称是必填项!', action: 'keyup,blur', rule: validate_testsubmition_project },
                       { input: '#testsubmition_versiondropdownlist', message: '请选择版本!', action: 'keyup, blur', rule: validate_testsubmition_version},
                       { input: '#testsubmition_newfeatureInput', message: '新增功能是必填项', action: 'keyup, blur', rule: validate_testsubmition_newfeature },
                       { input: '#testsubmition_bugfixInput', message: 'Bug修复信息是必填项', action: 'keyup, blur', rule: validate_testsubmition_bugfix },
                       { input: '#testsubmition_advice4testingInput', message: '测试建议是必填项!', action: 'keyup, blur', rule: validate_testsubmition_advance },
                       { input: '#testsubmition_jenkinsjobcombo', message: 'JenkinsJob是必填项', action: 'keyup,blur', rule: validate_testsubmition_jenkinsjob },
                       ];
                       
		    $("#testsubmition_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#testsubmition_create").css('visibility', 'visible');
            $('#testsubmitionsendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#testsubmition_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#testsubmition_create_backbutton").on('click',function(){
            	$('#testsubmition_create_form').jqxValidator('hide');
            	loadtestsubmitionpage();
            }); 

              init_testsubmition_platform(testsubmitionid);
              init_testsubmition_projecttype(testsubmitionid);
              init_testsubmition_project(testsubmitionid);
              init_testsubmition_version(testsubmitionid);
              init_testsubmition_newfeature(testsubmitionid);
              init_testsubmition_bugfix(testsubmitionid);
              init_testsubmition_advance(testsubmitionid);
              init_testsubmition_jenkinsserver(testsubmitionid);
              init_testsubmition_cc(testsubmitionid);
              init_testsubmition_buildparameters(testsubmitionid);
              
             change_jenkinsserver_handler(testsubmitionid);
             change_project_handler(testsubmitionid);
            
            $("#testsubmition_advance_button").jqxButton({theme:theme, width: '80'});
            $("#testsubmition_advance_button").on('click',function(){
                 $("tr[class=testsubmition_advance]").toggle();
            });
            
           $('#testsubmitionsendButton').on('click', function () {
                $('#testsubmition_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#testsubmition_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(testsubmitionid==0)
            	 {
            	 	send_createtask_request();
            	 }
            	 else
            	 {
            	 	send_edittask_request(testsubmitionid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_testsubmition_platform(testsubmitionid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TESTSUBMITIONPLATFORM"},function(data,status){
			var testsubmitionplatform_source =eval("(" + data + ")");
			$("#testsubmition_platform_dropdownlist").jqxDropDownList({theme:theme,source: testsubmitionplatform_source,selectedIndex:0, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in testsubmitionplatform_source)
			{
				if(testsubmitionplatform_source[i].selected==1)
				{
					// $("#testsubmition_platform_dropdownlist").jqxDropDownList('selectIndex',i);
					var selectedItem=$("#testsubmition_platform_dropdownlist").jqxDropDownList('getItem',Number(i));
			        $("#testsubmition_platform_dropdownlist").jqxDropDownList('selectItem',selectedItem);
					// selectedIndex=i;
					
					break;
				}
				
			} 
		
		});
	}
	
	function validate_testsubmition_platform()
	{
		var testsubmitionname=$("#testsubmition_nameInput").jqxInput("val");
		var result=false;
		if(testsubmitionid!=0)
		{
			result=true;
		}
		else
		{
		  $.ajax({  
                async:false,
                type: "POST",  
                url: "/functiontesting/testsubmition/check_name_exits",  
                data: "testsubmitionname="+testsubmitionname,  
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
	
	function init_testsubmition_projecttype(testsubmitionid,projectid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TESTSUBMITIONPROJECTTYPE"},function(data,status){
			var testsubmitiontype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#testsubmition_producttype_dropdownlist").jqxDropDownList({theme:theme,source: testsubmitiontype_source,selectedIndex:0, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in testsubmitiontype_source)
			{
				if(testsubmitiontype_source[i].selected==1)
				{
					// selectedIndex=i;
					var selectedItem=$("#testsubmition_producttype_dropdownlist").jqxDropDownList('getItem',Number(i));
			        $("#testsubmition_producttype_dropdownlist").jqxDropDownList('selectItem',selectedItem);
					// $("#testsubmition_producttype_dropdownlist").jqxDropDownList('selectIndex',i);
					break;
				}
				
			}           
			});		
	}
	
	
	
	//testsubmition_config validate function
	
	function validate_testsubmition_projecttype()
	{
		var result=false;
		var item = $("#testsubmition_producttype_dropdownlist").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
	}
	//初始化测试配置控件
	
	function init_testsubmition_project(testsubmitionid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TESTPROJECT"},function(data,status){
			var testsubmitionproject_source =eval("(" + data + ")");
			var selectIndex=0;
			$("#testsubmition_productnamecombo").jqxComboBox({theme:theme,source:testsubmitionproject_source, selectedIndex:0,multiSelect: false, width: 350, height: 25,displayMember:'text',valueMember: 'memberid',searchMode :'contains',autoComplete:true});
			for(var i in testsubmitionproject_source)
			{
				if(testsubmitionproject_source[i].selected==1)
				{
					var selectedItem=$("#testsubmition_productnamecombo").jqxComboBox('getItem',Number(i));
			        $("#testsubmition_productnamecombo").jqxComboBox('selectItem',selectedItem);
					break;
				}
				
			}
			var projectid=$("#testsubmition_productnamecombo").jqxComboBox('getSelectedItem').value;
			init_testsubmition_version(testsubmitionid,projectid);
		});           
	}
	
	 //TASK TYPE change event
   function change_project_handler(testsubmitionid)
   {
   	  $("#testsubmition_productnamecombo").on("change",function(){
   	  	 var projectid= $("#testsubmition_productnamecombo").jqxComboBox('getSelectedItem').value;
   	  	 init_testsubmition_version(testsubmitionid,projectid);
   	  });
   	  
   	  
   }
	
	
	//testsubmition validate function
	
	function validate_testsubmition_project()
	{
		var result=false;
		var item = $("#testsubmition_productnamecombo").jqxComboBox('getSelectedIndex');
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
   
   //初始化测试任务类型控件
	
	function init_testsubmition_version(testsubmitionid,projectid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TESTSUBMITIONPROJECTVERSION",projectid:projectid},function(data,status)
		{
			var testsubmitionproject_source =eval("(" + data + ")");
			var selectIndex=0;
			$("#testsubmition_versiondropdownlist").jqxDropDownList({theme:theme,source:testsubmitionproject_source,selectedIndex:0, width: 350, height: 25,displayMember:'text',valueMember: 'memberid'});
			for(var i in testsubmitionproject_source)
			{
				if(testsubmitionproject_source[i].selected==1)
				{
					var selectedItem=$("#testsubmition_versiondropdownlist").jqxDropDownList('getItem',Number(i));
			        $("#testsubmition_versiondropdownlist").jqxDropDownList('selectItem',selectedItem);
					break;
				}
				
			}
		});
	}
	
	
	//testsubmition_type validate function
	
	function validate_testsubmition_version()
	{
        var result=false;
		var item = $("#testsubmition_versiondropdownlist").jqxDropDownList('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }

   
  // 初始化新增功能
  function init_testsubmition_newfeature(testsubmitionid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TESTSUBMITIONNEWFEATURE"},function(data,status)
		{
			$("#testsubmition_newfeatureInput").jqxEditor({
				theme:theme,
                height: 200,
                width: 350,
                tools: 'bold'
            });
			if(data!="")
             {
        	  $("#testsubmition_newfeatureInput").jqxEditor("val",data);
             }       		
		});           
	}
	
	
	// 验证新增功能
  function validate_testsubmition_newfeature()
	{
        var  value=$("#testsubmition_newfeatureInput").jqxEditor("val");
        var result=false;
        if(value!="<div>​</div>")
        {
        	result=true;
        }
        return result;
	}

 //初始化 bug 修复信息
  function init_testsubmition_bugfix(testsubmitionid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TESTSUBMITIONBUGFIX"},function(data,status){
			$("#testsubmition_bugfixInput").jqxEditor({
				theme:theme,
                height: 200,
                width: 350,
                tools: 'bold'
            });
             if(data!="")
             {
        	  $("#testsubmition_bugfixInput").jqxEditor("val",data);
             }     
		});           
	}
	
 
  function validate_testsubmition_bugfix()
	{
        var  value=$("#testsubmition_bugfixInput").jqxEditor("val").trim();
        var result=false;
        if(value!="<div>​</div>")
        {
        	result=true;
        }
        return result;
	}
	
	//初始化 bug 修复信息
  function init_testsubmition_advance(testsubmitionid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TESTSUBMITIONADVANCE"},function(data,status){
			$("#testsubmition_advice4testingInput").jqxEditor({
				theme:theme,
                height: 200,
                width: 350,
                tools: 'bold'
            });
             if(data!="")
             {
        	  $("#testsubmition_advice4testingInput").jqxEditor("val",data);
             }     
		});           
	}
	
	// 初始化新增功能
  function validate_testsubmition_advance()
	{
		var result=false;
        var  value=$("#testsubmition_advice4testingInput").jqxEditor('val').trim();
        if(value!="<div>​</div>")
        {
        	result=true;
        }
        return result;

	}
	
	 

   //初始化jenkins server
	function init_testsubmition_jenkinsserver(testsubmitionid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TPSJENKINSSERVER"},function(data,status){
			var testsubmitionproject_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#testsubmition_jenkinsserverdropdownlist").jqxDropDownList({theme:theme,source: testsubmitionproject_source, width: 350, height: 25,selectedIndex:selectedIndex,displayMember:'text',valueMember:'memberid'});
			for(var i in testsubmitionproject_source)
			{
				if(testsubmitionproject_source[i].selected==1)
				{
					// $("#testsubmition_jenkinsserverdropdownlist").jqxDropDownList('selectIndex',i);
					var selectItem=$("#testsubmition_jenkinsserverdropdownlist").jqxDropDownList('getItem',Number(i));
					$("#testsubmition_jenkinsserverdropdownlist").jqxDropDownList('selectItem',selectItem);
					break;
				}
				
			}  
		var jenkinsserverid= $("#testsubmition_jenkinsserverdropdownlist").jqxDropDownList('getSelectedItem').value;
		init_testsubmition_jenkinsjob(testsubmitionid,jenkinsserverid);         
		});
	}
	
   
     //TASK TYPE change event
   function change_jenkinsserver_handler(testsubmitionid)
   {
   	  $("#testsubmition_jenkinsserverdropdownlist").on("change",function(){
   	  	 var jenkinsserverid= $("#testsubmition_jenkinsserverdropdownlist").jqxDropDownList('getSelectedItem').value;
   	  	 init_testsubmition_jenkinsjob(testsubmitionid,jenkinsserverid);
   	  });
   	  
   	  
   }
   
    //初始化jenkins job
	function init_testsubmition_jenkinsjob(testsubmitionid,jenkinsserverid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TPSJENKINSJOB",jenkinsserverid:jenkinsserverid},function(data,status){
			var testsubmitionproject_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#testsubmition_jenkinsjobcombo").jqxComboBox({theme:theme,source: testsubmitionproject_source, width: 350, height: 25,displayMember:'text',valueMember: 'memberid', searchMode:'contains',autoComplete:true});
			for(var i in testsubmitionproject_source)
			{
				if(testsubmitionproject_source[i].selected==1)
				{
					var selectedItem=$("#testsubmition_jenkinsjobcombo").jqxComboBox('getItem',Number(i));
			        $("#testsubmition_jenkinsjobcombo").jqxComboBox('selectItem',selectedItem);
					break;
				}
				
			}
         });
	}
	
	function validate_testsubmition_jenkinsjob()
	{
		var result=false;
		var item = $("#testsubmition_jenkinsjobcombo").jqxComboBox('getSelectedIndex');
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
   
   
    //初始化jenkins cc list
	function init_testsubmition_cc(testsubmitionid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TPSCC"},function(data,status){
			var testsubmitionCC_source =eval("(" + data + ")");
			$("#testsubmition_cc_combo").jqxListBox({theme:theme,source: testsubmitionCC_source,multiple: true, width: 350, height: 200,displayMember:'text',valueMember: 'memberid'});
			for(var i in testsubmitionCC_source)
			{
				if(testsubmitionCC_source[i].selected==1)
				{
					$("#testsubmition_cc_combo").jqxListBox('selectIndex',i);
				}
				
			}
         });
	}
	
   
    //初始化jenkins server
	function init_testsubmition_buildparameters(testsubmitionid)
	{
		$.post("/functiontesting/testsubmition/init_testsubmition_formcontrol",{testsubmitionid:testsubmitionid,controlname:"TPSBUILDPARAMETER"},function(data,status){
			$("#testsubmition_buildparameterInput").jqxInput({theme:theme, placeHolder:"可选参数build parameter", width: 350, height: 25});
             if(data!="")
             {
        	  $("#testsubmition_buildparameterInput").jqxInput("val",data);
             }     
		});     
	}
	

   
              
   //发送创建任务请求
   function send_createtask_request()
   {
   	  var testsubmition_field=$('#testsubmition_create_form').serialize();
   	  $.post("/functiontesting/testsubmition/create",$('#testsubmition_create_form').serialize(),function(data,status){
          loadtestsubmitionpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_edittask_request(testsubmitionid)
   {
   	  var testsubmition_field=$('#testsubmition_create_form').serialize();
   	  $.post("/functiontesting/testsubmition/edit",$('#testsubmition_create_form').serialize()+"&testsubmitionid="+testsubmitionid,function(data,status){
          loadtestsubmitionpage();
   	  });
   	  
   }
   

 
     
  
	//点击添加自动化任务按钮
	
	function click_add_testsubmition()
	{
		$("#middleContainer").load("/functiontesting/testsubmition/create", function() {
			  create_testsubmition(0);
		});
	}
	
	//编辑自动化任务
	function edit_testsubmition(testsubmitionid)
	{
		$("#middleContainer").load("/functiontesting/testsubmition/edit", function() {
			  create_testsubmition(testsubmitionid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_testsubmition_toolbar()
	{
		$("#testsubmitiontoolbar").jqxToolBar("disableTool",0, true);
	    $("#testsubmitiontoolbar").jqxToolBar("disableTool",1, true);
		$("#testsubmitiontoolbar").jqxToolBar("disableTool",2, true);
		$("#testsubmitiontoolbar").jqxToolBar("disableTool",3, true);
	}
	
    
	loadpagenation(get_search_keyword());
	function loadpagenation(searchkeyword) 
	{
		$.post("/functiontesting/testsubmition/get_testsubmition_page_counts", {
			searchkeyword : searchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					searchkeyword = $('#testsubmitionsearchinput').val();
					if (searchkeyword == "") 
					{
						 searchkeyword = "ALL";
					}
					loadList("getlist", "testsubmition", page,searchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadtestsubmitionpage() {
		$("#middleContainer").load("/functiontesting/testsubmition/index", function() {
			$.getScript("/static/testjob/js/testsubmition_new.js");
			loadtestsubmitiontoolbar();
		});
	}
	
	//复制提测项目
	function copytestsubmition() {
		$("#header_copy").click(function() {
			var $chk = $("[name = selecttestsubmition:checkbox");
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
				testsubmitionid = $chk.filter(":checked").parent().find("span[class=testsubmitionidcontent]").text().trim();
				$.get("/functiontesting/testsubmition/copy_testsubmition", {
					id : testsubmitionid
				}, function(data, status) {
					$("#dialog-confirm").empty();
					$("#dialog-confirm").append(data);
					$("#dialog-confirm").dialog("open");
					searchkeyword = $('#testsubmitionsearchinput').val();
					if (searchkeyword == "") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "testsubmition", currnetpageindex, searchkeyword);
				});
			}
		});
	}
	
	//search submition
	function searchtestsubmition() {
		//点击搜索按钮
		$("#testsubmitionsearchbutton").click(function() 
		{
			search_testsubmition_bykeyword();
		});
		
		$('#testsubmitionsearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_testsubmition_bykeyword();
				}
			});
	}
	
	//search submition
	function search_testsubmition_bykeyword()
	{
		    searchkeyword = $('#testsubmitionsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}

			loadpagenation(searchkeyword);
			loadList("getlist", "testsubmition", 1, searchkeyword);
	}
	
	//获取当前搜索关键字
	function get_search_keyword()
	{
		searchkeyword = $('#testsubmitionsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}
		return searchkeyword;
	}
	
	//删除任务确认
	
	function delete_testsubmition() {
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
				"是" : function() 
				{
					$(this).dialog("close");
					$.post("/functiontesting/testsubmition/deletetestsubmition",{testsubmitionid:testsubmitionid},function(data,status){
				         loadList("getlist", "testsubmition",currnetpageindex,get_search_keyword());
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
	
	
	$("#dialog-confirm").dialog({
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
	
	//提测
	function submition() {
		$("button[name=submit2tester]").click(function(data, status) {
			submitionid = $(this).parent().parent().find("span[class=testsubmitionidcontent]").text().trim();
			$.get("/functiontesting/testsubmition/submitfortesting", {
				testsubmitionid : submitionid
			}, function(data, status) {
				$("#dialog-confirm").empty();
				$("#dialog-confirm").append(data);
				$("#dialog-confirm").dialog("open");
				loadList("getlist", "testsubmition", currnetpageindex,get_search_keyword());
			});
		});
	}

	//点击打包
	function clickpackage() {
		$("button[name=package]").click(function(data, status) {
			submitionid = $(this).parent().parent().find("span[class=testsubmitionidcontent]").text().trim();
			$.get("/functiontesting/testsubmition/package", {
				testsubmitionid : submitionid
			}, function(data, status) {
				$("#dialog-confirm").empty();
				$("#dialog-confirm").append(data);
				$("#dialog-confirm").dialog("open");
			});
		});
	}



});
