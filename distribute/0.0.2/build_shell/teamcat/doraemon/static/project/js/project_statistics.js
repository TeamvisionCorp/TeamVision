$(document).ready(function(){
    var theme = 'bootstrap';
	var rootUri = window.location.href;
	
	init_web_app();
	init_page();
	
	
	
	function init_page()
	{
		load_issue_by_people(0);
		createOpenedIssueToday(0);
		createOpenedIssueTotal(0);
		createVersionTotalIssue();
		createModuleIssueCount(0);
		createSeverityIssueCount(0);
		createCategoryIssueCount(0);
		createResolvedResultIssueCount(0);
		init_DropDownList("unresloved_chart_version",0,false);
        init_DropDownList("issuestatus_chart_version",0,false);
		init_DropDownList("opened_chart_version",0,false);
		init_DropDownList("total_chart_version",0,false);
		init_DropDownList("module_chart_version",0,false);
		init_DropDownList("severity_chart_version",0,false);
		init_DropDownList("category_chart_version",0,false);
		init_DropDownList("reslovedresult_chart_version",0,false);
		version_change_handler("opened_chart_version");
        version_change_handler("issuestatus_chart_version");
		version_change_handler("unresloved_chart_version");
		version_change_handler("total_chart_version");
		version_change_handler("module_chart_version");
		version_change_handler("severity_chart_version");
		version_change_handler("category_chart_version");
		version_change_handler("reslovedresult_chart_version");
	}
	
	
	function init_web_app()
	{
		var parent_height=$(".web-app-view-body-default").css("height");
		 $(".web-app-view-content-default").css("height",parent_height.replace("px","")+"px");
		 $(".webapp_header_leftbar_nav").hide();
	}
	
	
	
	
	function createOpenedIssueToday(version_id)
	{
		var project_id=$("#project_id").attr('projectid');
		 $.getJSON("/api/project/"+project_id+"/"+version_id+"/statistics/issue_trend_new",function(result){
			 createTrendLineChart(result.result,'container2');
		 });	
	}
	
	
	function createOpenedIssueTotal(version_id)
	{
		var project_id=$("#project_id").attr('projectid');
		 $.getJSON("/api/project/"+project_id+"/"+version_id+"/statistics/issue_trend_total",function(result){
			 createTrendLineChart(result.result,'container9');
		 });	
	}
	
	function createVersionTotalIssue()
	{
		var project_id=$("#project_id").attr('projectid');
		 $.getJSON("/api/project/"+project_id+"/statistics/version_total_issue",function(result){
			 console.log(result);
			 createColumnChart(result.result,'container4');
		 });	
	}
	
	
	function createModuleIssueCount(version_id)
	{
		var project_id=$("#project_id").attr('projectid');
		 $.getJSON("/api/project/"+project_id+"/"+version_id+"/statistics/issue_count_per_module",function(result){
			 createColumnChart(result.result,'container5');
		 });	
	}
	
	
	function createSeverityIssueCount(version_id)
	{
		var project_id=$("#project_id").attr('projectid');
		 $.getJSON("/api/project/"+project_id+"/"+version_id+"/statistics/issue_count_by_severity",function(result){
			 console.log(6);
			 console.log(result);
			 createPieChart(result.result,'container6');
		 });	
	}
	
	function createCategoryIssueCount(version_id)
	{
		var project_id=$("#project_id").attr('projectid');
		 $.getJSON("/api/project/"+project_id+"/"+version_id+"/statistics/issue_count_by_category",function(result){
	
			 createPieChart(result.result,'container8');
		 });	
	}
	
	function createResolvedResultIssueCount(version_id)
	{
		var project_id=$("#project_id").attr('projectid');
		 $.getJSON("/api/project/"+project_id+"/"+version_id+"/statistics/issue_count_by_resolveresult",function(result){
			 createPieChart(result.result,'container7');
		 });	
	}
	
	
	
	 
	 
	 //生成趋势线图
	 function createTrendLineChart(data,chart_container)
	 {
		 Highcharts.chart(chart_container, {
			    chart: {
			        type: data['chart_type']
			    },
			    title: {
			        text: data['chart_title']
			    },
			    subtitle: {
			        text: data['chart_sub_title']
			    },
			    xAxis: {
			        categories: data['xaxis']
			    },
			    yAxis: {
			        title: {
			           
			        }
			    },
			    plotOptions: {
			        line: {
			            dataLabels: {
			                enabled: true          // 开启数据标签
			            },
			            enableMouseTracking: true // 关闭鼠标跟踪，对应的提示框、点击事件会失效
			        }
			    },
			    series:data['series_data']
			});
 
		 
	 }
	 
	 
	 
	
	
	//生成简单柱状图
	 function createColumnChart(data,chart_container)
	 {
		    Highcharts.chart(chart_container,{
		        chart: {
		            type: data['chart_type']
		        },
		        title: {
		            text:data['chart_title']
		        },
		        subtitle: {
		            text:data['chart_sub_type']
		        },
		        xAxis: {
		            categories:data['xaxis'],
		            crosshair: true
		        },
		        yAxis: {
		            min: 0,
		            title: {
		                text: '问题数量 (个)'
		            }
		        },
		        tooltip: {
		            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
		            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
		            '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
		            footerFormat: '</table>',
		            shared: true,
		            useHTML: true
		        },
		        plotOptions: {
		            column: {
		                borderWidth: 0,
		                colorByPoint:true,
		            }
		        },
		        series:data['series_data']
		    });
	 }


	function load_status_issue_count(version_id)
	{
        var project_id=$("#project_id").attr('projectid');
        $("#status_chart_version").load("/project/"+project_id+"/version/"+version_id+"/statistics/issue_count_status");

	}
	
	
	function load_issue_by_people(version_id)
	{
		
		var project_id=$("#project_id").attr('projectid');
		 $.getJSON("/api/project/"+project_id+"/"+version_id+"/statistics/unclosed_issue",function(result){
		 var data=result.result;
		$('#container').highcharts({
	        chart: {
	            type: data["chart_type"]
	        },
	        title: {
	            text: data['chart_title']
	        },
	        xAxis: {
	            categories: data['xaxis']
	        },
	        yAxis: {
	            min: 0,
	            title: {
	                text: ''
	            },
	            stackLabels: {
	                enabled: true,
	                style: {
	                    fontWeight: 'bold',
	                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
	                }
	            }
	        },
	        legend: {
	            align: 'right',
	            x: -30,
	            verticalAlign: 'top',
	            y: 25,
	            floating: true,
	            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
	            borderColor: '#CCC',
	            borderWidth: 1,
	            shadow: false
	        },
	        tooltip: {
	            formatter: function () {
	                return '<b>' + this.x + '</b><br/>' +
	                    this.series.name + ': ' + this.y + '<br/>' +
	                    '总数: ' + this.point.stackTotal;
	            }
	        },
	        plotOptions: {
	            column: {
	                stacking: 'normal',
	                dataLabels: {
	                    enabled: true,
	                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
	                    style: {
	                        textShadow: '0 0 3px black'
	                    }
	                }
	            }
	        },
	        series:data['series_data']
	    });
		 });
	}



	
	

	//生成饼图
	function createPieChart(data,chart_container)
	{
		Highcharts.chart(chart_container,{
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text:data['chart_title']
        },
        tooltip: {
            headerFormat: '{series.name}<br>',
            pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            type: data['chart_type'],
            name: data['chart_title'],
            data: data['series_data']
        }]
    });
	}
	
	
	//version_change_handler
	
	function version_change_handler(controll_name)
	{
		$("#"+controll_name).on('change',function(event){
			var args = event.args;
		    if (args) {
		    var item = args.item;
		    var value = item.value;
		    reload_chart(controll_name,value);
		    }
		});
	}
	
	function reload_chart(controll_name,value)
	{
		switch(controll_name) {
        case 'issuestatus_chart_version':
            load_status_issue_count(value);
            break;
		case 'unresloved_chart_version':
			load_issue_by_people(value);
		    break;
		case 'opened_chart_version':
			createOpenedIssueToday(value);
		     break;
		case 'total_chart_version':
			createOpenedIssueTotal(value);
		    break;
		case 'module_chart_version':
			createModuleIssueCount(value);
			break;
		case 'severity_chart_version':
			createSeverityIssueCount(value);
		    break;
		case 'category_chart_version':
			createCategoryIssueCount(value);
			break;
		case 'reslovedresult_chart_version':
			createResolvedResultIssueCount(value);
			break;
		default:
			 break;
		}
	}
	
	
	/**********************************通用方法**************************************/
	
	//初始化下来列表
	function init_DropDownList(name,value,checkbox)
	{
		$("#"+name).jqxDropDownList({
			theme : theme,
			width : "150px",
			height : 22,
			checkboxes:checkbox,
			filterable:true,
		});
		if(value!=0){
			var item = $("#"+name).jqxDropDownList('getItemByValue',value);
			$("#"+name).jqxDropDownList('selectItem', item);
		}	
	}
	

	
	
	
});