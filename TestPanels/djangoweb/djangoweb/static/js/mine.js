function checkuser1(id) {
    console.log(id);
    var user = document.getElementById(id).value;
    if(user == ""){
        alert("请输入内容");
    }
}