$(document).ready(function() {

	var currnetpageindex = 1;
	var searchkeyword="ALL";
	var automobiledeviceid=0;
	var theme='arctic';

	loadList("getlist", "automobiledevice",currnetpageindex,"ALL");
     
    loadautomobiledevicetoolbar();
    
    searchautomobiledevice();

 
	//加载对象列表容器
	function loadList(listmethod, objectType, pageindex, searchkeyword) {
		//加载列表
		$("#automobiledevicelistcontainer").load("/autotesting/" + objectType + "/" + listmethod, {
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
		var contextMenu = $("#automobiledevicerowoperation").jqxMenu({theme:theme,width: '120px', height: '140px', autoOpenPopup: false, mode: 'popup'});
                // open the context menu when the user presses the mouse right button.
                $("img[name=automobiledevicerowmore]").on('click', function (event) {
                	    var element=$(this).parent().parent().find("span[class=automobiledeviceidcontent]");
                	    automobiledeviceid=element.text();
                        var scrollTop = $(window).scrollTop();
                        var scrollLeft = $(window).scrollLeft();
                        $("ul[name=automobiledevicerowoperationitems]").show();
                        contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
                        return false;
                    
                });
	}
	
	//row menu item handler
	function row_menu_event_handle()
	{
		$("li[name=automobiledevicerowoperationedit]").click(function(){
			disable_automobiledevice_toolbar();
			edit_automobiledevice(automobiledeviceid);
		});
		$("li[name=automobiledevicerowoperationdelete]").click(function(){
			$("#dialog-confirmdelete").empty();
			$("#dialog-confirmdelete").append("确定要删除ID为" +automobiledeviceid + "的自动化任务吗？");
			$("#dialog-confirmdelete").dialog("open");
		});
		$("li[name=automobiledevicerowoperationdetail]").click(function(){
		});
		$("li[name=automobiledevicerowoperationreport]").click(function(){
			
		});
		$("li[name=automobiledevicerowoperationcopy]").click(function(){
			$.post("/autotesting/automobiledevice/copyautomobiledevice",{automobiledeviceid:automobiledeviceid},function(data,status){
				loadList("getlist", "automobiledevice",currnetpageindex,get_search_keyword());
				loadpagenation(get_search_keyword());
			});
		});
	}


	//点击checkbox

	function clickcheckbox() {
		$("[name = selectautomobiledevice]:checkbox").bind("click", function() {
			var $chk = $("[name = selectautomobiledevice]:checkbox");
			// $("#automobiledeviceselectall").attr("checked", $chk.length == $chk.filter(":checked").length);
		});
		// $("#automobiledeviceselectall").bind("click", function() {
			// var $chk = $("[name = selectautomobiledevice]:checkbox");
			// if ($chk.filter(":checked").length == $chk.length) {
				// $("[name = selectautomobiledevice]:checkbox").attr("checked", false);
			// } else {
				// $("[name = selectautomobiledevice]:checkbox").attr("checked", true);
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
		$("button[name=automobiledevicerowedit]").click(function() {
			var element=$(this).parent().parent().find("span[class=automobiledeviceidcontent]");
            var automobiledeviceid=element.text();
			disable_automobiledevice_toolbar();
			edit_automobiledevice(automobiledeviceid);
		});
	}


	

	//鼠标滑过数据行
	function mouseroverdatarow() {
		$("li[class=automobiledevicedatarow]").mouseover(function() {
			$(this).addClass("mouseroverdatarow");
		});
		$("li[class=automobiledevicedatarow]").mouseout(function() {
			$(this).removeClass("mouseroverdatarow");
		});
	}
	
	
	
	//加载自动化任务工具栏
	function loadautomobiledevicetoolbar() {
		$("#automobiledevicetoolbar").jqxToolBar({theme:theme,
			tools : "custom",
			initTools : function(type, index, tool, menuToolIninitialization) {
				// var countries = new Array("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antarctica", "Antigua and Barbuda");
                
				switch (index) {
					// case 0:
						// tool.jqxButton({width:80});
						// tool.text("添加");
						// tool.on("click",function(event){
							// disable_automobiledevice_toolbar();
							// click_add_automobiledevice();
						// });
						// break;
					case 0:
					    var searchbox=$("<div id='automobiledevicesearchbox'><input id='automobiledevicesearchinput'  type='text'/><div id='automobiledevicesearchbutton'><img alt='search' width='16' height='16' src='/static/global/js/jqwidgets-ver3.7.1/jqwidgets/styles/images/search.png' /></div></div>");     
					    tool.append(searchbox);
					    // var source ={
                            // datatype: "json",
                            // datafields:[{name:'automobiledevicename'}],
                            // url: '/autotesting/automobiledevice/get_taskname_list'
                            // };
                        // var dataAdapter = new $.jqx.dataAdapter(source);
					    searchbox.jqxInput({theme:theme, placeHolder: "请输入ID或者名称", height: 23, width: 250, minLength: 1});
						break;
				}
			}
		});
	}
	
	//auto task 创建
	
	
	
	function create_automobiledevice(automobiledeviceid)
	{
		//控件验证规则
		var valdaterules=[
                       { input: '#automobiledevice_nameInput', message: '机器名称 是必填项!', action: 'keyup, blur', rule: 'required' },
                       { input: '#automobiledevice_nameInput', message: '任务名称长度必须在5-100个字符之间!', action: 'keyup, blur', rule: 'length=5,100' },
                       { input: '#automobiledevice_IPInput', message: 'IP地址是必须项', action: 'keyup, blur', rule: 'required' },
                       { input: '#automobiledevice_browsers_listbox', message: '浏览器是必选项!', action: 'keyup, blur,change', rule: validate_automobiledevice_browser}
                       ];
                       
		    $("#automobiledevice_create").jqxExpander({theme:theme, toggleMode: 'none', width: '100%', height:'100%', showArrow: false });
		    $("#automobiledevice_create").css('visibility', 'visible');
            $('#sendButton').jqxButton({theme:theme, width: 80, height: 25 });
            $("#automobiledevice_create_backbutton").jqxButton({theme:theme, width: '60'});
            $("#automobiledevice_create_backbutton").on('click',function(){
            	$('#automobiledevice_create_form').jqxValidator('hide');
            	loadautomobiledevicepage();
            }); 

              init_automobiledevice_name(automobiledeviceid);
              init_automobiledevice_os(automobiledeviceid);
              init_automobiledevice_browser(automobiledeviceid);
              init_automobiledevice_ip(automobiledeviceid);
              init_automobiledevice_isreserved(automobiledeviceid);
            
            // $("#automobiledevice_advance_button").jqxButton({theme:theme, width: '80'});
            // $("#automobiledevice_advance_button").on('click',function(){
                 // $("tr[class=automobiledevice_advance]").toggle();
            // });
              // change_tasktype_handler();
            
            $('#sendButton').on('click', function () 
            {
                $('#automobiledevice_create_form').jqxValidator('validate');
            });
            // initialize validator.
            $('#automobiledevice_create_form').jqxValidator({rules: valdaterules,onSuccess: function(){
            	 if(automobiledeviceid==0)
            	 {
            	 	send_createautomobiledevice_request();
            	 }
            	 else
            	 {
            	 	send_editautomobiledevice_request(automobiledeviceid);
            	 }
            	 }});
	}
	
	//初始化任务名称字段
	function init_automobiledevice_name(automobiledeviceid)
	{
		$.post("/autotesting/automobiledevice/init_automobiledevice_formcontrol",{automobiledeviceid:automobiledeviceid,controlname:"AUTOAGENTNAME"},function(data,status){
			 $("#automobiledevice_nameInput").jqxInput({theme:theme,placeHolder:"请输入任务名称!", width: 350, height: 25});
            if(data!="")
          {
        	$("#automobiledevice_nameInput").jqxInput("val",data);
          }       			
		});
	}
	
	function validate_automobiledevice_name()
	{
		return false;
	}
	
	
	//初始化代码地址
	
	//初始化任务名称字段
	function init_automobiledevice_os(automobiledeviceid)
	{
		$.post("/autotesting/automobiledevice/init_automobiledevice_formcontrol",{automobiledeviceid:automobiledeviceid,controlname:"AUTOAGENTOS"},function(data,status){
			var automobiledevice_OS =eval("(" + data + ")");
			var selectedIndex=0;
			for(var i in automobiledevice_OS)
			{
				if(automobiledevice_OS[i].selected==1)
				{
					selectedIndex=i;
					break;
				}
				
			}
		var countries =[{text:"All",value:0,isselected:false},{text:"A",value:1,isselected:false},{text:"B",value:2,isselected:false},{text:"C",value:3,isselected:true},{text:"D",value:4,isselected:true}];
        $("#automobiledevice_OS_dropdownlist").jqxDropDownList({theme:theme,selectedIndex:selectedIndex,source: automobiledevice_OS, width: 350, height: 25,displayMember:'text',valueMember:'memberid'});           
		});
	}
	
	//初始化测试配置os
	
	function init_automobiledevice_ip(automobiledeviceid)
	{
		$.post("/autotesting/automobiledevice/init_automobiledevice_formcontrol",{automobiledeviceid:automobiledeviceid,controlname:"AUTOAGENTIP"},function(data,status){
			 $("#automobiledevice_IPInput").jqxInput({theme:theme,placeHolder:"请输入IP地址!", width: 350, height: 25});
            if(data!="")
             {
        	   $("#automobiledevice_IPInput").jqxInput("val",data);
             }       			
			});		
	}
	
	
	//automobiledevice_config validate function
	
	function validate_automobiledevice_ip()
	{
		var result=false;
		var item = $("#automobiledevice_IPInput").jqxInput('getSelectedItem');
		
		//空检查
		if(item!=null)
		{
			result=true;
		}
        return result;
	}
	
	//初始化测试配置os
	
	function init_automobiledevice_browser(automobiledeviceid)
	{
		$.post("/autotesting/automobiledevice/init_automobiledevice_formcontrol",{automobiledeviceid:automobiledeviceid,controlname:"AUTOAGENTBROWSER"},function(data,status){
			var automobiledevicetype_source =eval("(" + data + ")");
			var selectedIndex=0;
			$("#automobiledevice_browsers_listbox").jqxListBox({theme:theme,selectedIndex:selectedIndex,multiple: true,source: automobiledevicetype_source, width: 350, height: 200,displayMember:'text',valueMember:'memberid'});
			for(var i in automobiledevicetype_source)
			{
				if(automobiledevicetype_source[i].selected==1)
				{
					$("#automobiledevice_browsers_listbox").jqxListBox('selectIndex', i);
				}
				
			}
			// var countries =[{text:"All",value:0},{text:"A",value:1},{text:"B",value:2},{text:"C",value:3},{text:"D",value:4}];
        // $("#automobiledevice_browsers_listbox").jqxListBox({theme:theme,selectedIndex:selectedIndex,multiple: true,source: automobiledevicetype_source, width: 350, height: 200,displayMember:'text',valueMember:'memberid'});      
			});		     
	}
	
	
	//automobiledevice_config validate function
	
	function validate_automobiledevice_browser()
	{
		var result=false;
		var item = $("#automobiledevice_browsers_listbox").jqxListBox('getSelectedItems');
		 //空检查
		 if(item.length!=0)
		 {
		   result=true;
		 }
          return result;
	 }
	//初始化测试配置控件
	
	function init_automobiledevice_isreserved(automobiledeviceid)
	{
		$.post("/autotesting/automobiledevice/init_automobiledevice_formcontrol",{automobiledeviceid:automobiledeviceid,controlname:"AUTOAGENTRESERVED"},function(data,status){
			var selectedIndex=0;
			if(data=="True")
			{
				selectedIndex=1;
			}
			var countries =[{text:"否",value:0},{text:"是",value:1}];
			$("#automobiledevice_reserved_dropdownlist").jqxDropDownList({theme:theme,selectedIndex:selectedIndex,source: countries, width: 350, height: 25,displayMember:'text',valueMember:'value'});
		});           
	}
	
	
	
   //发送创建任务请求
   function send_createautomobiledevice_request()
   {
   	  var automobiledevice_field=$('#automobiledevice_create_form').serialize();
   	  $.post("/autotesting/automobiledevice/create",$('#automobiledevice_create_form').serialize(),function(data,status){
          loadautomobiledevicepage();
   	  });
   	  
   }
   
   //保存编辑后的任务
    function send_editautomobiledevice_request(automobiledeviceid)
   {
   	  var automobiledevice_field=$('#automobiledevice_create_form').serialize();
   	  $.post("/autotesting/automobiledevice/edit",$('#automobiledevice_create_form').serialize()+"&automobiledeviceid="+automobiledeviceid,function(data,status){
          loadautomobiledevicepage();
   	  });
   	  
   }
   

 
     
    
	
	
	//点击添加自动化任务按钮
	
	function click_add_automobiledevice()
	{
		$("#middleContainer").load("/autotesting/automobiledevice/create", function() {
			  create_automobiledevice(0);
		});
	}
	
	//编辑自动化任务
	function edit_automobiledevice(automobiledeviceid)
	{
		$("#middleContainer").load("/autotesting/automobiledevice/edit", function() {
			  create_automobiledevice(automobiledeviceid);
		});
	}
	
	
	//点击添加任务，工具条不可用
	function disable_automobiledevice_toolbar()
	{
		$("#automobiledevicetoolbar").jqxToolBar("disableTool",0, true);
	    $("#automobiledevicetoolbar").jqxToolBar("disableTool",1, true);
		$("#automobiledevicetoolbar").jqxToolBar("disableTool",2, true);
		$("#automobiledevicetoolbar").jqxToolBar("disableTool",3, true);
	}
	
    
	loadpagenation(get_search_keyword());
	function loadpagenation(searchkeyword) 
	{
		$.post("/autotesting/automobiledevice/get_automobiledevice_page_counts", {
			searchkeyword : searchkeyword
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					searchkeyword = $('#automobiledevicesearchinput').val();
					if (searchkeyword == "") 
					{
						 searchkeyword = "ALL";
					}
					loadList("getlist", "automobiledevice", page,searchkeyword);
				 }
			 });
		});
	}
    // 清理左右 栏自动化任务页面
	function loadautomobiledevicepage() {
		$("#middleContainer").load("/autotesting/automobiledevice/index", function() {
			$.getScript("/static/autotesting/js/automobiledevice.js");
			loadautomobiledevicetoolbar();
		});
	}
	
	//复制提测项目
	function copyautomobiledevice() {
		$("#header_copy").click(function() {
			var $chk = $("[name = selectautomobiledevice:checkbox");
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
				automobiledeviceid = $chk.filter(":checked").parent().find("span[class=automobiledeviceidcontent]").text().trim();
				$.get("/autotesting/automobiledevice/copy_automobiledevice", {
					id : automobiledeviceid
				}, function(data, status) {
					$("#dialog-confirm").empty();
					$("#dialog-confirm").append(data);
					$("#dialog-confirm").dialog("open");
					searchkeyword = $('#automobiledevicesearchinput').val();
					if (searchkeyword == "") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "automobiledevice", currnetpageindex, searchkeyword);
				});
			}
		});
	}
	
	//search submition
	function searchautomobiledevice() {
		//点击搜索按钮
		$("#automobiledevicesearchbutton").click(function() 
		{
			search_automobiledevice_bykeyword();
		});
		
		$('#automobiledevicesearchinput').keyup(function(){
				if(event.keyCode==13)
				{
					search_automobiledevice_bykeyword();
				}
			});
	}
	
	//search submition
	function search_automobiledevice_bykeyword()
	{
		    searchkeyword = $('#automobiledevicesearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}

			loadpagenation(searchkeyword);
			loadList("getlist", "automobiledevice", 1, searchkeyword);
	}
	
	//获取当前搜索关键字
	function get_search_keyword()
	{
		searchkeyword = $('#automobiledevicesearchinput').val().trim();
			if (searchkeyword == "") {
				searchkeyword = "ALL";
			}
		return searchkeyword;
	}
	
	//删除任务确认
	
	function delete_automobiledevice() {
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
					$.post("/autotesting/automobiledevice/deleteautomobiledevice",{automobiledeviceid:automobiledeviceid},function(data,status){
				loadList("getlist", "automobiledevice",currnetpageindex,get_search_keyword());
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
