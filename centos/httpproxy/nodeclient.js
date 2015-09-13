var net = require('net');
var sock = net.Socket();
var host = '0.0.0.0';
sock.connect(host, 9000, function () {

    console.log('CONNECTED TO: ' + host);
    client.write('I am Chuck Norris!');

});
