$(document).ready(function() {

	var currnetpageindex = 1;
	var searchkeyword="ALL";
	var autoagentid=0;
	var theme='arctic';

	loadList("getlist", "autoagent",currnetpageindex,"ALL");
     
    loadautoagenttoolbar();
    
    searchautoagent();

 
	//加载对象列表容器
	function loadList(listmethod, objectType, pageindex, searchkeyword) {
		//加载列表
		$("#autoagentlistcontainer").load("/autotesting/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			searchkeyword : searchkeyword
		}, function(data, status) {
			// showrowmenu();
			// row_menu_event_handle();
			// //加载测试进度
			// loadprogress();
			// //点击行编辑按钮弹出编辑窗口
			clickrowedit();
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
		var contextMenu = $("#autoagentrowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=autoagentrowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=autoagentidcontent]");
                	    autoagentid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=autoagentrowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function row_menu_event_handle()
	{
		$("li[name=autoagentrowoperationedit]").click(function(){
			disable_autoagent_toolbar();
			edit_autoagent(autoagentid);
		});
		$("li[name=autoagentrowoperationdelete]").click(function(){
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" +autoagentid + "的自动化任务吗？");
			$("#dialog-confirmdelete").dialog("open");
		});
		$("li[name=autoagentrowoperationdetail]").click(function(){
		});
		$("li[name=autoagentrowoperationreport]").click(function(){
			
		});
		$("li[name=autoagentrowoperationcopy]").click(function(){
			$.post("/autotesting/autoagent/copyautoagent",{autoagentid:autoagentid},function(data,status){
				loadList("getlist", "autoagent",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
		});
	}


	//点击checkbox

	function clickcheckbox() {
		$("[name = selectautoagent]:checkbox").bind("click", function() {
			var $chk = $("[name = selectautoagent]:checkbox");
			// $("#autoagentselectall").attr("checked", $chk.length == $chk.filter(":checked").length);
		});
		// $("#autoagentselectall").bind("click", function() {
			// var $chk = $("[name = selectautoagent]:checkbox");
			// if ($chk.filter(":checked").length == $chk.length) {
				// $("[name = selectautoagent]:checkbox").attr("checked", false);
			// } else {
				// $("[name = selectautoagent]:checkbox").attr("checked", true);
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
		$("button[name=autoagentrowedit]").click(function() {
			var element=$(this).parent().parent().find("span[class=autoagentidcontent]");
            autoagentid=element.text();
			disable_autoagent_toolbar();
			edit_autoagent(autoagentid);
		});
	}


	

	//鼠标滑过数据行
	function mouseroverdatarow() {
		$("li[class=autoagentdatarow]").mouseover(function() {
			$(this).addClass("mouseroverdatarow");
		});
		$("li[class=autoagentdatarow]").mouseout(function() {
			$(this).removeClass("mouseroverdatarow");
		});
	}
	
	
	
	//加载自动化任务工具栏
	function loadautoagenttoolbar() {
		$("#autoagenttoolbar").jqxToolBar({theme:theme,
			tools : "button | custom",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					case 0:
						tool.jqxButton({width:80});
						tool.text("添加");
						tool.on("click",function(event){
							disable_autoagent_toolbar();
							click_add_autoagent();
						});
						break;
					case 1:
					    var searchbox=$("<div id='autoagentsearchbox'><input id='autoagentsearchinput'  type='text'/><div id='autoagentsearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    tool.append(searchbox);
					    // var source ={
                            // datatype: "json",
                            // datafields:[{name:'autoagentname'}],
                            // url: '/autotesting/autoagent/get_taskname_list'
                            // };
                        // var dataAdapter = new $.jqx.dataAdapter(source);
					    searchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						break;
				}
			}
		});
	}
	
	//auto task 创建
	
	
	
	function create_autoagent(autoagentid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#autoagent_nameInput', message: '机器名称 是必填项!', action: 'keyup, blur', rule: 'required' },
                       { input: '#autoagent_nameInput', message: '结点名称已经存在。', action: 'keyup,blur', rule: validate_autoagent_name },
                       { input: '#autoagent_IPInput', message: 'IP地址是必须项', action: 'keyup, blur', rule: 'required' },
                       { input: '#autoagent_IPInput', message: '该IP地址表示的机器已经存在！', action: 'keblur', rule: validate_autoagent_ip },
                       { input: '#autoagent_WorkSpaceInput', message: '工作目录是必须的！', action: 'keyup, blur', rule: 'required' },
                       { input: '#autoagent_WorkSpaceInput', message: '工作目录长度不能超过255个字符、！', action: 'keyup, blur', rule: 'length=1,255' },
                       { input: '#autoagent_browsers_listbox', message: '浏览器是必选项!', action: 'keyup, blur,change', rule: validate_autoagent_browser}
                       ];
                       
		    $("#autoagent_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#autoagent_create").css('visibility', 'visible');
            $('#sendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#autoagent_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#autoagent_create_backbutton").on('click',function(){
            	$('#autoagent_create_form').jqxValidator('hide');
            	loadautoagentpage();
            }); 

              init_autoagent_name(autoagentid);
              init_autoagent_os(autoagentid);
              init_autoagent_browser(autoagentid);
              init_autoagent_ip(autoagentid);
              init_autoagent_isreserved(autoagentid);
              init_autoagent_workspace(autoagentid);
            
            // $("#autoagent_advance_button").jqxButton({theme:theme, width: '80'});
            // $("#autoagent_advance_button").on('click',function(){
                 // $("tr[class=autoagent_advance]").toggle();
            // });
              // change_tasktype_handler();
            
            $('#sendButton').on('click', function () 
            {
                $('#autoagent_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#autoagent_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(autoagentid==0)
            	 {
            	 	send_createautoagent_request();
            	 }
            	 else
            	 {
            	 	send_editautoagent_request(autoagentid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_autoagent_name(autoagentid)
	{
		$.post("/autotesting/autoagent/init_autoagent_formcontrol",{autoagentid:autoagentid,controlname:"AUTOAGENTNAME"},function(data,status){
			 $("#autoagent_nameInput").jqxInput({theme:theme,placeHolder:"请输入任务名称!", width: 350, height: 25});
            if(data!="")
          {
        	$("#autoagent_nameInput").jqxInput("val",data);
          }       			
		});
	}
	
	function validate_autoagent_name()
	{
		var agent_name=$("#autoagent_nameInput").jqxInput("val");
		var result=false;
		if(autoagentid!=0)
		{
			result=true;
		}
		else
		{
			$.ajax({  
                async:false,
                type: "POST",  
                url: "/autotesting/autoagent/check_name_exits",  
                data: "agentname="+agent_name,  
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
	function init_autoagent_os(autoagentid)
	{
		$.post("/autotesting/autoagent/init_autoagent_formcontrol",{autoagentid:autoagentid,controlname:"AUTOAGENTOS"},function(data,status){
			var autoagent_OS =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autoagent_OS_dropdownlist").jqxDropDownList({theme:theme,selectedIndex:selectedIndex,source: autoagent_OS, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});
			for(var i in autoagent_OS)
			{
				if(autoagent_OS[i].selected==1)
				{
					var selectItem=$("#autoagent_OS_dropdownlist").jqxDropDownList('getItem',Number(i));
					$("#autoagent_OS_dropdownlist").jqxDropDownList('selectItem',selectItem);
					break;
				}
				
			}           
		});
	}
	
	//初始化测试配置os
	
	function init_autoagent_ip(autoagentid)
	{
		$.post("/autotesting/autoagent/init_autoagent_formcontrol",{autoagentid:autoagentid,controlname:"AUTOAGENTIP"},function(data,status){
			 $("#autoagent_IPInput").jqxInput({theme:theme,placeHolder:"请输入IP地址!", width: 350, height: 25});
            if(data!="")
             {
        	   $("#autoagent_IPInput").jqxInput("val",data);
             }       			
			});		
	}
	
	
	//autoagent_config validate function
	
	function validate_autoagent_ip()
	{
		var agent_ip=$("#autoagent_IPInput").jqxInput("val");
		var result=false;
		if(autoagentid!=0)
		{
			result=true;
		}
		else
		{
			$.ajax({  
                async:false,
                type: "POST",  
                url: "/autotesting/autoagent/check_ip_exits",  
                data: "agentip="+agent_ip,  
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
	
	//初始化工作目录
	function init_autoagent_workspace(autoagentid)
	{
		$.post("/autotesting/autoagent/init_autoagent_formcontrol",{autoagentid:autoagentid,controlname:"AUTOAGENTWORKSPACE"},function(data,status){
			 $("#autoagent_WorkSpaceInput").jqxInput({theme:theme,placeHolder:"请输入结点工作目录!", width: 350, height: 25});
            if(data!="")
             {
        	   $("#autoagent_WorkSpaceInput").jqxInput("val",data);
             }       			
			});		
	}
	
	
	//初始化测试配置os
	
	function init_autoagent_browser(autoagentid)
	{
		$.post("/autotesting/autoagent/init_autoagent_formcontrol",{autoagentid:autoagentid,controlname:"AUTOAGENTBROWSER"},function(data,status){
			var autoagenttype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autoagent_browsers_listbox").jqxListBox({theme:theme,multiple: true,source: autoagenttype_source, width: 350, height: 200,displayMember:'text',valueMember:'memberid'});
			for(var i in autoagenttype_source)
			{
				if(autoagenttype_source[i].selected==1)
				{
					$("#autoagent_browsers_listbox").jqxListBox('selectIndex', i);
				}
				
			}
			// var countries =[{text:"All",value:0},{text:"A",value:1},{text:"B",value:2},{text:"C",value:3},{text:"D",value:4}];
        // $("#autoagent_browsers_listbox").jqxListBox({theme:theme,selectedIndex:selectedIndex,multiple: true,source: autoagenttype_source, width: 350, height: 200,displayMember:'text',valueMember:'memberid'});      
			});		     
	}
	
	
	//autoagent_config validate function
	
	function validate_autoagent_browser()
	{
		var result=false;
		var item = $("#autoagent_browsers_listbox").jqxListBox('getSelectedItems');
		 //空检查
		 if(item.length!=0)
		 {
		   result=true;
		 }
          return result;
	 }
	//初始化测试配置控件
	
	function init_autoagent_isreserved(autoagentid)
	{
		$.post("/autotesting/autoagent/init_autoagent_formcontrol",{autoagentid:autoagentid,controlname:"AUTOAGENTRESERVED"},function(data,status){
			var selectedIndex=0;
			if(data=="True")
			{
				selectedIndex=1;
			}
			var countries =[{text:"否",value:0},{text:"是",value:1}];
			$("#autoagent_reserved_dropdownlist").jqxDropDownList({theme:theme,selectedIndex:selectedIndex,source: countries, width: 350, height: 25,displayMember:'text',valueMember:'value'});
		});           
	}
	
	
	
   //发送创建任务请求
   function send_createautoagent_request()
   {
   	  var autoagent_field=$('#autoagent_create_form').serialize();
   	  $.post("/autotesting/autoagent/create",$('#autoagent_create_form').serialize(),function(data,status){
          loadautoagentpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_editautoagent_request(autoagentid)
   {
   	  var autoagent_field=$('#autoagent_create_form').serialize();
   	  $.post("/autotesting/autoagent/edit",$('#autoagent_create_form').serialize()+"&autoagentid="+autoagentid,function(data,status){
          loadautoagentpage();
   	  });
   	  
   }
   

 
     
    
	
	
	//点击添加自动化任务按钮
	
	function click_add_autoagent()
	{
		$("#middleContainer").load("/autotesting/autoagent/create", function() {
			  create_autoagent(0);
		});
	}
	
	//编辑自动化任务
	function edit_autoagent(autoagentid)
	{
		$("#middleContainer").load("/autotesting/autoagent/edit", function() {
			  create_autoagent(autoagentid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_autoagent_toolbar()
	{
		$("#autoagenttoolbar").jqxToolBar("disableTool",0, true);
	    $("#autoagenttoolbar").jqxToolBar("disableTool",1, true);
		$("#autoagenttoolbar").jqxToolBar("disableTool",2, true);
		$("#autoagenttoolbar").jqxToolBar("disableTool",3, true);
	}
	
    
	loadpagenation(get_search_keyword());
	function loadpagenation(searchkeyword) 
	{
		$.post("/autotesting/autoagent/get_autoagent_page_counts", {
			searchkeyword : searchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					searchkeyword = $('#autoagentsearchinput').val();
					if (searchkeyword == "") 
					{
						 searchkeyword = "ALL";
					}
					loadList("getlist", "autoagent", page,searchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadautoagentpage() {
		$("#middleContainer").load("/autotesting/autoagent/index", function() {
			$.getScript("/static/autotesting/js/autoagent.js");
			loadautoagenttoolbar();
		});
	}
	
	//复制提测项目
	function copyautoagent() {
		$("#header_copy").click(function() {
			var $chk = $("[name = selectautoagent:checkbox");
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
				autoagentid = $chk.filter(":checked").parent().find("span[class=autoagentidcontent]").text().trim();
				$.get("/autotesting/autoagent/copy_autoagent", {
					id : autoagentid
				}, function(data, status) {
					$("#dialog-confirm").empty();
					$("#dialog-confirm").append(data);
					$("#dialog-confirm").dialog("open");
					searchkeyword = $('#autoagentsearchinput').val();
					if (searchkeyword == "") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "autoagent", currnetpageindex, searchkeyword);
				});
			}
		});
	}
	
	//search submition
	function searchautoagent() {
		//点击搜索按钮
		$("#autoagentsearchbutton").click(function() 
		{
			search_autoagent_bykeyword();
		});
		
		$('#autoagentsearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_autoagent_bykeyword();
				}
			});
	}
	
	//search submition
	function search_autoagent_bykeyword()
	{
		    searchkeyword = $('#autoagentsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}

			loadpagenation(searchkeyword);
			loadList("getlist", "autoagent", 1, searchkeyword);
	}
	
	//获取当前搜索关键字
	function get_search_keyword()
	{
		searchkeyword = $('#autoagentsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}
		return searchkeyword;
	}
	
	//删除任务确认
	
	function delete_autoagent() {
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
					$.post("/autotesting/autoagent/deleteautoagent",{autoagentid:autoagentid},function(data,status){
				loadList("getlist", "autoagent",currnetpageindex,get_search_keyword());
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
