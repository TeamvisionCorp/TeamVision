$(document).ready(function() 
{

var current_filter="all";

load_device_view("all");

$("#home_page_device_menu").children().click(function()
{
	$("#home_page_device_menu").children().each(function()
	{
 	  $(this).removeClass("device_info_menu_item_active");
      });
 	$(this).addClass("device_info_menu_item_active");
 	var filter=$(this).attr("method");
 	load_device_view(filter);
});
 
 


function load_device_view(filter)
{
	current_filter=filter;
	$("#home_device_list_view").load("/device/filter",{"device_filter":filter},function(data,status)
   {
	   borrow_device();
   });
}

function borrow_device()
{
	$("a[name=borrow_device]").click(function()
	{
	var device_id=$(this).parent().find("input[name=device_id]").val();
	$.post("/device/borrow",{"device_id":device_id},function(data,status)
	{
		if (data == "True") 
					{
						load_device_view(current_filter);
					} 
					else 
					{
						init_notification("error", data, false);
					}
	});
	});
}



});
