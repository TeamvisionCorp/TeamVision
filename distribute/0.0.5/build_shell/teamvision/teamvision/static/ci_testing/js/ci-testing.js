$(document).ready(function(){
	
	default_select_history();
	click_history_item();
	click_analytics_item();
	
	//默认选中第一条历史记录
	function default_select_history()
	{
		var first_history_row=$("#ci_testing_history_container").find(".ci_testing_history_row")[0];
		$(first_history_row).addClass("testing_history_selected");
	}
	
	//选择历史记录
	function click_history_item()
	{
	
		$(".ci_testing_history_row").click(function()
				{   
					var history_id=$(this).find("input[name=task_history_id]").val();
					$(".testing_history_selected").removeClass("testing_history_selected");
					$("#auto_testing_caseresult_export").attr('href','/ci/testing/'+history_id+"/caseresult/export");
					$(this).addClass("testing_history_selected");
					$("#task_history_staticts_container").load("/ci/testing/result/"+history_id+"/analytics",function(){
						click_analytics_item();
					});
					$("#ci_testing_caseresult_container").load("/ci/testing/result/"+history_id+"/caseresult/0");
					
				});
	}
	//根据分析结果过滤 详细结果
	function click_analytics_item()
	{
		$(".ci_testing_history_analytics").click(function()
				{   
					var history_id=$("#analytics_auto_task_history_id").val();
					var result_type=$(this).attr("result_type");
//					$(".testing_history_selected").removeClass("testing_history_selected");
//					$(this).addClass("testing_history_selected");
					$("#ci_testing_caseresult_container").load("/ci/testing/result/"+history_id+"/caseresult/"+result_type);
					
				});
	}
	
	
});