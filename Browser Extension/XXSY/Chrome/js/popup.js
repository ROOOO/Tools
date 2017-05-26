function httpRequest(url, callback){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            callback(xhr.responseText)
        }
    }
    xhr.send();
}
httpRequest('http://108.61.200.192/xxsy/', function (rst) {
	alert(rst)
     document.getElementById("ip_div").innerHTML = rst
})