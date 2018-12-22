$(document).ready(function(){
    $("#message").text("Sent a request");
    var html;
    chrome.runtime.onMessage.addListener(function (request, sender){
		if (request.action === "html_send") {
			data_to_send = request.source;
			$.post("http://127.0.0.1:5000", data_to_send, function (received_data){
				$("#message").html("Received: " + received_data)
			});
		}
	});
    chrome.tabs.executeScript(null, {file: "GetChromePageHTML.js"}, null);	
});
