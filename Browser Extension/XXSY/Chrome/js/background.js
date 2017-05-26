function httpRequest(url, callback){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            var name = localStorage.xxname ? localStorage.xxname : '"blackList"';
            var reg = new RegExp(name, "g");
            var mat = xhr.responseText.match(reg);
            mat = mat ? mat.length : 0;
            callback(mat);
        }
    }
    xhr.send();
}

function setNum() {
    httpRequest('http://108.61.200.192/xxsy/', function(count){
        var color = count == 0 ? '#00FF00' : '#FF0000';
        var iconColor = count == 0 ? 'green.png' : 'red.png';
        chrome.browserAction.setIcon({path: {'19': 'images/'+iconColor}});
        chrome.browserAction.setIcon({path: {'38': 'images/'+iconColor}});
        chrome.browserAction.setBadgeBackgroundColor({color: color});
        chrome.browserAction.setBadgeText({text: count.toString()});
    });
    setTimeout(function(){setNum()}, 2000);
}

function notification() {
    httpRequest('http://108.61.200.192/xxsy/', function (count) {
        if (count != 0) {
            chrome.notifications.create("abc", { 
                type: "basic", 
                iconUrl: 'images/red.png', 
                title: 'Waring', 
                message: '小黑账 x' + count.toString()
                }, function() {}); 
        }
    });
    var time = localStorage.xxnotitime ? localStorage.xxnotitime : 10;
    setTimeout(function(){notification()}, time * 1000);
}

chrome.browserAction.onClicked.addListener(function(activeTab)
{
    // var newURL = "http://108.61.200.192/xxsy/";
    // chrome.tabs.create({ url: newURL });
});

function Init() {
    setNum()
    notification()
}
Init()
