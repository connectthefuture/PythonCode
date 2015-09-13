/**
 * Created by libra on 2015/9/13.
 */
console.log('abc');
var net = require('net');
net.createServer(function (src) {// new connection
    var des = new net.Socket();
    des.connect("127.0.0.1", 9000, function(err) {
        console.log(err);
    });
    des.on('error', function (err) {
        console.log(err)
    })

    src.on('data', function (chunk) {
        des.write(chunk);
    })
    des.on('data', function(chunk){
        src.write(chunk);
    })
    des.on('end', function(){
        console.log('des ended');
    })
}).listen(4000);