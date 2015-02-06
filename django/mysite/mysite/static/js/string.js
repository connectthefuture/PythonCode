function split(str, spliter){
    var array = new Array();
    var len = str.length;
    var idx0, idx1;
    for(var i = 0; i < len; ){
        idx1 = str.indexOf(spliter, i);
        if(idx1 == -1){
            break;
        }
        array.push(str.substring(idx0, idx1));
        i = idx1 + 1;
        idx0 = idx1 + 1;
    }
    if(idx1 < len){
        array.push(str.substr(idx1));
    }
    return array;
}

function rjust(str, N, ch) {
    var n = N - str.length;
    var tmp = str;
    for(var i = 0; i < n; i++) {
        tmp = ch + tmp;
    }
    return tmp;
}