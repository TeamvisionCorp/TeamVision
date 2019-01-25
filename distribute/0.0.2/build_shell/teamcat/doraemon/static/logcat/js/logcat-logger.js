$(document).ready(function() 
{

var current_filter="all";
var web_socket=null;


logcat_logger_clickhandler();
get_more_log();
init_page();
remove_logger();



//初始化页面
function init_page(){
	$(".logcat_logger_item").mouseover(function(){
		$(this).find("i[name=logcat_logger_remove]").show();
	});
	$(".logcat_logger_item").mouseout(function(){
		$(this).find("i[name=logcat_logger_remove]").hide();
	});
	
}

//ajax初始化

function ajax_init_page(){
	logcat_logger_clickhandler();
	get_more_log();
	init_page();
	remove_logger();

}

//删除logger
function remove_logger(){
	$("i[name=logcat_logger_remove]").click(function(){
		var logger_id=$(this).parent().find('span').attr("loggerID");
		var target=$(this).parent();
		$.get("/logcat/logger/"+logger_id+"/delete",function(data,status){
			if(data=="True")
				{
				  $(target).remove();
				}
		});
	});
}

$("#logger_type_menu").children().click(function()
{
	$("#logger_type_menu").children().each(function()
	{
 	  $(this).removeClass("logger_type_menu_item_active");
      });
 	$(this).addClass("logger_type_menu_item_active");
 	var filter=$(this).attr("method");
});



function logcat_logger_clickhandler() {
	$(".logcat_logger_container ul li").click(function() 
	{
		if(!$(this).hasClass('logcat_logger_item_active'))
		{
			set_device_pageindex(0);
			$("#logcat_old_log").empty();
			$(".logcat_logger_item_active").removeClass("logcat_logger_item_active");
			$(this).addClass("logcat_logger_item_active");
			$("#logcat_last_day_log").show();
			var device_id=$(this).find("span").attr('id');
			recive_message("logcat_"+device_id);
		}
	});
	
}


function get_more_log()
{
   $("#logcat_last_day_log").click(function(){
	   var index=0;
	   var device_id="";
	   $(".logcat_logger_item_active").each(function(){
			var device_element=$(this).find('span');
			device_id=$(device_element).attr('id');
			index=$(device_element).attr('pageindex');
			$(device_element).attr('pageindex',parseInt(index)+1);
		});
	   $.post("/logcat/logger/more_bslog",{'index':index,'device_id':device_id},function(data,status){
		   if(data!="False")
			{
			   $("#logcat_old_log").prepend("<br/>"+data);
			}
		   else
			 {
			   $("#logcat_old_log").prepend("no more logs!</br>");
			 }
	   });
   });
}


function set_device_pageindex(index)
{
	$(".logcat_logger_item_active").each(function(){
		var device_element=$(this).find('span');
		$(device_element).attr('pageindex',index);
	});
}


function recive_message(channel_id)
   {
	var billboard = $('#logcat_logger_content');
	if(web_socket!=null)
	{
		   web_socket.close();
	}
	billboard.empty();
	var ws4redis = WS4Redis({
		uri : 'ws://'+window.location.host+'/ws/'+channel_id+'?subscribe-broadcast&publish-broadcast&echo',
		receive_message : receiveMessage,
		heartbeat_msg : "--heartbeat--",
	});
	web_socket=ws4redis;

	// receive a message though the Websocket from the server
	function receiveMessage(msg) {
		billboard.append('<br/>' + msg);
		var scrollbar_setting=$("#logcat_sbar_default_setting");
		if(scrollbar_setting.is(':checked'))
		{
			   $("#logger_content_show_box").scrollTop($("#logger_content_show_box")[0].scrollHeight);
		}	
		
	}
   }





});
