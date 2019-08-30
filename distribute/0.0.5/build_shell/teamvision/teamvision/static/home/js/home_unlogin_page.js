$(document).ready(function() {

	//
	$("a[name=home_page_icon]").click(function() {
		$("#function-warning-dialog").modal('show');
	});

	$("#project_summary").click(function() {
		show_project_info_table();
		$(".home_project_summary_page").fadeIn(2000);
		$("#home_page_welcome").hide();
	});

	$("#home_welcome").click(function() {
		$(".home_project_summary_page").hide();
		$("#home_page_welcome").fadeIn(2000);
	});

	function show_project_info_table() {
		var url = "/project_json";
		// prepare the data
		var source = {
			datatype : "json",
			datafields : [{
				name : 'Project',
				type : 'string'
			}, {
				name : 'Platform',
				type : 'string'
			}, {
				name : 'Creator',
				type : 'string'
			}, {
				name : 'Product',
				type : 'string'
			}],
			url : url,
			pager : function(pagenum, pagesize, oldpagenum) {
				// callback called when a page or page size is changed.
			}
		};

		// prepare the data;
		var dataAdapter = new $.jqx.dataAdapter(source);
		$("#home_page_project_summary").jqxGrid({
			theme : 'metro',
			width : '60%',
			height : '768px',
			rowsheight : 40,
			source : source,
			selectionmode : 'none',
			sortable : true,
			pageable : true,
			autoheight : true,
			autoloadstate : false,
			autosavestate : false,
			autoshowfiltericon : true,
			columnsresize : true,
			columnsreorder : true,
			showfilterrow : true,
			filterable : true,
			filterrowheight : 35,
			columns : [{
				text : '项目名称',
				filtercondition : 'contains',
				datafield : 'Project',
				width : "50%"
			}, {
				text : '负责人',
				filtercondition : 'contains',
				datafield : 'Creator',
				width : "15%"
			}, {
				text : '项目平台',
				filtercondition : 'contains',
				datafield : 'Platform',
				width : "15%"
			}, {
				text : '产品线',
				filtercondition : 'contains',
				datafield : 'Product'
			}]
		});

	}


 load_device_view("all");
$("#home_page_device_menu").children().click(function()
{
	$("#home_page_device_menu").children().each(function(){
 	$(this).removeClass("device_info_menu_item_active");
    });
 	$(this).addClass("device_info_menu_item_active");
 	var filter=$(this).attr("method");
 	load_device_view(filter);
 });

function load_device_view(filter)
{
	$("#home_device_list_view").load("/home/device/filter",{"device_filter":filter},function(data,status)
{
	
});
}


});
