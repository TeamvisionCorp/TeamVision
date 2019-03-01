$(document).ready(function() {
	var theme = 'metro';

	init_page();
	cancel_task();
	cancel_tq();
	open_build_log_dalog();
	save_url_to_cookie();

	function init_page() {
		$("span[name=loader]").hide();
	}

	function open_build_log_dalog() {
		$("span[name=ci_bulid_log]").click(function(event) {
			$("#global-mark").addClass('mark');
			$("#global-mark").show();
			var tq_id = $($(this).parent().find("span[name=tq_id]")[0]).text();
			$("#popup-dialog-container").load("/ci/dashboard/build_log_dialog", {
				"tq_id" : tq_id
			}, function() {
				$("#global-mark").removeClass('mark');
				load_pre_log();
			$("#global-mark").hide();
			adjust_bulid_log_dialog_size();
				window.onresize = function() {
		       adjust_bulid_log_dialog_size();
	            }
				$("#build-log-popup-dialog").modal('show');
				$('#build-log-popup-dialog').on('hidden.bs.modal', function(e) {
					$("#web_socket_scripts").empty(); 
				});
			});
		});
	}

	
	
	
	//load pre log contents
	
	function load_pre_log()
	{
		$("#prelog_trigger").click(function(){
			$("#build_log_loader").show();
			var tq_id=$("#log_dialog_tq_id").val();
			$(this).hide();
			$("#billboard").load("/ci/dashboard/pre_build_log",{"tq_id":tq_id});
		});
	}
	
    adjust_bulid_log_dialog_size();
	function adjust_bulid_log_dialog_size() {
		var window_width = window.innerWidth;
		console.log(window_width);
		var parent_width=window_width*0.8;
		var child_width=window_width*0.8*0.8;
			$("#build-content-container").parent().css('width',parent_width+"px");
			$("#billboard").css('width',child_width+"px" );
			$("#build-content-container").parent().css('margin-left', 'auto');
	}

	function cancel_tq() {
		$("span[name=tq_stop]").click(function() {
			var tq_uuid = $($(this).parent().parent().parent().find("span[name=tq_uuid]")[0]).text();
			var ci_task_id = $($(this).parent().parent().parent().find("span[name=task_id]")[0]).text();
			stop_task_request(ci_task_id, tq_uuid);
		});
	}

	function cancel_task() {
		$("span[name=task_stop]").click(function() {
			var tq_uuid = $($(this).parent().find("span[name=tq_uuid]")[0]).text();
			var ci_task_id = $($(this).parent().parent().parent().find("span[name=task_id]")[0]).text();
			stop_task_request(ci_task_id, tq_uuid);
		});
	}

	function stop_task_request(ci_task_id, tq_uuid) {
		$.post("/ci/task/stop/" + ci_task_id, {
			"task_uuid" : tq_uuid
		}, function(data, status) {
			if (data == "False") {
				init_notification('error', data, true);
			} else {
				init_notification('success', "任务取消指令已经下发！", true);
			}

		});

	}
	
	
	//点击历史连接，保存当前url到cookie
	function save_url_to_cookie() {
		$("a[name=ci_task_name]").click(function() {
			// delCookie('ci_task_entrance_link');
			setCookie("ci_task_entrance_link", window.location.href);
		});
	}
	
	//保存cookie
	function setCookie(name, value)//两个参数，一个是cookie的名子，一个是值
	{
		var Days = 1;
		//此 cookie 将被保存 30 天
		var exp = new Date();
		//new Date("December 31, 9998");
		exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
		document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString() + ";path=/";
	}

	window.setInterval(refresh_build_status,5*1000);
	window.setInterval(refresh_tq_list,5*1000);

	// 定时刷新构建状态
	function refresh_build_status() {
		$("#ci_dashboard_agent_container").load("/ci/dashboard/agent_list", function() {
			cancel_task();
			cancel_tq();
			open_build_log_dalog();
			save_url_to_cookie();
		});
	}

	//定时刷新任务队列
	function refresh_tq_list() {
		$("#ci_dashboard_taskqueue_container").load("/ci/dashboard/tq_list", function() {
			cancel_task();
			cancel_tq();
			save_url_to_cookie();
		});
	}

	function init_notification(template, data, autoclose) {
		$("#operation_notification").jqxNotification({
			width : 250,
			// position : "bottom-right",
			opacity : 0.8,
			autoOpen : false,
			animationOpenDelay : 300,
			autoClose : autoclose,
			template : template,
			appendContainer: "#notification_container",
		});
		$("#operation_notification_message").empty();
		$("#operation_notification_message").append(data);
		$("#operation_notification").jqxNotification("open");
	}

});
