$(document).ready(function() {
//	init_board();
//	board_column_item_change_handler();
	function init_board()
	{
		 $(".web-board-column-item-container").jqxSortable({connectWith: ".web-board-column-item-container"});
		 var parent_height=$(".app-body-default").css("height");

		 $(".web-board-column-item-container").css("height",parent_height.replace("px","")+"px");
	}

    function board_column_item_change_handler()
    {
    	 $('.web-board-column-item-container').on('stop', function (e) {
    	     var trigger=e.currentTarget.id;
    	    	   $(".web-board-column-item-container").each(function(e){
    	    		   if($(this).attr('id')!=trigger)
    	    			   {
    	    			     var new_item_list=$(this).jqxSortable("toArray").sort();
    	    			     var old_item_list=column_status_map[($(this).attr('id'))];
    	    			     var result="0";
    	    			     if(old_item_list.length!=new_item_list.length)
    	    			    	 {
    	    			    	 var flag=false;
    	    			    	    for(i in new_item_list)
    	    			    	    	{
    	    			    	    	  console.log(new_item_list[i]);
    	    			    	    	  for(j in old_item_list)
    	    			    	    		{

    	    			    	    		  if(new_item_list[i]==old_item_list[j])
    	    			    	    			{
    	    			    	    			   flag=true;
    	    			    	    			   break;
    	    			    	    			}
    	    			    	    		  else
    	    			    	    			  {
    	    			    	    			   flag=false;
    	    			    	    			  }
    	    			    	    		}
    	    			    	    	   if(!flag)
    	       			    	    	{
    	       			    	    	  result=new_item_list[i];
    	       			    	    	  break;
    	       			    	    	}
    	    			    	    	}
    	    			    	    console.log("result is :"+result);
    	    			    	    console.log("column is :"+$(this).attr('id'));
    	    			    	 }
    	    			   }
    	    	   });
    	    	   set_column_status();
    	    	   $(".web-board-column-item-container").jqxSortable("cancel");

    	    });
    }



	var column_status_map={};
//    set_column_status();
    function set_column_status()
    {
    	$('.web-board-column-item-container').each(function(){
    		var column_id=$(this).attr('id');
    		column_status_map[column_id]=$("#"+column_id).jqxSortable("toArray").sort();
    	});
    }
});
