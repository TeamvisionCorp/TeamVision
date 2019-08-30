$(document).ready(function() {

	//加载默认任务列表以及操作
	loadtool("nga");

	//加载测试任务左导航项目
	$("#leftContainer").load("/toolbox/getleftnavigater", function(data, textstatus) {
		$("#lefttab li").click(function() {
			$("#lefttab li").removeClass("lefttabactive");
			$("#lefttab li").removeClass("lefttenabactive");
			$("#lefttab li").addClass("lefttabenactive");
			$(this).removeClass("lefttabenactive");
			$(this).addClass("lefttabactive");
			var listmethod = $(this).attr("method");
			var objectType = $(this).attr("name");
			loadtool(listmethod);
		});
	});

	// //加载对象列表容器
	function loadtool(listmethod) {
		//加载列表
		$("#toolcontainer").load("/toolbox/gettoolpage",{"toolname":listmethod},function(data,status){
		
		});
		
	}
	
	

});
