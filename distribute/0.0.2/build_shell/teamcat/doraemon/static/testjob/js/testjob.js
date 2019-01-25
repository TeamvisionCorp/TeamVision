$(document).ready(function() {

	var currnetpageindex = 1;
	var producttype = "0";
	var jobstatus = "0";
	var searchkeyword="ALL";
	//加载默认任务列表以及操作
	loadOperation("getoperation", "testjob");
	loadList("getlist", "testjob", currnetpageindex, "ALL", "0", "0");
	// loadrightcontainer();
	//加载测试任务左导航项目
	// $("#leftBarContainer").load("/testtask/testtask/getleftnavigater", function(data, textstatus) {
	// $("#lefttab li").click(function() {
	// $("#lefttab li").removeClass("lefttabactive");
	// $("#lefttab li").removeClass("lefttenabactive");
	// $("#lefttab li").addClass("lefttabenactive");
	// $(this).removeClass("lefttabenactive");
	// $(this).addClass("lefttabactive");
	// var listmethod = $(this).attr("method");
	// var objectType = $(this).attr("name");
	// loadList(listmethod, objectType);
	// loadOperation("getoperation", objectType);
	// });
	// });

	//加载右边栏
	function loadrightcontainer() {
		$("#rightContainer").load("/testjob/getrightcontainer", function(data, textstatus) {
			var accordionContainer = $("#accordion");
			accordionContainer.accordion({
				collapsible : true
			},{ active: false }
			);
			$("#producttypefilter").selectable({
				stop : function() {
					$(".ui-selected", this).each(function() {
						var index = $("#producttypefilter li").index(this);
						producttype= $("#producttypefilter").children("li:eq("+index+")").attr("name");
						loadpagenation(searchkeyword,"0","0");
						loadList("getlist", "testjob", currnetpageindex, searchkeyword,"producttype","0","0");
					});
				}
			});
			$("#jobstatusfilter").selectable({
				stop : function() {
					$(".ui-selected",this).each(function() {
						var index = $("#jobstatusfilter li").index(this);
						jobstatus= $("#jobstatusfilter").children("li:eq("+index+")").attr("name");
						loadpagenation(searchkeyword,producttype,jobstatus);
						loadList("getlist", "testjob", currnetpageindex,searchkeyword,"0",jobstatus);
					});
				}
			});
			
			$("#jobproperties").selectable({
				stop : function() {
					$(".ui-selected",this).each(function() {
						var index = $("#jobproperties li").index(this);
					});
				}
			});
		});
	}

	//加载对象列表容器
	function loadList(listmethod, objectType, pageindex, searchkeyword, producttype, jobstatus) {
		//加载列表
		$("#listcontainer").load("/" + objectType + "/" + listmethod, {
			pageindex : pageindex,
			searchkeyword : searchkeyword,
			producttype : producttype,
			jobstatus : jobstatus
		}, function(data, status) {
			//加载测试进度
			loadprogress();
			//点击行编辑按钮弹出编辑窗口
			clickrowedit();
			//点击复选框
			clickcheckbox();

			//双击行
			doubleclickrow();
			// mouseroverdatarow();
			// $("span[class=testjobidcontent]").each(function(){
				// $(this).hide();
			// });
			$("span[class=testjobsubmitidcontent]").each(function(){
				$(this).hide();
			});
		});

	}


	//点击checkbox

	function clickcheckbox() {
		$("[name = selecttestjob]:checkbox").bind("click", function() {
			var $chk = $("[name = selecttestjob]:checkbox");
			$("#selectall").attr("checked", $chk.length == $chk.filter(":checked").length);
		});
		$("#selectall").bind("click", function() {
			var $chk = $("[name = selecttestjob]:checkbox");
			if ($chk.filter(":checked").length == $chk.length) {
				$("[name = selecttestjob]:checkbox").attr("checked", false);
			} else {
				$("[name = selecttestjob]:checkbox").attr("checked", true);
			}
		});
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

	//弹出编辑对话框
	function openEditJobDialog(jobid) {
		$.get("/testjob/edit", {
			id : jobid
		}, function(data, status) {
			$("#dialog-edittestjob").append(data);
			showecalenderforeditform();
			addstyleforform();
			loadjobname();
			$("#TJEndTime").hide();
		});
		//显示编辑任务窗口
		$("#dialog-edittestjob").dialog("open");
	}

	//加载测试进度
	function loadprogress() {
		$("div[name=testjobprogress]").each(function(index, element) {
			var jobid = $(element).parent().parent().find("span[class=testjobidcontent]").text().trim();
			$.get("/testjob/getjobprogress", {
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

	//鼠标滑过数据行
	function mouseroverdatarow() {
		$("li[class=testjobdatarow]").mouseover(function() {
			$(this).addClass("mouseroverdatarow");
		});
		$("li[class=testjobdatarow]").mouseout(function() {
			$(this).removeClass("mouseroverdatarow");
		});
	}

	//根据提测ID动态加载Job名称
	function loadjobname() {
		$("#id_TJSubmitionID").blur(function() {
			$.get("/testjob/getjobname", {
				'submitionid' : $(this).val()
			}, function(data, status) {
				$("#id_TJJobName").attr("value", data);
			});
		});
	}

	//为创建，编辑窗口添加样式
	function addstyleforform() {
		$("#testjobformview form fieldset input").addClass("text ui-widget-content ui-corner-all");
		$("fieldset input[type=text]").addClass("modelforminputbox");
		$("fieldset[class=modelform] select").addClass("modelformselect").addClass("formselect");
		$("fieldset[class=modelform] select[multiple=multiple]").addClass("modelformmulipleselect");
		$("#jobadvancedbutton").click(function(data, status) {
			$("#jobadvancedoptions").toggle();
		});
	}

	//加载edit 日历控件
	function showecalenderforeditform() {
		$("#id_TJStartTime").click(function() {
			$("#id_TJStartTime").datepicker({
				showOn : "button",
				buttonImage : "/static/global/images/calendar.gif",
				buttonImageOnly : true,
				buttonText : "Select date"
			});
			$("#id_TJStartTime").datepicker("option", "dateFormat", "yy-mm-dd");
			$("#id_TJStartTime").datepicker("option", "showAnim", "slide");
		});
		$("#id_TJEndTime").click(function() {
			$("#id_TJEndTime").datepicker({
				showOn : "button",
				buttonImage : "/static/global/images/calendar.gif",
				buttonImageOnly : true,
				buttonText : "Select date"
			});
			$("#id_TJEndTime").datepicker("option", "dateFormat", "yy-mm-dd");
			$("#id_TJEndTime").datepicker("option", "showAnim", "slide");
		});
	}

	//加载新建窗口的日历控件
	function showcalenderforaddform() {
		$("#id_TJStartTime").datepicker();
		$("#id_TJStartTime").datepicker("option", "dateFormat", "yy-mm-dd");
		$("#id_TJStartTime").datepicker("option", "showAnim", "slide");
		$("#id_TJEndTime").datepicker();
		$("#id_TJEndTime").datepicker("option", "dateFormat", "yy-mm-dd");
		$("#id_TJEndTime").datepicker("option", "showAnim", "slide");
	}

	//加载操作容器
	function loadOperation(opmethod, objectType) {

		//加载任务操作操作
		$("#operationcontainer").load("/" + objectType + "/" + opmethod, function(data, statutext) {
			//焦点进入搜索输入框，清除默认问题
			defaultsearch();
			clicksearchjobbutton();
			searchjobbypressenterkey();
			//隐藏行操作列表
			//click edittask button on top
			$("#header_edit").click(function() {
				$("button[name=rowedit]").toggle();
				$("button[name=detail]").toggle();
				$("button[name=newchildjob]").toggle();
			});

			//点击添加任务弹出创建窗口
			$("#header_new").click(function() {
				//加载创建任务form
				$("#dialog-newtestjob").load("/" + objectType + "/create", function(data, status) {
					addstyleforform();
					showcalenderforaddform();
					loadjobname();
				});
				//显示创建任务窗口
				$("#dialog-newtestjob").dialog("open");
			});
			$("#header_copy").click(function() {
				var $chk = $("[name = selecttestjob]:checkbox");
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
					jobid = $chk.filter(":checked").parent().find("span[class=testjobidcontent]").text().trim();
					$.get("/testjob/copyjob", {
						id : jobid
					}, function(data, status) {
						$("#dialog-confirm").empty();
						$("#dialog-confirm").append(data);
						$("#dialog-confirm").dialog("open");
						searchkeyword = $('#searchkeyword').val();
						if (searchkeyword == "请输入ID或名称搜索") {
							searchkeyword = "ALL";
						}
						loadList("getlist", "testjob", currnetpageindex, searchkeyword,"0","0");
					});
				}
			});
		});
	}

	//搜索框逻辑
	function defaultsearch() {
		//焦点进入搜索输入框，清除默认问题
		$('#searchkeyword').focus(function() {
			if ($(this).val() == '请输入ID或名称搜索') {
				$(this).val("");
			}
		});

		//焦点离开搜索输入框，显示默认文字
		$('#searchkeyword').blur(function() {
			if ($(this).val() == '') {
				$(this).val("请输入ID或名称搜索");
			}
		});

	}

	//search job by click search button
	function clicksearchjobbutton() {
		//点击搜索按钮
		$("#searchjob").click(function() {
			searchjob();
		});

	}

	//search job by press enter key
	function searchjobbypressenterkey() {
		$('#searchkeyword').keyup(function() {
			if (event.keyCode == 13) {
				searchjob();
			}
		});
	}

	//search job
	function searchjob() {
		searchkeyword = $('#searchkeyword').val().trim();
		if (searchkeyword == "请输入ID或名称搜索") {
			searchkeyword = "ALL";
		}

		loadpagenation(searchkeyword,"0","0");
		loadList("getlist", "testjob", 1, searchkeyword,"0","0");
	}

	//新建任务
	$(function() {
		var submitionid = $("#id_TJSubmitionID"), jobname = $("#id_TJJobName"), starttime = $("#id_TJStartTime"), endtime = $("#id_TJEndTime"), tester = $("#id_TJTester"), progress = $("#id_TJProgress");
		allFields = $([]).add(submitionid).add(jobname).add(starttime).add(endtime).add(tester).add(progress);
		function updateTips(t) {
			var tips = $(".validateTips");
			tips.text(t).addClass("ui-state-highlight");
			setTimeout(function() {
				tips.removeClass("ui-state-highlight", 10000);
			}, 10000);
		}

		function checkIsNull(o, n) {
			if (!(o.val().length > 0)) {
				o.addClass("ui-state-error");
				updateTips(n);
				return false;
			} else {
				return true;
			}
		}

		function addjob() {
			var submitionid = $("#id_TJSubmitionID"), jobname = $("#id_TJJobName"), starttime = $("#id_TJStartTime"), endtime = $("#id_TJEndTime"), tester = $("#id_TJTester"), progress = $("#id_TJProgress");
			// var bugCounts=$("#id_TJBugCounts");
			allFields = $([]).add(submitionid).add(jobname).add(starttime).add(endtime).add(tester).add(progress);
			var valid = true;
			allFields.removeClass("ui-state-error");
			valid = valid && checkIsNull(submitionid, "提测ID为必填项,没有提测ID，请填写0！");
			valid = valid && checkIsNull(jobname, "任务名称为必填项！");
			valid = valid && checkIsNull(starttime, "任务开始时间为必填项！");
			valid = valid && checkIsNull(endtime, "任务结束时间为必填项！");
			valid = valid && checkIsNull(tester, "测试人员为必填项！");
			valid = valid && checkIsNull(progress, "进度信息为必填项！");

			if (valid) {
				$.post("/testjob/create", $('#testjobcreate').serialize(), function(data, status) {
					searchkeyword = $('#searchkeyword').val();
					if (searchkeyword == "请输入ID或名称搜索") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "testjob", currnetpageindex, searchkeyword,"0","0");
					$("#testjobformview").remove();
				});
				$("#dialog-newtestjob").dialog("close");
				$("#dialog-edittestjob").dialog("close");
			}
			return valid;
		}

		function editjob() {
			var submitionid = $("#id_TJSubmitionID"),jobid=$("#id_id"),jobname = $("#id_TJJobName"), starttime = $("#id_TJStartTime"), endtime = $("#id_TJEndTime"), tester = $("#id_TJTester"), progress = $("#id_TJProgress");
			allFields = $([]).add(submitionid).add(jobname).add(starttime).add(endtime).add(tester).add(progress);
			var valid = true;
			allFields.removeClass("ui-state-error");
			valid = valid && checkIsNull(submitionid, "提测ID为必填项,没有提测ID，请填写0！");
			valid = valid && checkIsNull(jobname, "任务名称为必填项！");
			valid = valid && checkIsNull(starttime, "任务开始时间为必填项！");
			valid = valid && checkIsNull(endtime, "任务结束时间为必填项！");
			valid = valid && checkIsNull(tester, "测试人员为必填项！");
			valid = valid && checkIsNull(progress, "进度信息为必填项！");

			if (valid) {
				$.post("/testjob/edit", $('#testjobcreate').serialize(), function(data, status) {
					searchkeyword = $('#searchkeyword').val();
					if (searchkeyword == "请输入ID或名称搜索") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "testjob", currnetpageindex, searchkeyword,"0","0");
					$("#testjobformview").remove();
				});
				$("#dialog-edittestjob").dialog("close");
			}
		    $.get('/testjob/updatecodelines',{'testjobid':jobid.val()});
			return valid;
		}

		dialog = $("#dialog-newtestjob").dialog({
			autoOpen : false,
			height : 600,
			width : 700,
			modal : true,
			buttons : {
				"添加Job" : addjob,
				取消 : function() {
					$(this).dialog("close");
					$("#testjobformview").remove();
				}
			},
			close : function() {
				allFields.removeClass("ui-state-error");
				$("#testjobformview").remove();
			}
		});

		$("#dialog-edittestjob").dialog({
			autoOpen : false,
			height : 600,
			width : 700,
			modal : true,
			buttons : {
				"保存" : editjob,
				取消 : function() {
					$(this).dialog("close");
					$("#testjobformview").remove();
				}
			},
			close : function() {
				allFields.removeClass("ui-state-error");
				$("#testjobformview").remove();
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
				allFields.removeClass("ui-state-error");
			}
		});

	});

	//加载分页控件

	loadpagenation("ALL","0","0");
	function loadpagenation(searchkeyword,filterproducttype,filterjobstatus) {
		$.post("/testjob/getjobcounts", {
			searchkeyword : searchkeyword,
			producttype:filterproducttype,
			jobstatus:filterjobstatus
		}, function(data, status) {
			$('.pagination').jqPagination({
				link_string : '/?page={page_number}',
				max_page : data,
				paged : function(page) {
					currnetpageindex = page;
					searchkeyword = $('#searchkeyword').val();
					if (searchkeyword == "请输入ID或名称搜索") {
						searchkeyword = "ALL";
					}
					loadList("getlist", "testjob", page, searchkeyword,"0","0");
				}
			});
		});

	}

});
