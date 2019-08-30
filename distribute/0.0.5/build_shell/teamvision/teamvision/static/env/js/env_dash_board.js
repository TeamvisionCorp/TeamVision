$(document).ready(function() {
	var theme = 'metro';
	var rootUrl=window.location.href;
	
	
	add_more_activites();
	function add_more_activites()
	{
		$("#project_dashbaord_more_activites").click(function()
		{
			var activites_container=$("#project_dashbaord_activites");
			var start_index=activites_container.children().length;
			$.post(rootUrl+"more_activites",{"start_index":start_index},function(data,status)
			{
				if(data!="")
				{
				  activites_container.append(data);
				}			
			});
		});
	}
	

});
