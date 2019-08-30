$(document).ready(function() {

	var currnetpageindex = 1;
	var searchkeyword="ALL";
	var autorunresultid=0;
	var theme='arctic';

	loadList("getlist", "autorunresult",currnetpageindex,"ALL");
     
    loadautorunresulttoolbar();
    
    searchautorunresult();

 
	//加载对象列表容器
	function loadList(listmethod, objectType, pageindex, searchkeyword) {
		//加载列表
		$("#autorunresultlistcontainer").load("/autotesting/" + objectType + "/" + listmethod, {
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
		var contextMenu = $("#autorunresultrowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=autorunresultrowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=autorunresultidcontent]");
                	    autorunresultid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=autorunresultrowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function row_menu_event_handle()
	{
		$("li[name=autorunresultrowoperationedit]").click(function(){
			disable_autorunresult_toolbar();
			edit_autorunresult(autorunresultid);
		});
		$("li[name=autorunresultrowoperationdelete]").click(function(){
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" +autorunresultid + "的自动化任务吗？");
			$("#dialog-confirmdelete").dialog("open");
		});
		$("li[name=autorunresultrowoperationdetail]").click(function(){
		});
		$("li[name=autorunresultrowoperationreport]").click(function(){
			
		});
		$("li[name=autorunresultrowoperationcopy]").click(function(){
			$.post("/autotesting/autorunresult/copyautorunresult",{autorunresultid:autorunresultid},function(data,status){
				loadList("getlist", "autorunresult",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
		});
	}


	//点击checkbox

	function clickcheckbox() {
		$("[name = selectautorunresult]:checkbox").bind("click", function() {
			var $chk = $("[name = selectautorunresult]:checkbox");
			// $("#autorunresultselectall").attr("checked", $chk.length == $chk.filter(":checked").length);
		});
		// $("#autorunresultselectall").bind("click", function() {
			// var $chk = $("[name = selectautorunresult]:checkbox");
			// if ($chk.filter(":checked").length == $chk.length) {
				// $("[name = selectautorunresult]:checkbox").attr("checked", false);
			// } else {
				// $("[name = selectautorunresult]:checkbox").attr("checked", true);
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
		$("button[name=autorunresultrowedit]").click(function() {
			var element=$(this).parent().parent().find("span[class=autorunresultidcontent]");
            var autorunresultid=element.text();
			disable_autorunresult_toolbar();
			edit_autorunresult(autorunresultid);
		});
	}


	

	//鼠标滑过数据行
	function mouseroverdatarow() {
		$("li[class=autorunresultdatarow]").mouseover(function() {
			$(this).addClass("mouseroverdatarow");
		});
		$("li[class=autorunresultdatarow]").mouseout(function() {
			$(this).removeClass("mouseroverdatarow");
		});
	}
	
	
	
	//加载自动化任务工具栏
	function loadautorunresulttoolbar() {
		$("#autorunresulttoolbar").jqxToolBar({theme:theme,
			tools : "custom",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					case 0:
					    var searchbox=$("<div id='autorunresultsearchbox'><input id='autorunresultsearchinput'  type='text'/><div id='autorunresultsearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    tool.append(searchbox);
					    searchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						break;
				}
			}
		});
	}
	
	//auto task 创建
	
	
	
	function create_autorunresult(autorunresultid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#autorunresult_nameInput', message: '机器名称 是必填项!', action: 'keyup, blur', rule: 'required' },
                       { input: '#autorunresult_nameInput', message: '任务名称长度必须在5-100个字符之间!', action: 'keyup, blur', rule: 'length=5,100' },
                       { input: '#autorunresult_IPInput', message: 'IP地址是必须项', action: 'keyup, blur', rule: 'required' },
                       { input: '#autorunresult_browsers_listbox', message: '浏览器是必选项!', action: 'keyup, blur,change', rule: validate_autorunresult_browser}
                       ];
                       
		    $("#autorunresult_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#autorunresult_create").css('visibility', 'visible');
            $('#sendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#autorunresult_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#autorunresult_create_backbutton").on('click',function(){
            	$('#autorunresult_create_form').jqxValidator('hide');
            	loadautorunresultpage();
            }); 

              init_autorunresult_name(autorunresultid);
              init_autorunresult_os(autorunresultid);
              init_autorunresult_browser(autorunresultid);
              init_autorunresult_ip(autorunresultid);
              init_autorunresult_isreserved(autorunresultid);
            
            // $("#autorunresult_advance_button").jqxButton({theme:theme, width: '80'});
            // $("#autorunresult_advance_button").on('click',function(){
                 // $("tr[class=autorunresult_advance]").toggle();
            // });
              // change_tasktype_handler();
            
            $('#sendButton').on('click', function () 
            {
                $('#autorunresult_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#autorunresult_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(autorunresultid==0)
            	 {
            	 	send_createautorunresult_request();
            	 }
            	 else
            	 {
            	 	send_editautorunresult_request(autorunresultid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_autorunresult_name(autorunresultid)
	{
		$.post("/autotesting/autorunresult/init_autorunresult_formcontrol",{autorunresultid:autorunresultid,controlname:"AUTOAGENTNAME"},function(data,status){
			 $("#autorunresult_nameInput").jqxInput({theme:theme,placeHolder:"请输入任务名称!", width: 350, height: 25});
            if(data!="")
          {
        	$("#autorunresult_nameInput").jqxInput("val",data);
          }       			
		});
	}
	
	function validate_autorunresult_name()
	{
		return false;
	}
	
	
	//初始化代码地址
	
	//初始化任务名称字段
	function init_autorunresult_os(autorunresultid)
	{
		$.post("/autotesting/autorunresult/init_autorunresult_formcontrol",{autorunresultid:autorunresultid,controlname:"AUTOAGENTOS"},function(data,status){
			var autorunresult_OS =eval("(" + data + ")");
			var selectedIndex=0;
			for(var i in autorunresult_OS)
			{
				if(autorunresult_OS[i].selected==1)
				{
					selectedIndex=i;
					break;
				}
				
			}
		var countries =[{text:"All",value:0,isselected:false},{text:"A",value:1,isselected:false},{text:"B",value:2,isselected:false},{text:"C",value:3,isselected:true},{text:"D",value:4,isselected:true}];
        $("#autorunresult_OS_dropdownlist").jqxDropDownList({theme:theme,selectedIndex:selectedIndex,source: autorunresult_OS, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});           
		});
	}
	
	//初始化测试配置os
	
	function init_autorunresult_ip(autorunresultid)
	{
		$.post("/autotesting/autorunresult/init_autorunresult_formcontrol",{autorunresultid:autorunresultid,controlname:"AUTOAGENTIP"},function(data,status){
			 $("#autorunresult_IPInput").jqxInput({theme:theme,placeHolder:"请输入IP地址!", width: 350, height: 25});
            if(data!="")
             {
        	   $("#autorunresult_IPInput").jqxInput("val",data);
             }       			
			});		
	}
	
	
	//autorunresult_config validate function
	
	function validate_autorunresult_ip()
	{
		var result=false;
		var item = $("#autorunresult_IPInput").jqxInput('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
	}
	
	//初始化测试配置os
	
	function init_autorunresult_browser(autorunresultid)
	{
		$.post("/autotesting/autorunresult/init_autorunresult_formcontrol",{autorunresultid:autorunresultid,controlname:"AUTOAGENTBROWSER"},function(data,status){
			var autorunresulttype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#autorunresult_browsers_listbox").jqxListBox({theme:theme,selectedIndex:selectedIndex,multiple: true,source: autorunresulttype_source, width: 350, height: 200,displayMember:'text',valueMember:'memberid'});
			for(var i in autorunresulttype_source)
			{
				if(autorunresulttype_source[i].selected==1)
				{
					$("#autorunresult_browsers_listbox").jqxListBox('selectIndex', i);
				}
				
			}
			// var countries =[{text:"All",value:0},{text:"A",value:1},{text:"B",value:2},{text:"C",value:3},{text:"D",value:4}];
        // $("#autorunresult_browsers_listbox").jqxListBox({theme:theme,selectedIndex:selectedIndex,multiple: true,source: autorunresulttype_source, width: 350, height: 200,displayMember:'text',valueMember:'memberid'});      
			});		     
	}
	
	
	//autorunresult_config validate function
	
	function validate_autorunresult_browser()
	{
		var result=false;
		var item = $("#autorunresult_browsers_listbox").jqxListBox('getSelectedItems');
		 //空检查
		 if(item.length!=0)
		 {
		   result=true;
		 }
          return result;
	 }
	//初始化测试配置控件
	
	function init_autorunresult_isreserved(autorunresultid)
	{
		$.post("/autotesting/autorunresult/init_autorunresult_formcontrol",{autorunresultid:autorunresultid,controlname:"AUTOAGENTRESERVED"},function(data,status){
			var selectedIndex=0;
			if(data=="True")
			{
				selectedIndex=1;
			}
			var countries =[{text:"否",value:0},{text:"是",value:1}];
			$("#autorunresult_reserved_dropdownlist").jqxDropDownList({theme:theme,selectedIndex:selectedIndex,source: countries, width: 350, height: 25,displayMember:'text',valueMember:'value'});
		});           
	}
	
	
	
   //发送创建任务请求
   function send_createautorunresult_request()
   {
   	  var autorunresult_field=$('#autorunresult_create_form').serialize();
   	  $.post("/autotesting/autorunresult/create",$('#autorunresult_create_form').serialize(),function(data,status){
          loadautorunresultpage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_editautorunresult_request(autorunresultid)
   {
   	  var autorunresult_field=$('#autorunresult_create_form').serialize();
   	  $.post("/autotesting/autorunresult/edit",$('#autorunresult_create_form').serialize()+"&autorunresultid="+autorunresultid,function(data,status){
          loadautorunresultpage();
   	  });
   	  
   }
   

 
     
    
	
	
	//点击添加自动化任务按钮
	
	function click_add_autorunresult()
	{
		$("#middleContainer").load("/autotesting/autorunresult/create", function() {
			  create_autorunresult(0);
		});
	}
	
	//编辑自动化任务
	function edit_autorunresult(autorunresultid)
	{
		$("#middleContainer").load("/autotesting/autorunresult/edit", function() {
			  create_autorunresult(autorunresultid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_autorunresult_toolbar()
	{
		$("#autorunresulttoolbar").jqxToolBar("disableTool",0, true);
	    $("#autorunresulttoolbar").jqxToolBar("disableTool",1, true);
		$("#autorunresulttoolbar").jqxToolBar("disableTool",2, true);
		$("#autorunresulttoolbar").jqxToolBar("disableTool",3, true);
	}
	
    
	loadpagenation(get_search_keyword());
	function loadpagenation(searchkeyword) 
	{
		$.post("/autotesting/autorunresult/get_autorunresult_page_counts", {
			searchkeyword : searchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					searchkeyword = $('#autorunresultsearchinput').val();
					if (searchkeyword == "") 
					{
						 searchkeyword = "ALL";
					}
					loadList("getlist", "autorunresult", page,searchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadautorunresultpage() {
		$("#middleContainer").load("/autotesting/autorunresult/index", function() {
			$.getScript("/static/autotesting/js/autorunresult.js");
			loadautorunresulttoolbar();
		});
	}
	
	//复制提测项目
	function copyautorunresult() {
		$("#header_copy").click(function() {
			var $chk = $("[name = selectautorunresult:checkbox");
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
				autorunresultid = $chk.filter(":checked").parent().find("span[class=autorunresultidcontent]").text().trim();
				$.get("/autotesting/autorunresult/copy_autorunresult", {
					id : autorunresultid
				}, function(data, status) {
					$("#dialog-confirm").empty();
					$("#dialog-confirm").append(data);
					$("#dialog-confirm").dialog("open");
					searchkeyword = $('#autorunresultsearchinput').val();
					if (searchkeyword == "") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "autorunresult", currnetpageindex, searchkeyword);
				});
			}
		});
	}
	
	//search submition
	function searchautorunresult() {
		//点击搜索按钮
		$("#autorunresultsearchbutton").click(function() 
		{
			search_autorunresult_bykeyword();
		});
		
		$('#autorunresultsearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_autorunresult_bykeyword();
				}
			});
	}
	
	//search submition
	function search_autorunresult_bykeyword()
	{
		    searchkeyword = $('#autorunresultsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}

			loadpagenation(searchkeyword);
			loadList("getlist", "autorunresult", 1, searchkeyword);
	}
	
	//获取当前搜索关键字
	function get_search_keyword()
	{
		searchkeyword = $('#autorunresultsearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}
		return searchkeyword;
	}
	
	//删除任务确认
	
	function delete_autorunresult() {
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
					$.post("/autotesting/autorunresult/deleteautorunresult",{autorunresultid:autorunresultid},function(data,status){
				loadList("getlist", "autorunresult",currnetpageindex,get_search_keyword());
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
