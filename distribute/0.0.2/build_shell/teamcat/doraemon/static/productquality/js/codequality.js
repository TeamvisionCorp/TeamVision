$(document).ready(function() {

	loadcodequalitycontainer(0);
    loadleftbarcontainer();
	

    /* 加载chart 容器*/	
	function loadcodequalitycontainer(submitionid)
	{
		$("#codequalitycontainer").load("/pquality/codequality/getchart",{'submitionid':submitionid},function(data,status){
		   if(submitionid!=0)
		   {
		   load_code_line_chart(submitionid);
		   load_bug_counts_chart(submitionid);
		   load_bug_rate_chart(submitionid);
		   }
		});
	}
	
	
	/*加载代码行数图标*/
	function load_bug_counts_chart(submitionid)
	{
	  $.get("/pquality/codequality/getproductbugs",{'submitionid':submitionid},function(bugdata,status){
	  	var datalist=bugdata.split(";");
	  	var xaxixlabel=eval("(" +datalist[0]+ ")");
	  	var value=eval("(" +datalist[1]+ ")");
	  	$('#bugcountforeveryversion').highcharts({
	        chart: {
	            type: 'line'
	        },
	        title: {
	            text: '各版本bug趋势'
	        },
	        xAxis: {
	                categories:xaxixlabel
	        },
	        yAxis: {
	            title: {
	                text: 'Bug数量'
	            }
	        },
	        series:[{
	        	name:"",
	        	data:value
	        }],
	         credits:{
	         	       enabled:false
	        	    },
	         plotOptions:
	          {
	          	line:
	          	{
	          		color:'#fcaf17'
	          	}
	          }
	    });
	  });
	}
	
	/*加载代码行数图标*/
	function load_code_line_chart(submitionid)
	{
	  $.get("/pquality/codequality/getcodelines",{'submitionid':submitionid},function(codelines,status){
	  	var datalist=codelines.split(";");
	  	var xaxixlabel=eval("(" +datalist[0]+ ")");
	  	var value=eval("(" +datalist[1]+ ")");
	  	$('#codelinesforeveryone').highcharts({
	        chart: {
	            type: 'column'
	        },
	        title: {
	            text: '当前版本开发代码行数'
	        },
	        xAxis: {
	                categories:xaxixlabel
	        },
	        yAxis: {
	            title: {
	                text: '代码行数'
	            }
	        },
	        series:[{
	        	name:"",
	        	data:value
	        }],
	         credits:{
	         	       enabled:false
	        	    },
	          plotOptions:
	          {
	          	column:
	          	{
	          		color:'#1d953f'
	          	}
	          }
	    });
	  });
	}
	
	/*加载bug rate图表*/
	
	function load_bug_rate_chart(submitionid)
	{
	  $.get("/pquality/codequality/getproductbugrates",{'submitionid':submitionid},function(bugrates,status){
	  	var datalist=bugrates.split(";");
	  	var xaxixlabel=eval("(" +datalist[0]+ ")");
	  	var value=eval("(" +datalist[1]+ ")");
	  	$('#bugrates').highcharts({
	        chart: {
	            type: 'line'
	        },
	        title: {
	            text: '各版本bug率趋势'
	        },
	        xAxis: {
	                categories:xaxixlabel
	        },
	        yAxis: {
	            title: {
	                text: '千行bug数'
	            }
	        },
	        series:[{
	        	name:"",
	        	data:value
	        }],
	        credits:{
	        	      enabled:false
	        	    },
	        plotOptions:
	          {
	          	line:
	          	{
	          		color:'#ef4136'
	          	}
	          }
	    });
	  });
	}
	
	/*加载左边栏*/
	function loadleftbarcontainer()
	{
		$("#leftContainer").load("/pquality/codequality/loadleftcontainer",function(data,status)
		{
			loadfoldpanel();
			loadproductnamecontrol();
			loadproductversioncontrol(0,0);
			changeplatfrom();
			
	    });
	}
	
	/*加载折叠挑*/
	function loadfoldpanel()
	{
		var accordionContainer = $("#accordion");
			accordionContainer.accordion({
				collapsible : true
			},{ active: false }
			);
	}
	
	/*加载产品，以及版本下拉框*/
	function loadproductnamecontrol()
	{
		var platfromid = $("#id_productplatform").val().trim();
		$("#id_productname").load("/pquality/codequality/getproductnamecontrol",{'platformid':platfromid},function(data,status)
		{
			changeproductname();
		});
	}
	
	/*加载产品，以及版本下拉框*/
	function loadproductversioncontrol(productid,platfromid)
	{
		$("#id_productversion").load("/pquality/codequality/getproductversioncontrol",{'productid':productid,"platformid":platfromid},function(data,status){
			changeproductversion();
		});
	}
	
	
	function changeproductname() {
		$("#id_productname").change(function() {
		    var productid = $("#id_productname").val().trim();
	        var platfromid = $("#id_productplatform").val().trim();
			loadproductversioncontrol(productid,platfromid);
		});
	}
	
	function changeplatfrom()
	{
		$("#id_productplatform").change(function(){
	       loadproductnamecontrol();
		});
	}
	
	function changeproductversion() {
		$("#id_productversion").change(function() {
			var submitionid = $("#id_productversion").val().trim();
			loadcodequalitycontainer(submitionid);
		});
	}
	
	
	

});
