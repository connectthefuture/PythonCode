(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return decodeURI(r[2]); return '';
    }
})(jQuery);

(function ($) {
    $.fn.movebg = function (options) {
        var defaults = {
            width: 120, /*移动块的大小*/
            extra: 5, /*反弹的距离*/
            speed: 300, /*块移动的速度*/
            rebound_speed: 100/*块反弹的速度*/
        };
        var defaultser = $.extend(defaults, options);
        return this.each(function () {
            var _this = $(this);
            var _item = _this.children("ul").children("li").children("a"); /*找到触发滑块滑动的元素	*/
            var origin = _this.children("ul").children("li.cur").index(); /*获得当前导航的索引*/
            var _mover = _this.find(".move-bg"); /*找到滑块*/
            var hidden; /*设置一个变量当html中没有规定cur时在鼠标移出导航后消失*/
            if (origin == -1) { origin = 0; hidden = "1" } else { _mover.show() }; /*如果没有定义cur,则默认从第一个滑动出来*/
            var cur = prev = origin; /*初始化当前的索引值等于上一个及初始值;*/
            var extra = defaultser.extra; /*声明一个变量表示额外滑动的距离*/
            _mover.css({ left: "" + defaultser.width * origin + "px" }); /*设置滑块当前显示的位置*/

            //设置鼠标经过事件
            _item.each(function (index, it) {
                $(it).mouseover(function () {
                    cur = index; /*对当前滑块值进行赋值*/
                    move();
                    prev = cur; /*滑动完成对上个滑块值进行赋值*/
                });
            });
            _this.mouseleave(function () {

                if (hidden == 1) { _mover.stop().hide(200); } /*当html中没有规定cur时在鼠标移出导航后消失*/
                else {
                    cur = origin; /*鼠标离开导航时当前滑动值等于最初滑块值*/
                    move();
                }
            });

            //滑动方法
            function move() {
                _mover.clearQueue();
                if (cur < prev) { extra = -Math.abs(defaultser.extra); } /*当当前值小于上个滑块值时，额外滑动值为负数*/
                else { extra = Math.abs(defaultser.extra) }; /*当当前值大于上个滑块值时，滑动值为正数*/
                _mover.queue(
				function () {
				    $(this).show().stop(true, true).animate({ left: "" + Number(cur * defaultser.width + extra) + "" }, defaultser.speed),
					function () { $(this).dequeue() }
				}
			);
                _mover.queue(
				function () {
				    $(this).stop(true, true).animate({ left: "" + cur * defaultser.width + "" }, defaultser.rebound_speed),
					function () { $(this).dequeue() }
				}
			);
            };
        })
    }
})(jQuery);

jQuery.fn.emptyText = function () {
    this.each(function () {
        var $this = $(this);
        tip = $this.attr("emptyText");
        if (tip != '') {
            if ($this.val() == '') {
                $this.val(tip);
                $this.css("color", "#999");
            }
            $this.focus(focus);
            $this.blur(blur);
        }
    });
}
function focus() {
    var $this = $(this);
    if ($this.val() == $this.attr("emptyText")) {
        $this.val('');
        $this.css("color", "#000");
    }
}
function blur() {
    var $this = $(this);
    if ($this.val() == '') {
        $this.val($this.attr("emptyText"));
        $this.css("color", "#999");
    }
}
var IsLogined = false;
var myid = 0;
var NickName = ""; 
function GetUserCookie() {
    var MyCookie = document.cookie.toLowerCase();
    re = /qingrenid=(\d+)&/g;
    if (re.test(MyCookie)) {
        IsLogined = true;
        myid = RegExp.$1;
        re2 = /nickname=([^&]+)/g;
        re2.test(MyCookie);
        NickName = unescape(RegExp.$1).replace("+", " ").replace("+", " "); 
    }
}
GetUserCookie();
var time1;
function usernotice() {
    $.post("/control/userres.ashx?q=" + Math.random(), function (data, status) {
        var r = $.parseJSON(data);
        r.letter > 0 ? $(".i_zlx").show().text(r.letter) : $(".i_zlx").hide();
        r.sayhi > 0 ? $(".i_dzh").show().text(r.sayhi) : $(".i_dzh").hide();
        r.look > 0 ? $(".i_kgw").show().text(r.look) : $(".i_kgw").hide();
        r.contact > 0 ? $(".i_lxw").show().text(r.contact) : $(".i_lxw").hide();
        r.hudong > 0 ? $(".i_hdtz").show().text(r.hudong) : $(".i_hdtz").hide();
        r.hongbao > 0 ? $(".i_hbtz").show().text(r.hongbao) : $(".i_hbtz").hide();
        r.yuehui > 0 ? $(".i_yhtz").show().text(r.yuehui) : $(".i_yhtz").hide();
        r.liwu > 0 ? $(".i_lwtz").show().text(r.liwu) : $(".i_lwtz").hide();
        r.system > 0 ? $(".i_xttz").show().text(r.system) : $(".i_xttz").hide();
        r.total > 0 ? $(".i_total").show().text(r.total) : $(".i_total").hide();
        if(time1!=null)clearInterval(timer1);
        if (r.total > 0) {
            time1 = setInterval(shanshan, 500);
        }
    });
}
function shanshan() {
    $("#t_msg").toggleClass("t_msg");
}
$(document).ready(function () {
    if (IsLogined) {
        $('#t_msg').mouseover(function () {
            $("#navuser").hide();
            $("#navmsg").show();
        });
        $('#t_user').mouseover(function () {
            $("#navmsg").hide();
            $("#navuser").show();
        });
        $('.ns').mouseleave(function () {
            $(this).hide();
        });
        usernotice();
        setInterval(usernotice, 30000);
    }
    else {
        $(".user_msg").hide();
        $(".nologin").show();
        $('.ns').hide();
    }
    $(function () {
        var href = window.location.href.toLowerCase();
        if (href.indexOf("myself") > 0) {
            $("#navBd li:eq(0)").addClass("cur");
        }
        else if (href.indexOf("yuehui") > 0) {
            $("#navBd li:eq(3)").addClass("cur");
        }
        else if (href.indexOf("article") > 0) {
            $("#navBd li:eq(4)").addClass("cur");
        }
        else if (href.indexOf("hongbao") > 0) {
            $("#navBd li:eq(5)").addClass("cur");
        }
        else if (href.indexOf("dynamic") > 0) {
            $("#navBd li:eq(6)").addClass("cur");
        }
        else if (href.indexOf("girl") > 0 || $.getUrlParam("sex") == "0") {
            $("#navBd li:eq(1)").addClass("cur");
        }
        else if (href.indexOf("man") > 0 || $.getUrlParam("sex") == "1") {
            $("#navBd li:eq(2)").addClass("cur");
        }
        $("#navBd").movebg();
    });
});