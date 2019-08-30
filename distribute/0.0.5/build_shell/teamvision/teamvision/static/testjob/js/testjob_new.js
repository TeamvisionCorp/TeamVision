$(document).ready(function() {

	var currnetpageindex = 1;
	var searchkeyword="ALL";
	var testjobid=0;
	var theme='arctic';

	loadList("getlist", "testjob",currnetpageindex,"ALL");
     
    loadtestjobtoolbar();
    
    searchtestjob();

 
	//加载对象列表容器
	function loadList(listmethod, objectType, pageindex, searchkeyword) {
		//加载列表
		$("#testjoblistcontainer").load("/functiontesting/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			searchkeyword : searchkeyword
		}, function(data, status) {
			showrowmenu();
			row_menu_event_handle();
			// //加载测试进度
			loadprogress();
			clickrowedit();
			// //点击行编辑按钮弹出编辑窗口
			// clickrowedit();testjobrowoperation
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
		var contextMenu = $("#testjobrowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=testjobrowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=testjobidcontent]");
                	    testjobid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=testjobrowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function row_menu_event_handle()
	{
		$("li[name=testjobrowoperationedit]").click(function(){
			disable_testjob_toolbar();
			edit_testjob(testjobid);
		});
		$("li[name=testjobrowoperationdelete]").click(function(){
			
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" +testjobid + "的提测项目吗？");
			$("#dialog-confirmdelete").dialog("open");
		});
		$("li[name=testjobrowoperationdetail]").click(function(){
		});
		
		$("li[name=testjobrowoperationcopy]").click(function(){
			$.post("/functiontesting/testjob/copytestjob",{testjobid:testjobid},function(data,status){
				loadList("getlist", "testjob",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
		});
	}


	//点击checkbox

	function clickcheckbox() {
		$("[name = selecttestjob]:checkbox").bind("click", function() {
			var $chk = $("[name = selecttestjob]:checkbox");
			// $("#testjobselectall").attr("checked", $chk.length == $chk.filter(":checked").length);
		});
		// $("#testjobselectall").bind("click", function() {
			// var $chk = $("[name = selecttestjob]:checkbox");
			// if ($chk.filter(":checked").length == $chk.length) {
				// $("[name = selecttestjob]:checkbox").attr("checked", false);
			// } else {
				// $("[name = selecttestjob]:checkbox").attr("checked", true);
			// }
		// });
	}

	//双击测试计划行
	function clickrowedit() {
		$("button[name=testjobrowedit]").click(function() {
			testjobid = $(this).parent().parent().find("span[class=testjobidcontent]").text().trim();
			disable_testjob_toolbar();
			edit_testjob(testjobid);

		});
	}
	
	
	//加载自动化任务工具栏
	function loadtestjobtoolbar() {
		$("#testjobtoolbar").jqxToolBar({theme:theme,
			tools : "button | custom",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					case 0:
						tool.jqxButton({width:80});
						tool.text("添加");
						tool.on("click",function(event){
							disable_testjob_toolbar();
							click_add_testjob();
						});
						break;
					case 1:
					    var searchbox=$("<div id='testjobsearchbox'><input id='testjobsearchinput'  type='text'/><div id='testjobsearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    tool.append(searchbox);
					    // var source ={
                            // datatype: "json",
                            // datafields:[{name:'testjobname'}],
                            // url: '/functiontesting/testjob/get_taskname_list'
                            // };
                        // var dataAdapter = new $.jqx.dataAdapter(source);
					    searchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						break;
				}
			}
		});
	}
	
	//auto task 创建
	
	
	
	function create_testjob(testjobid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#testjob_commitidInput', message: '提测ID是必填项!', action: 'keyup, blur', rule:'required' },
                       { input: '#testjob_bugcountsInput', message: '提测ID是必填项!', action: 'keyup, blur', rule:'required' },
                       { input: '#testjob_jobnameInput', message: 'Job名称是必填项', action: 'keyup, blur', rule: 'required' },
                       { input: '#testjob_tester_listbox', message: '测试人员是必填项!', action: 'keyup, blur', rule: validate_testjob_tester },
                       { input: '#testjob_processInput', message: '进度是必填项', action: 'keyup, blur', rule:'required' }
                       ];
                       
		    $("#testjob_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#testjob_create").css('visibility', 'visible');
            $('#testjobsendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#testjob_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#testjob_create_backbutton").on('click',function(){
            	$('#testjob_create_form').jqxValidator('hide');
            	loadtestjobpage();
            }); 

              init_testjob_jobtype(testjobid);
              init_testjob_commitid(testjobid);
              init_testjob_jobname(testjobid);
              init_testjob_startdate(testjobid);
              init_testjob_enddate(testjobid);
              init_testjob_progress(testjobid);
              init_testjob_tester(testjobid);
              // init_testjob_status(testjobid);
              init_testjob_comments(testjobid);
              init_testjob_bugcounts(testjobid);
              loadjobname();
              
             // change_jenkinsserver_handler(testjobid);
            
            // $("#testjob_advance_button").jqxButton({theme:theme, width: '80'});
            // $("#testjob_advance_button").on('click',function(){
                 // $("tr[class=testjob_advance]").toggle();
            // });
            
           $('#testjobsendButton').on('click', function () {
                $('#testjob_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#testjob_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(testjobid==0)
            	 {
            	 	send_createtask_request();
            	 }
            	 else
            	 {
            	 	send_edittask_request(testjobid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_testjob_jobtype(testjobid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBTYPE"},function(data,status){
			var testjobplatform_source =eval("(" + data + ")");
			$("#testjob_jobtype_dropdownlist").jqxDropDownList({theme:theme,source: testjobplatform_source,selectedIndex:0, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in testjobplatform_source)
			{
				if(testjobplatform_source[i].selected==1)
				{
					$("#testjob_jobtype_dropdownlist").jqxDropDownList('selectIndex',i);
					// selectedIndex=i;
					
					break;
				}
				
			} 
		
		});
	}


	function init_testjob_status(testjobid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBSTATUS"},function(data,status){
			var testjobstatus_source =eval("(" + data + ")");
			$("#testjob_status_dropdownlist").jqxDropDownList({theme:theme,source: testjobstatus_source,selectedIndex:0, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in testjobstatus_source)
			{
				if(testjobstatus_source[i].selected==1)
				{
					$("#testjob_status_dropdownlist").jqxDropDownList('selectIndex',i);
					// var selectItem=$("#testjob_status_dropdownlist").jqxDropDownList('getItem',Number(i));
					// $("#testjob_status_dropdownlist").jqxDropDownList('selectItem',selectItem);
					// selectedIndex=i;
					
					break;
				}
				
			} 
		
		});
	}
	
	function validate_testjob_name()
	{
		var testjobname=$("#testjob_nameInput").jqxInput("val");
		var result=false;
		if(testjobid!=0)
		{
			result=true;
		}
		else
		{
		  $.ajax({  
                async:false,
                type: "POST",  
                url: "/functiontesting/testjob/check_name_exits",  
                data: "testjobname="+testjobname,  
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
	
	function init_testjob_commitid(testjobid,projectid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBCOMMITID"},function(data,status)
		{
			$("#testjob_commitidInput").jqxInput({theme:theme, placeHolder:"请输入版本号！", width: 350, height: 25});
			if(data!="")
          {
        	 $("#testjob_commitidInput").jqxInput("val",data);
          }       		
		});
	}
	
	
	
	//testjob_config validate function
	
	function validate_testjob_commitid()
	{
		var result=false;
		var item = $("#testjob_commitidInput").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
	}
	
	function loadjobname() {
		$("#testjob_commitidInput").blur(function() {
			
			$.get("/functiontesting/testjob/getjobname", {
				'submitionid' : $(this).val()
			}, function(data, status) {
				$("#testjob_jobnameInput").jqxInput("val",data);
			});
		});
	}
	//初始化测试配置控件
	
	function init_testjob_jobname(testjobid)
	{
       $.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBNAME"},function(data,status)
		{
			$("#testjob_jobnameInput").jqxInput({theme:theme, placeHolder:"Job名称", width: 350, height: 25});
			if(data!="")
             {
        	  $("#testjob_jobnameInput").jqxInput("val",data);
             }       		
		});                     
	}
	
	
	//testjob_testcase validate function
	
	function validate_testjob_jobname()
	{
		var result=false;
		var item = $("#testjob_productnamecombo").jqxComboBox('getSelectedIndex');
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
   
   //初始化测试任务类型控件
	
	function init_testjob_startdate(testjobid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBSTARTDATE"},function(data,status)
		{
			$("#testjob_startdate").jqxDateTimeInput({width: '350px', height: '25px',formatString: "yyyy-MM-dd"});
			if(data!="")
          {
        	 $("#testjob_startdate").jqxDateTimeInput("val",data);
          }       		
		});
	}
	
	
	//testjob_type validate function
	
	function validate_testjob_startdate()
	{
        var productversion=$("#testjob_versionInput").jqxInput("val");
		var result=false;
		if(testjobid!=0)
		{
			result=true;
		}
		else
		{
		  $.ajax({  
                async:false,
                type: "POST",  
                url: "/functiontesting/testjob/check_version_exits",  
                data: "productversion="+productversion,  
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

   
  // 初始化新增功能
  function init_testjob_enddate(testjobid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBENDDATE"},function(data,status)
		{
			$("#testjob_enddate").jqxDateTimeInput({width: '350px', height: '25px',formatString: "yyyy-MM-dd"});
			if(data!="")
             {
        	  $("#testjob_enddate").jqxDateTimeInput("val",data);
             }       		
		});           
	}

 //初始化 bug 修复信息
  function init_testjob_progress(testjobid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBPROGRESS"},function(data,status){
			$("#testjob_processInput").jqxInput({theme:theme, placeHolder:"请填写bug修复信息", width: 350, height: 25});
             if(data!="")
             {
        	  $("#testjob_processInput").jqxInput("val",data);
             }     
		});           
	}
	
	
	//初始化 bug 修复信息
  function init_testjob_tester(testjobid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBTESTER"},function(data,status){
			var testjob_tester_source =eval("(" + data + ")");
			$("#testjob_tester_listbox").jqxListBox({theme:theme,source: testjob_tester_source,multiple: true, width: 350, height: 150,displayMember:'text',valueMember: 'memberid'});
			for(var i in testjob_tester_source)
			{
				if(testjob_tester_source[i].selected==1)
				{
					$("#testjob_tester_listbox").jqxListBox('selectIndex',i);
				}
				
			}
         });
	}

  function validate_testjob_tester()
  {
  	    var result=false;
		var item = $("#testjob_tester_listbox").jqxListBox('getSelectedItems');
		 //空检查
		 if(item.length!=0)
		 {
		   result=true;
		 }
          return result;
  }
	
	function init_testjob_comments(testjobid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBCOMMENT"},function(data,status){
			$("#testjob_commentsInput").jqxInput({theme:theme, placeHolder:"请填写测试建议", width: 350, height: 150});
             if(data!="")
             {
        	  $("#testjob_commentsInput").jqxInput("val",data);
             }     
		});           
	}
	
	
   
    //初始化jenkins server
	function init_testjob_bugcounts(testjobid)
	{
		$.post("/functiontesting/testjob/init_testjob_formcontrol",{testjobid:testjobid,controlname:"TESTJOBBUGCOUNTS"},function(data,status){
			$("#testjob_bugcountsInput").jqxInput({theme:theme, placeHolder:"请输入bug数", width: 350, height: 25});
             if(data!="")
             {
        	  $("#testjob_bugcountsInput").jqxInput("val",data);
             }     
		});     
	}
	

   
              
   //发送创建任务请求
   function send_createtask_request()
   {
   	  var testjob_field=$('#testjob_create_form').serialize();
   	  $.post("/functiontesting/testjob/create",$('#testjob_create_form').serialize(),function(data,status){
          loadtestjobpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_edittask_request(testjobid)
   {
   	  var testjob_field=$('#testjob_create_form').serialize();
   	  $.post("/functiontesting/testjob/edit",$('#testjob_create_form').serialize()+"&testjobid="+testjobid,function(data,status){
          loadtestjobpage();
   	  });
   	  
   }
   

 
     
  
	//点击添加自动化任务按钮
	
	function click_add_testjob()
	{
		$("#middleContainer").load("/functiontesting/testjob/create", function() {
			  create_testjob(0);
		});
	}
	
	//编辑自动化任务
	function edit_testjob(testjobid)
	{
		$("#middleContainer").load("/functiontesting/testjob/edit", function() {
			  create_testjob(testjobid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_testjob_toolbar()
	{
		$("#testjobtoolbar").jqxToolBar("disableTool",0, true);
	    $("#testjobtoolbar").jqxToolBar("disableTool",1, true);
		$("#testjobtoolbar").jqxToolBar("disableTool",2, true);
		$("#testjobtoolbar").jqxToolBar("disableTool",3, true);
	}
	
    
	loadpagenation(get_search_keyword());
	function loadpagenation(searchkeyword) 
	{
		$.post("/functiontesting/testjob/get_testjob_page_counts", {
			searchkeyword : searchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					searchkeyword = $('#testjobsearchinput').val();
					if (searchkeyword == "") 
					{
						 searchkeyword = "ALL";
					}
					loadList("getlist", "testjob", page,searchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadtestjobpage() {
		$("#middleContainer").load("/functiontesting/testjob/index", function() {
			$.getScript("/static/testjob/js/testjob_new.js");
			loadtestjobtoolbar();
		});
	}
	
	//复制提测项目
	function copytestjob() {
		$("#header_copy").click(function() {
			var $chk = $("[name = selecttestjob:checkbox");
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
				testjobid = $chk.filter(":checked").parent().find("span[class=testjobidcontent]").text().trim();
				$.get("/functiontesting/testjob/copy_testjob", {
					id : testjobid
				}, function(data, status) {
					$("#dialog-confirm").empty();
					$("#dialog-confirm").append(data);
					$("#dialog-confirm").dialog("open");
					searchkeyword = $('#testjobsearchinput').val();
					if (searchkeyword == "") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "testjob", currnetpageindex, searchkeyword);
				});
			}
		});
	}
	
	//search job
	function searchtestjob() {
		//点击搜索按钮
		$("#testjobsearchbutton").click(function() 
		{
			search_testjob_bykeyword();
		});
		
		$('#testjobsearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_testjob_bykeyword();
				}
			});
	}
	
	//search job
	function search_testjob_bykeyword()
	{
		    searchkeyword = $('#testjobsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}

			loadpagenation(searchkeyword);
			loadList("getlist", "testjob", 1, searchkeyword);
	}
	
	//获取当前搜索关键字
	function get_search_keyword()
	{
		searchkeyword = $('#testjobsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}
		return searchkeyword;
	}
	
	//删除任务确认
	
	function delete_testjob() {
		$("button[name=rowdelete]").click(function(data, status) {
			currentjobid = $(this).parent().parent().find("span[class=testjobidcontent]").text().trim();
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" + currentjobid + "的提测项吗？");
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
					$.post("/functiontesting/testjob/deletetestjob",{testjobid:testjobid},function(data,status){
				         loadList("getlist", "testjob",currnetpageindex,get_search_keyword());
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
	
	//展示进度
	
	function loadprogress() {
		$("div[name=testjobprogress]").each(function(index, element) {
			var jobid = $(element).parent().parent().find("span[class=testjobidcontent]").text().trim();
			$.get("/functiontesting/testjob/getjobprogress", {
				jobid : jobid
			}, function(data, status) {
				var result = data.split(",");
				var progressvalue = result[0];
				var color = result[1];
				$(element).progressbar({
					value : progressvalue
				});
				$(element).attr("title", progressvalue + '%');
				progressbarValue = $(element).find(".ui-progressbar-value");
				progressbarValue.css({
					"background" : color,
					"display" : 'block',
					"width" : progressvalue + '%'
				});
			});
		});
	}
	
	
	



});
