$(document).ready(function() {
	var theme = 'metro';
	var currentUri=window.location.href;
     submit_login_form();
    
	
	
	function submit_login_form() {
		$("#user_login_button").click(function() {
				$.post("/user/login", $('#user_login_form').serialize(), function(data, status) {
					if (data =="") 
					{
					} else 
					{
						init_notification("error", data, true);
					}
				});
		});
	}
	
	function init_notification(template, data, autoclose) {
		$("#operation_notification").jqxNotification({
			width : 250,
			// position : "bottom-right",
			opacity : 0.8,
			autoOpen : false,
			animationOpenDelay : 300,
			autoClose : autoclose,
			template : template,
			appendContainer: "#notification_container",
		});
		$("#operation_notification_message").empty();
		$("#operation_notification_message").append(data);
		$("#operation_notification").jqxNotification("open");
	}
	

});
