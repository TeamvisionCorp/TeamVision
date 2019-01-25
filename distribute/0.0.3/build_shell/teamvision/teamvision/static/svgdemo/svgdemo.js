$(document).ready(function(){
      
   // $("svg>use").hide();
   // $("svg>line").hide();
   // $("svg>text").hide();
   $("#firstdemo").click(function(){
   	
   	 $("use[class=secondchild]").toggle();
   	 $("use[class=thirdchild]").toggle();
   $("line[class=secondline]").toggle();
   $("line[class=thirdline]").toggle();
   });
   
   $("#second").click(function(){
   	
   	 $("use[class=thirdchild]").toggle();
   $("line[class=thirdline]").toggle();
   });
   
});
