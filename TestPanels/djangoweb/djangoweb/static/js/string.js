function split(str, spliter) {
    var array = new Array();
    var len = str.length;
    var idx0, idx1;
    for (var i = 0; i < len;) {
        idx1 = str.indexOf(spliter, i);
        if (idx1 == -1) {
            break;
        }
        array.push(str.substring(idx0, idx1));
        i = idx1 + 1;
        idx0 = idx1 + 1;
    }
    if (idx1 < len) {
        array.push(str.substr(idx1));
    }
    return array;
}

function rjust(str, N, ch) {
    var n = N - str.length;
    var tmp = str;
    for (var i = 0; i < n; i++) {
        tmp = ch + tmp;
    }
    return tmp;
}

function rtrim(str) {
    return str.replace(/(\s*$)/g, "");
}

function ltrim(str) {
    return str.replace(/(^\s*)/g, "");
}

function trim(str) {
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

function checkzh_cn(str) {
    var patrn = /[\u4E00-\u9FA5]|[\uFE30-\uFFA0]/gi;
    if (!patrn.exec(str)) {
        return false;
    } else {
        return true;
    }
}

function checknull(str) {
    if(trim(str) == ""){
        return true;
    }else{
        return false;
    }
}