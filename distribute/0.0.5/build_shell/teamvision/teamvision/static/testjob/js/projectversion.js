$(document).ready(function() {

	var pvpageindex = 1;
	var pvsearchkeyword="ALL";
	var projectversionid=0;
	var theme='arctic';

	load_projectversion_List("getlist", "projectversion",pvpageindex,"ALL");
     
     
    load_projectversion_toolbar();
    
    searchprojectversion();

 
	//加载对象列表容器
	function load_projectversion_List(listmethod, objectType, pageindex, pvsearchkeyword) {
		//加载列表
		$("#projectversionlistcontainer").load("/functiontesting/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			pvsearchkeyword : pvsearchkeyword
		}, function(data, status) {
			show_projectversion_rowmenu();
			projectversion_row_menu_event_handle();              
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
			tools : "button | button | custom",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					case 0:
					     tool.jqxButton({width:80});
						tool.text("返回项目");
						tool.on("click",function(event){
							loadtestprojectpage();
						});
						break;
					   
					case 1:
						tool.jqxButton({width:80});
						tool.text("添加");
						tool.on("click",function(event){
							disable_projectversion_toolbar();
							click_add_projectversion();
						});
						break;
					case 2:
					    var projectversionsearchbox=$("<div id='projectversionsearchbox'><input id='projectversionsearchinput'  type='text'/><div id='projectversionsearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    tool.append(projectversionsearchbox);
					    projectversionsearchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						break;
				}
			}
		});
	}

	
	//auto task 创建
	
	
	function create_projectversion(projectversionid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#projectversion_nameInput', message: '提测ID是必填项!', action: 'keyup, blur', rule:'required' },
                       { input: '#projectversion_keyInput', message: '提测ID是必填项!', action: 'keyup, blur', rule:'required' },
                       //{ input: '#projectversion_lead_combo', message: 'Job名称是必填项', action: 'keyup, blur', rule: 'required' }
                       ];
                       
		    $("#projectversion_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#projectversion_create").css('visibility', 'visible');
            $('#projectversionsendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#projectversion_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#projectversion_create_backbutton").on('click',function(){
            	$('#projectversion_create_form').jqxValidator('hide');
            	loadprojectversionpage();
            }); 

              // init_projectversion_name(projectversionid);
              // init_projectversion_key(projectversionid);
              // init_projectversion_lead(projectversionid);
              // init_projectversion_startdate(projectversionid);
              // init_projectversion_enddate(projectversionid);
              // init_projectversion_progress(projectversionid);
              // init_projectversion_tester(projectversionid);
              // // init_projectversion_status(projectversionid);
              // init_projectversion_comments(projectversionid);
              // init_projectversion_bugcounts(projectversionid);
              // loadjobname();
              
             // change_jenkinsserver_handler(projectversionid);
            
            // $("#projectversion_advance_button").jqxButton({theme:theme, width: '80'});
            // $("#projectversion_advance_button").on('click',function(){
                 // $("tr[class=projectversion_advance]").toggle();
            // });
            
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
	function init_projectversion_name(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTPROJECTNAME"},function(data,status)
		{
			$("#projectversion_nameInput").jqxInput({theme:theme, placeHolder:"请输入版本号！", width: 350, height: 25});
			if(data!="")
          {
        	 $("#projectversion_nameInput").jqxInput("val",data);
          }       		
		});
	}


	function init_projectversion_key(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTPROJECTKEY"},function(data,status)
		{
			$("#projectversion_keyInput").jqxInput({theme:theme, placeHolder:"请输入版本号！", width: 350, height: 25});
			if(data!="")
          {
        	 $("#projectversion_keyInput").jqxInput("val",data);
          }       		
		});
	}
	
	function validate_projectversion_name()
	{
		var projectversionname=$("#projectversion_nameInput").jqxInput("val");
		var result=false;
		if(projectversionid!=0)
		{
			result=true;
		}
		else
		{
		  $.ajax({  
                async:false,
                type: "POST",  
                url: "/functiontesting/projectversion/check_name_exits",  
                data: "projectversionname="+projectversionname,  
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
	
	function init_projectversion_lead(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTPROJECTLEAD"},function(data,status){
			var projectversion_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#projectversion_lead_combo").jqxComboBox({theme:theme,source: projectversion_source, multiSelect: false, width: 350, height: 25,displayMember:'text',valueMember: 'memberid', searchMode:'contains',autoComplete:true});
			for(var i in projectversion_source)
			{
				if(projectversion_source[i].selected==1)
				{
					var selectedItem=$("#projectversion_lead_combo").jqxComboBox('getItem',Number(i));
			        $("#projectversion_lead_combo").jqxComboBox('selectItem',selectedItem);
					break;
				}
				
			}
         });
	}
	
	
	
	//projectversion_config validate function
	
	function validate_projectversion_commitid()
	{
		var result=false;
		var item = $("#projectversion_commitidInput").jqxComboBox('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
	}
	
	//初始化测试配置控件
	
	function init_projectversion_jobname(projectversionid)
	{
       $.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTJOBNAME"},function(data,status)
		{
			$("#projectversion_jobnameInput").jqxInput({theme:theme, placeHolder:"Job名称", width: 350, height: 25});
			if(data!="")
             {
        	  $("#projectversion_jobnameInput").jqxInput("val",data);
             }       		
		});                     
	}
	
	
	//projectversion_testcase validate function
	
	function validate_projectversion_jobname()
	{
		var result=false;
		var item = $("#projectversion_productnamecombo").jqxComboBox('getSelectedIndex');
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
   }
   
   //初始化测试任务类型控件
	
	function init_projectversion_startdate(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTJOBSTARTDATE"},function(data,status)
		{
			$("#projectversion_startdate").jqxDateTimeInput({width: '350px', height: '25px',formatString: "yyyy-MM-dd"});
			if(data!="")
          {
        	 $("#projectversion_startdate").jqxInput("val",data);
          }       		
		});
	}
	
	
	//projectversion_type validate function
	
	function validate_projectversion_startdate()
	{
        var productversion=$("#projectversion_versionInput").jqxInput("val");
		var result=false;
		if(projectversionid!=0)
		{
			result=true;
		}
		else
		{
		  $.ajax({  
                async:false,
                type: "POST",  
                url: "/functiontesting/projectversion/check_version_exits",  
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
  function init_projectversion_enddate(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTJOBENDDATE"},function(data,status)
		{
			$("#projectversion_enddate").jqxDateTimeInput({width: '350px', height: '25px',formatString: "yyyy-MM-dd"});
			if(data!="")
             {
        	  $("#projectversion_enddate").jqxInput("val",data);
             }       		
		});           
	}

 //初始化 bug 修复信息
  function init_projectversion_progress(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTJOBPROGRESS"},function(data,status){
			$("#projectversion_processInput").jqxInput({theme:theme, placeHolder:"请填写bug修复信息", width: 350, height: 25});
             if(data!="")
             {
        	  $("#projectversion_processInput").jqxInput("val",data);
             }     
		});           
	}
	
	
	//初始化 bug 修复信息
  function init_projectversion_tester(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTJOBTESTER"},function(data,status){
			var projectversion_tester_source =eval("(" + data + ")");
			$("#projectversion_tester_listbox").jqxListBox({theme:theme,source: projectversion_tester_source,multiple: true, width: 350, height: 150,displayMember:'text',valueMember: 'memberid'});
			for(var i in projectversion_tester_source)
			{
				if(projectversion_tester_source[i].selected==1)
				{
					$("#projectversion_tester_listbox").jqxListBox('selectIndex',i);
				}
				
			}
         });
	}

  function validate_projectversion_tester()
  {
  	    var result=false;
		var item = $("#projectversion_tester_listbox").jqxListBox('getSelectedItems');
		 //空检查
		 if(item.length!=0)
		 {
		   result=true;
		 }
          return result;
  }
	
	function init_projectversion_comments(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTJOBCOMMENT"},function(data,status){
			$("#projectversion_commentsInput").jqxInput({theme:theme, placeHolder:"请填写测试建议", width: 350, height: 150});
             if(data!="")
             {
        	  $("#projectversion_commentsInput").jqxInput("val",data);
             }     
		});           
	}
	
	
   
    //初始化jenkins server
	function init_projectversion_bugcounts(projectversionid)
	{
		$.post("/functiontesting/projectversion/init_projectversion_formcontrol",{projectversionid:projectversionid,controlname:"TESTJOBBUGCOUNTS"},function(data,status){
			$("#projectversion_bugcountsInput").jqxInput({theme:theme, placeHolder:"请输入bug数", width: 350, height: 25});
             if(data!="")
             {
        	  $("#projectversion_bugcountsInput").jqxInput("val",data);
             }     
		});     
	}
	

   
              
   //发送创建任务请求
   function send_createprojectversion_request()
   {
   	  var projectversion_field=$('#projectversion_create_form').serialize();
   	  $.post("/functiontesting/projectversion/create",$('#projectversion_create_form').serialize(),function(data,status){
          loadprojectversionpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_projectversion_request(projectversionid)
   {
   	  var projectversion_field=$('#projectversion_create_form').serialize();
   	  $.post("/functiontesting/projectversion/edit",$('#projectversion_create_form').serialize()+"&projectversionid="+projectversionid,function(data,status){
          loadprojectversionpage();
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
	
    
	load_projectversion_pagenation(get_projectversion_searchkeyword());
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
	function loadprojectversionpage() {
		$("#middleContainer").load("/functiontesting/projectversion/index", function() {
			$.getScript("/static/testjob/js/projectversion.js");
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
				}, function(data, status) {
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
