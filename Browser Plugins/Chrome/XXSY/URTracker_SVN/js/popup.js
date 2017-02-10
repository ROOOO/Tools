var notification = chrome.notifications.create("abc", { 
type: "basic", 
iconUrl: 'images/offline.png', 
title: 'Notification Demo', 
message: 'Merry Christmas' 
}, function() 

setTimeout(function() { 
notification()
}, 1); 

{}); 

setTimeout(function() { 
chrome.notifications.clear("abc", function() {}); 
}, 5000); 