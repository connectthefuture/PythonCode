var arr = new Array();
arr[0] = "0";
arr[1] = "1";

var a = [1, 2, 3, 4];
a.shift();
console.log(a);
a.push(5);
console.log(a);
console.log(a.pop());
console.log(a);
console.log(a.indexOf(2));
console.log(a.join(","));
console.log(a.reverse());
person = new Object();
person.firstname = "Bill";
person.lastname = "Gates";
person.age = 56;
person.eyecolor = "blue";
console.log(person.age);

function One(name, sex) {
    this.name = name;
    this.sex = sex;
    this.getName = function () {
        return this.name;
    }
}
One.Show = function () {
    return "Show";
}
One.prototype.IntroduceChinese = function () {
    return "我的名字是" + this.name;
}

o = new One('a', 'female');
console.log(o.getName());
console.log(One.Show());
console.log(o.IntroduceChinese())

function baseClass() {
    this.showMsg = function () {
        console.log("baseClass::showMsg");
    }
}

function extendClass() {
    this.showMsg = function () {
        console.log("extendClass::showMsg");
    }
}

extendClass.prototype = new baseClass();
var baseinstance = new baseClass();
var instance = new extendClass();
instance.showMsg(); // 显示baseClass::showMsg
new baseClass().showMsg.call(instance);
var jsontext = '{"firstname":"Jesper","surname":"Aaberg","phone":["555-0100","555-0120"]}';
var contact = JSON.parse(jsontext);
    var json = JSON.stringify(contact);
console.log(contact);
console.log(typeof(json));
console.log(contact['firstname']);