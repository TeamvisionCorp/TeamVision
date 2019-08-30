$(document).ready(function() {
	var theme = 'metro';
    // left_navitem_mouserover();
	// left_nav_clickhandler();

	
	init_summary_docking();
	init_activity_height();
	
	function init_summary_docking()
	{
	  $('#dashboard_project_docking').jqxDocking({
				theme : theme,
				orientation : 'vertical',
				mode : 'docked',
				windowsOffset : 20,
				width : "100%",
				cookies: false
			});
	}
	
	
    function init_activity_height()
    {
     	var container_height=$(window).height()-110;
     	var container_width=$(window).width();
     	if(container_height)
     		{
     		  var height1=container_height;
     		$(".tab-content").css("max-height",(height1-210)+"px"); 
     		}
    }
	
	
	// init_activity_docking();
	
	function init_activity_docking()
	{
		$('#dashboard_activity_docking').jqxDocking({
				theme : theme,
				orientation : 'vertical',
				mode : 'docked',
				windowsOffset : 20,
				width : "100%"
			});
		$("#dashboard_activity_window").jqxWindow({maxHeight:"100000px",});	
	}

	add_more_activites();
	function add_more_activites()
	{
		$("#home_dashbaord_more_activites").click(function()
		{
			var active_tab_id=$(this).parent().parent().find("#project-activities").find("li[class=active]").find("a:eq(0)").attr("href");
			var activites_container_id=$(active_tab_id).find("div:eq(0)").attr("id");
			var activites_container=$("#"+activites_container_id);
			var start_index=activites_container.children().length;
			$.post("/home/dashboard/more_activites",{"start_index":start_index,"activity_type":active_tab_id},function(data,status)
			{
				if(data!="")
				{
				  activites_container.append(data);
				}			
			});
		});
	}

});
