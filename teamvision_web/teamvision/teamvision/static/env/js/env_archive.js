$(document).ready(function() {
    var theme = 'bootstrap';
	var rootUri = window.location.href;
	var currentTrigger = null;
	var currentoPopObject = null;
	
	show_right_panel();
	init_webapp(); 
	load_archive_file();
	
	
	//展现右侧面板
	
	function show_right_panel()
	{
		$("#header-rightbar-filter").click(function(){
			$(".web-app-view-right-panel-default").toggle(500);
		});
	}
    
	function init_webapp()
	{
		 var parent_height=$(".web-app-view-body-default").css("height");
		 $(".web-app-view-content-default").css("height",parent_height.replace("px","")+"px");
		 $(".webapp_header_leftbar_nav").hide();
	}
	
	function load_archive_file()
	{
		$(".project_archive_folder").click(function(){
			var version_id=$(this).attr("version_id");
			var version_name=$("#folder_name").text();
			$("#project_archive_container").load("/project/1/archive/"+version_id,function(data,status){
				$(".webapp_header_leftbar_nav").show();
				$("#version_nav_bar").text(version_name);
				show_qrcode();
			});
		});
	}
	
	function show_qrcode()
	{
		$(".project_archive_folder_body").mouseover(function(){
			var qrcode_url=$(this).attr('qrcode_uri');
			  var img_src="/ci/history/download_package/qrcode?content="+qrcode_url;
			  var qr_code_container=$(this).find("img[name=qrcode_img]");
			  $(this).find("i[name=file_icon]").hide();
			  $(qr_code_container).attr('src',img_src);
			  $(qr_code_container).show();
			
		});
		$(".project_archive_folder").mouseout(function(){
			var qr_code_container=$(this).find("img[name=qrcode_img]");
			$(qr_code_container).hide();
			 $(this).find("i[name=file_icon]").show();
		});
	}

});
