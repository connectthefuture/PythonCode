function getserver() {
    return "http://192.168.1.106:8000";
}

function xml2sql4ins(tabname, fieldnames, fieldlenghs, fieldinfo) {
    var sql = 'insert into ' + tabname + ' (' + fieldnames + ') values(';
    var array = split(fieldlenghs, ',');
    var tmp;
    for (var i = 0, j = 0; i < array.length; i++) {
        val = Number(array[i]);
        tmp = fieldinfo.substring(j, j + val).replace(new RegExp(/(')/g), '');
        sql += "'" + tmp + "'";
        if (i != array.length - 1) {
            sql += ",";
        }
        j += val;
    }
    sql += ");";
    console.log('hahaaaa');
    return sql;
}

function json2db(url, db) {
    var request = getserver() + url;
    console.log(request);
    var array4sql = Array();
    $.ajax({
        type: "get",
        async: false,
        url: request,
        dataType: "jsonp",
        jsonp: "callbackparam",//服务端用于接收callback调用的function名的参数
        jsonpCallback: "success_jsonpcallback",//callback的function名称
        success: function (json) {
            var defines = json['defines'];
            for (var key in defines) {
                var tabname = key.substr(6);
                var fields = defines['table_' + tabname]['fielddesc'];
//                            console.log(json['table'][tabname]);
                for (var idx in json['table'][tabname]) {
                    var fieldlen = json['table'][tabname][idx][0];
                    var fieldinfo = json['table'][tabname][idx][1];
                    var sql = xml2sql4ins(tabname, fields, fieldlen, fieldinfo);
                    array4sql[idx] = sql;
                }
            }
            db.transaction(
                function (tx) {
                    console.log(array4sql.length);
                    for (var k = 0; k < array4sql.length; k++) {
                        var sql = array4sql[k];
                        console.log(sql);
                        tx.executeSql(sql, [], function (tx, result) {

                        }, function (tx, error) {
                            console.log(error);
                        });
                    }
                },
                function (tx, error) {
                    console.log(error);
                },
                function (tx, result) {
                    console.log("success");
                }
            );
        },
        error: function () {
            alert('fail');
        }
    });
}