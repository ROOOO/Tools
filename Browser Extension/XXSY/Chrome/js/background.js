function httpRequest(url, callback){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            callback(xhr.responseText);
        }
    }
    xhr.send();
    // setTimeout(function(){httpRequest(url, callback)}, 2000);
}

var rst_div = document.getElementById('ip_div');
alert(localStorage.xxname)
// setInterval(function(){
    httpRequest('http://108.61.200.192:8080/xxsy/', function(responseText){
        rst_div.innerText = responseText;
    });
// }, 2000);
