$(document).ready(function() {

	loadbugreportcontainer(0);
    loadleftbarcontainer();
	

    /* 加载chart 容器*/	
	function loadbugreportcontainer(submitionid)
	{
		$("#bugreportcontainer").load("/pquality/bugreport/getchart",{'submitionid':submitionid},function(data,status)
		{
		   load_perday_bug_counts_chart(submitionid);
		   load_allbugscounts_chart(submitionid);
		});
	}
	
	
	/*加载每日新开，以及修复的bug数图表*/
	function load_perday_bug_counts_chart(submitionid)
	{
		$.get("/pquality/bugreport/getbugcountsperday",{'submitionid':submitionid},function(bugdata,status)
		{
			
	  	var datalist=bugdata.split(";");
	  	var xaxixlabel=eval("(" +datalist[0]+ ")");
	  	var value1=eval("(" +datalist[1]+ ")");
	  	var value2=eval("(" +datalist[2]+ ")");
	  	var value3=eval("(" +datalist[3]+ ")");
	  	$('#openedfixedbugperday').highcharts(
	  		{
	  		 chart:
	  		 {
	  		 	type:'column'
	  		 },	  		
	        title: {
            text: '每日新增，修复bug数',
            x: -20 //center
            },
        subtitle: {
            text: '',
            x: -20
        },
        colors: ['#1d953f','#f7a35c', '#8085e9', '#f15c80', '#e4d354', '#8085e8', '#8d4653', '#91e8e1'],
        xAxis: {
            categories:xaxixlabel,
            labels: {
                rotation: 70
            },
            tickInterval:2
        },
        yAxis: {
            title: {
                text: 'Bug 数目'
            },
            min:0,
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '个'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
                 credits:{
	         	       enabled:false
	        	    },
	            plotOptions:
	          {
	          	line:
	          	{
	          		lineWidth:3
	          	}
	          },
        series: [{
            name: 'Opened',
            data: value1
        }, {
            name: 'Resolved',
            data: value2,
            type:'line'
        },
        {
            name: 'Closed',
            data: value3,
            type:'line'
        }
        ]
	    });
	});
	}
	
	/*加载累计提交，以及修复的bug数量图表*/
	function load_allbugscounts_chart(submitionid)
	{
	  $.get("/pquality/bugreport/getalldaybugcounts",{'submitionid':submitionid},function(bugdata,status){
	  	var datalist=bugdata.split(";");
	  	var xaxixlabel=eval("(" +datalist[0]+ ")");
	  	var value1=eval("(" +datalist[1]+ ")");
	  	var value2=eval("(" +datalist[2]+ ")");
	  	var value3=eval("(" +datalist[3]+ ")");
	  	$('#allopenedfixedbug').highcharts({
        title: {
            text: '累计提交，修复bug数',
            x: -20 //center
        },
        subtitle: {
            text: '',
            x: -20
        },
        colors: ['#1d953f','#f7a35c', '#8085e9', '#f15c80', '#e4d354', '#8085e8', '#8d4653', '#91e8e1'],
        xAxis: {
            categories:xaxixlabel
            ,
            labels: {
                rotation: 70
            },
            tickInterval:2
        },
        yAxis: {
            title: {
                text: 'Bug 数目'
            },
            min:0,
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '个'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
                 credits:{
	         	       enabled:false
	        	    },
	            plotOptions:
	          {
	          	line:
	          	{
	          		lineWidth:3
	          	}
	          },
        series: [{
            name: 'Opened',
            data: value1
        }, {
            name: 'Resoloved',
            data:value2
        },
        {
            name: 'Closed',
            data:value3
        }]
       });
	  });
	}
	
	
	
	/*加载左边栏*/
	function loadleftbarcontainer()
	{
		$("#leftContainer").load("/pquality/bugreport/loadleftcontainer",function(data,status)
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
		$("#id_productname").load("/pquality/bugreport/getproductnamecontrol",{'platformid':platfromid},function(data,status)
		{
			changeproductname();
		});
	}
	
	/*加载产品，以及版本下拉框*/
	function loadproductversioncontrol(productid,platfromid)
	{
		$("#id_productversion").load("/pquality/bugreport/getproductversioncontrol",{'productid':productid,"platformid":platfromid},function(data,status){
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
			loadbugreportcontainer(submitionid);
		});
	}
	
	

});
