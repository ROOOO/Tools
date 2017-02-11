var xxname = localStorage.xxname || 'blackList';
document.getElementById('xxname').value = xxname;
document.getElementById('save1').onclick = function(){
    localStorage.xxname = document.getElementById('xxname').value;
    alert('保存成功。');
}
var xxnotitime = localStorage.xxnotitime || 10;
document.getElementById('xxnotitime').value = xxnotitime;
document.getElementById('save2').onclick = function(){
    localStorage.xxnotitime = document.getElementById('xxnotitime').value;
    alert('保存成功。');
}
