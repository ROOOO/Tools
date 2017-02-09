var xxname = localStorage.xxname || 'all';
document.getElementById('xxname').value = xxname;
document.getElementById('save').onclick = function(){
    localStorage.xxname = document.getElementById('xxname').value;
    alert('保存成功。');
}