$(document).ready(function() {
	
	init_web_app();
//	show_right_panel();
	//页面初始化配置
	function init_web_app()
	{
		$(".web-app-view-right-panel-default").height($(window).height()-110);
//		$(".web-app-view-body-default").height($(window).height()-120);
		$(".web-app-view-right-panel-default").hide();
	}
	
	
	//展现右侧面板
	
	function show_right_panel()
	{
		$("#fortesting-header-rightbar-filter").click(function(){
			$(".web-app-view-right-panel-default").toggle(500);
		});
	}

}); 