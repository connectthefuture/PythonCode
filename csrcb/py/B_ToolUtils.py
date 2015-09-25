# -*- coding:gbk -*-
'''
@文件名称:B_ToolUtils.py
@组件组:工具类组件
@组件级别:银行级
@作    者:zh
@创建时间:2015-01-14 09:35:23
@创建地点:常熟银行
@修订说明:[每修订一次则新增如下一行 @修订: 某人    某日    修改内容及原因说明(>多次修订时依次排开),其中@修订要空4个空格]
'''

from pyExcelerator import *
from AFALogger import AppLoggerChange;
from AFALogger import LoggerTrace;
from AFALogger import LoggerError;
from traceback import format_exc;
from P_Database import P_dml_sel
from P_Dict import P_dict_colume
from P_File import P_filedata_getconf
from B_Communition import B_NATPClient
import urllib, urlparse
import os

try:
    import cStringIO as StringIO
except:
    import StringIO

try:
    global DBConn
    DBConn = __import__("__DBC__")
except ImportError as e:
    DBConn = None
    raise e


def B_exceldata_crt(__REQ__, title, columns, rows, fileAP):
    '''
    @组件名称:创建excel报表
    @组件风格:判断型
    @组件类型:横向参数模块
    @中文注释:生成excel报表，引用第三方类库pyExcelerator(版本0.6.3a)
    @入参:
        @param    __REQ__           dict     传入交易上下文req
        @param    title             str      excel报表的标题
        @param    columnName        list     excel报表的列名
        @param    fileData          list     生成excel的源数据
        @param    fileAP            str      excel报表保存的路径
    @出参:
    @返回状态:
        @return    0    失败
        @return    1    成功
    @作    者:ZH
    @创建时间:
    @使用范例: @A_GJS_exceldata_crt(__REQ__, "20031371班学生表",['学号','姓名','班级'], [['01','张三','20031371'],['02','李四','20031371']] , '/home/afa/temp/stu.xls')

    '''
    try:
        w = Workbook()
        ws = w.add_sheet(title.decode('gb18030'))

        for i, col in enumerate(columns):
            ws.write(0, i, col.decode("gb18030"))
        for y, row in enumerate(rows):
            for x in xrange(len(columns)):
                ws.write(y + 1, x, "" if row[x] is None or row[x] == "" else str(row[x]).decode("gb18030"))
        w.save(fileAP)
        return [1, None, None, None];
    except Exception, e:
        return [0, 'A01F022', '生成报表失败' + str(e)]


def B_CallTradeEx(__REQ__, __RSP__, MC, TC, logmode, callmethod):
    '''
    @组件名称: 参数化子交易调用
    @组件风格: 选择型
    @组件类型: 横向参数模块
    @中文注释: 执行子交易, 对于同步调用可以指定子交易是否是用新日志, 同时可以指定交易是否异步还是同步调用, 对于同步可以按照接口调用也可以共享全局容器调用
    @入参:
        @param    __REQ__    dict    输入容器
        @param    __RSP__    dict    输出容器
        @param    MC         str     子交易应用代码
        @param    TC         str     子交易交易代码
        @param    logmode    str     日志模式(1-共享主交易, 2-子交易单独创建)
        @param    callmethod str     调用方式(0-同步py调用,  2-异步py调用)
    @出参:
    @返回状态
        @return    0    调用失败
        @return    1    调用成功
        @return    2    调用异常(已执行完后出现异常)
    @作    者: 洪楷城
    @创建时间: 2015-2-9 09:21:07
    @使用范例:
    '''
    FLG = 0;
    Curlogname = None;
    Prevlogname = None;
    oldMC = None;
    oldTC = None;
    try:
        if ((type(__REQ__) is not dict ) or (type(__RSP__) is not dict)):
            return [0, "CTX001", "入参 __REQ__ or  __RSP__ 不合法", [None]];
        if ((type(MC) is not str ) or (type(TC) is not str)):
            return [0, "CTX001", "入参 MC or  TC 不合法", [None]];
        if ((type(logmode) is not str ) or (type(callmethod) is not str)):
            return [0, "CTX001", "入参 logmode or callmethod 不合法", [None]];

        # 防止交易调度自身加特殊判断
        if __REQ__["__MC__"] == MC and __REQ__["__TC__"] == TC:
            return [0, "UPC001", "交易调度时不可自身调用自身" + TC, [None]];

        # 子交易调度不可嵌套,最多只能子交易调度一次,如果有__subcall_dept__则说明是子交易了,不允许后续再进行调度子交易
        # if __REQ__.has_key("__subcall_dept__"):
        # return [0,"UPC001", "子交易不可调度其他交易" + TC, [None]];

        # 子交易的MC和TC替换
        oldMC = __REQ__["__MC__"];
        oldTC = __REQ__["__TC__"];
        __REQ__["__MC__"] = MC;
        __REQ__["__TC__"] = TC;
        __REQ__["templatecode"] = MC;
        __REQ__["transcode"] = TC;

        if callmethod == "0":  # 同步py调用
            _ModuleName_ = "T" + MC + "_" + TC;
            _EntryName_ = 'M' + TC + "_ENTRY";

            _Module_ = __import__(_ModuleName_);
            _Method_ = getattr(_Module_, _EntryName_);

            if logmode == "2":  # 子交易单独创建
                ret = AppLoggerChange(MC, TC, "");  # 日志改名称
                if (ret[0] != 0):
                    return [0, "CTX002", "日志名称修改为子交易名称时失败," + ret[1] + ret[2]];
                FLG = 1;
                Prevlogname = ret[3][0];
                Curlogname = ret[3][1];
                __REQ__["__LOG__"] = Curlogname;
                LoggerTrace("AppLoggerChange BEGIN:" + Curlogname + ":" + Prevlogname);

            ret = _Method_(__REQ__, __RSP__);
            FLG = 2;

            __REQ__["__MC__"] = oldMC;
            __REQ__["__TC__"] = oldTC;

            if logmode == "2":  # 子交易单独创建
                LoggerTrace("AppLoggerChange END:" + Prevlogname);
                ret2 = AppLoggerChange(oldMC, oldTC, "");
                if (ret2[0] != 0):
                    LoggerError("日志名称修改回原日志名称时失败," + ret[1] + ret[2]);
                __REQ__["__LOG__"] = Curlogname;

                FLG = 3;
            if (ret == True):
                return [1, None, None];
            else:
                return [2, "CTX003", "子交易调用返回值非True"];
        elif callmethod == "2":  # 异步py调用
            __RSP__["__ASYNC__"] = True;
            __RSP__["__AMC__"] = MC;
            __RSP__["__ATC__"] = TC;
            return [1, None, None];
        else:
            return [0, "CTX002", "不支持的调用方式,暂只支持同步py调用", [None]];
    except Exception, e:
        LoggerError(str(format_exc()));
        if logmode == "2":  # 子交易单独创建
            if (FLG >= 1 and FLG < 3 and Prevlogname != None):  # 日志名称更换回原名称
                AppLoggerChange(oldMC, oldTC, "");
                __REQ__["__LOG__"] = Curlogname;

        return [0, "EXPT00", str(e), None];
    finally:
        if oldMC != None:
            __REQ__["__MC__"] = oldMC;
            __REQ__["__TC__"] = oldTC;


def travelquery(req, lst):
    '''
            作用： 处理复杂查询函数
            作者：  ZH
    '''
    if type(lst[0]) is list or type(lst[0]) is tuple:
        yield '('
        for x in lst:
            for y in travelquery(req, x):
                yield y
        yield ')'
    else:
        if type(lst) is list or type(lst) is tuple:
            if len(lst) == 4:
                field = lst[3]
            else:
                field = lst[0]
            if req.get(field, ""):
                if type(lst[2]) is str:
                    if lst[1].find('is') >= 0 or lst[1].find('in') >= 0:
                        yield "(%s %s %s)" % (lst[0], lst[1], lst[2])
                    else:
                        yield "(%s %s '%s')" % (lst[0], lst[1], lst[2])
                else:
                    yield "(%s %s %s)" % (lst[0], lst[1], lst[2])
            else:
                yield '(1 = 1)'
        else:
            yield ' %s ' % lst


def PageSelect(_req_, _rsp_, sql, wherelist, pageinfo):
    '''
    @组件名称: 分页查询组件
    @组件风格: 处理型
    @组件类型: 横向参数模块
    @中文注释: 分页查询组件
    @入参:
        @param  __REQ__     dict 请求容器
        @param  __RSP__     dict 返回容器
        @param  sql         str  sql语句
        @param  wherelist   list where字段列表
        @param  pageinfo    dict 分页信息字典
    @出参:
        @param where str where条件
    @返回状态:
        @return 0  失败
        @return 1  成功
        @return 2  异常
    @作    者: ZH
    @创建时间: 2015-02-05
    @使用范例:
    '''
    try:
        DBCursor = None
        if ( DBConn == None ):
            return [0, 'A017059', '数据库连接对象为空,无数据库连接', [None]]
        pageindex = int(pageinfo['pageindex'])
        pagerownum = int(pageinfo['pagerownum'])
        sql = sql.lower().lstrip()
        cio = StringIO.StringIO()
        pagesql = "where rowno > %d fetch first %d rows only" % ((pageindex - 1) * pagerownum, pagerownum)
        if sql[-1] != ' ':
            sql += ' '
        if wherelist:
            for i in travelquery(_req_, wherelist):
                cio.write(i)
            tmp = cio.getvalue()
            while 1:
                if tmp.find("and (1 = 1)") >= 0:
                    tmp = tmp.replace("and (1 = 1)", "")
                else:
                    break
            while 1:
                if tmp.find("or (1 = 1)") >= 0:
                    tmp = tmp.replace("or (1 = 1)", "")
                else:
                    break
            # sql = '%s where %s' % (sql, tmp)
            bracket = sql.rfind(')')
            sql = sql[:bracket] + ' where %s' % tmp + sql[bracket:]
        else:
            pass
        wherepos = sql.find(' from ')
        countsql = "select count(*) %s" % ( sql[wherepos:])
        LoggerTrace("汇总查询语句为[%s]" % countsql)
        result = P_dml_sel(countsql, 0)
        if result[0] == 0:
            return [0, result[1], result[2], [None]]
        elif result[0] == 2:
            return [2, "999998", "无满足条件的记录！", [None]]
        totalrownum = result[3][1][0][0]
        m, n = divmod(totalrownum, pagerownum)
        if n > 0:
            totalpagenum = m + 1
        else:
            totalpagenum = m
        querysql = "%s %s" % (sql, pagesql)
        LoggerTrace("结果查询语句为[%s]" % querysql)
        DBCursor = DBConn.cursor()
        DBCursor.execute(querysql)
        result = DBCursor.fetchall()
        if not result:
            return [2, "999998", "无满足条件的记录！", [None]]
        cols = [row[0].lower() for row in DBCursor.description]
        LoggerTrace(str(cols))
        P_dict_colume(cols, result, _rsp_)
        _req_['totalrownum'] = totalrownum
        _req_['pagerownum'] = len(result)
        _req_['totalpagenum'] = totalpagenum
        return [1, None, None, [None]]
    except Exception as e:
        LoggerError(format_exc())
        return [0, "999996", str(e), [None]]
    finally:
        if DBCursor:
            DBCursor.close()
            DBCursor = None


def SelectRows(sql, onlyone=1, _rsp_=None):
    '''
    @组件名称: 数据查询
    @组件风格: 选择型
    @组件类型: 横向参数模块
    @中文注释: 根据sql查询语句获取查询的数据返回一个字典
    @入参:
        @param sql          str  查询sql语句
        @param onlyone      int  是否只查询单笔
    @出参:
        @param result       dict 查询返回数据
    @返回状态:
        @return 0 失败,数据库异常
        @return 1 成功
        @return 2 无满足条件记录
    @作    者: ZH
    @创建时间: 2015-3-20
    @使用范例:
    '''
    global sqlErrMsg
    sqlErrMsg = ''
    DBCursor = None

    try:
        DBCursor = DBConn.cursor()
        if ( DBCursor == None ):
            return [0, 'A017060', '数据库异常,获取操作游标时返回空', [None]]

        DBCursor.execute(sql)
        _Result_ = DBCursor.fetchall()
        if len(_Result_) == 0:
            return [2, 'A017061', '无满足条件记录', [None]]
        if onlyone:
            tmp = ["" if i is None else i for i in _Result_[0]]
            if _rsp_ is None:
                d = dict(zip([row[0].lower() for row in DBCursor.description], tmp))
            else:
                d = _rsp_
                for i, j in enumerate([row[0].lower() for row in DBCursor.description]):
                    d[j] = "" if tmp[i] is None else tmp[i]
        else:
            if _rsp_ is None:
                d = dict()
            else:
                d = _rsp_
            # x = zip(*_Result_)
            for i, j in enumerate([row[0].lower() for row in DBCursor.description]):
                d[j] = ["" if _Result_[k][i] is None else _Result_[k][i] for k in xrange(len(_Result_))]
        if _rsp_ is None:
            return [1, None, None, [d]]
        else:
            return [1, None, None, [None]]
    except Exception as e:
        LoggerError(str(format_exc()))
        return [0, 'A017100', '数据库异常,' + str(e), [None]]
    finally:
        if DBCursor != None:
            DBCursor.close()
            DBCursor = None


def B_Checkorgan(organo):
    '''
        @组件名称: 组织机构代码校验
        @组件风格: 判断型
        @组件类型: 横向参数模块
        @中文注释: 校验组织机构代码,证号为XXXXXXXX-X，00000000-0直接通过
        @入参:
            @param  organo        str 数据容器
        @出参:
            @param  errorcode     str 处理码
            @param  errormsg　　  str 处理信息
        @返回状态:
            @return 0  失败
            @return 1  成功
        @作    者: 洪楷城
        @创建时间: 2015年3月25日
        @使用范例:
    '''
    try:
        if (organo in ['XXXXXXXX-X', '00000000-0']):
            errorcode = '000000';
            errormsg = '组织结构代码校验完成';
            return [1, None, None, [errorcode, errormsg]];

        if (len(organo) != 10):
            errorcode = 'CKFAL01';
            errormsg = '组织结构代码格式不符,长度必须是10';
            return [0, None, None, [errorcode, errormsg]];
        chkno = organo[0:8];
        if (organo[-2] != '-'):
            errorcode = 'CKFAL01';
            errormsg = "组织结构代码格式不符,倒数第二位是'-'";
            return [0, None, None, [errorcode, errormsg]];
        chklst = list(chkno);
        ai = [];
        si = ['3', '7', '9', '10', '5', '8', '4', '2'];
        for i, j in enumerate(chklst):
            if (ord(j) >= 48 and ord(j) <= 57):  # 数字取本身
                ai.append(j);
            elif (ord(j) >= 65 and ord(j) <= 90):  # 大写子母取16进制编码整数
                ai.append(j.encode('hex'));
            else:
                errorcode = 'CKFAL02';
                errormsg = '组织结构代码是数字或大写字母';
                return [0, None, None, [errorcode, errormsg]];
        # 计算差值 10对应校验值11 11对应校验值0 其他为对应差值
        wi = {'10': 'X', '11': '0'};
        checkvalue = abs(11 - reduce((lambda x, y: x + y), map(lambda x, y: int(x) * int(y), ai, si)) % 11);
        LoggerTrace("校验值应为:" + str({'10': 'X', '11': '0'}.get(str(checkvalue), str(checkvalue))));
        if (str(checkvalue) in wi):
            if (wi[str(checkvalue)] == organo[-1]):
                errorcode = '000000';
                errormsg = '校验成功';
                return [1, None, None, [errorcode, errormsg]];
            else:
                errorcode = 'CKFAL03';
                errormsg = '校验不通过';
                return [0, None, None, [errorcode, errormsg]];
        elif (str(checkvalue) == organo[-1]):
            errorcode = '000000';
            errormsg = '校验成功';
            return [1, None, None, [errorcode, errormsg]];
        else:
            errorcode = 'CKFAL03';
            errormsg = '校验不通过';
            return [0, None, None, [errorcode, errormsg]];


    except Exception, e:
        LoggerError("------------------>校验组织机构代码异常" + str(format_exc()));
        errorcode = 'CKFAL00';
        errormsg = '校验组织机构代码异常';
        return [0, 'CKFAL00', '校验组织机构代码异常' + str(e), [errorcode, errormsg]]


def SFTP2Internet(__REQ__, method, host, port, user, password, filename, remotepath, afadir, afasubdir, ):
    '''
        @组件名称: 上传下载文件到互联网SFTP服务器
        @组件风格: 判断型
        @组件类型: 横向参数模块
        @中文注释: 上传下载文件到互联网SFTP服务器
        @入参:
            @param  __REQ__     dict 请求容器
            @param  method      str  上传下载 GET：下载 PUT：上传
            @param  host        str  SFTP服务器地址
            @param  port        str  SFTP服务器端口
            @param  user        str  SFTP用户名
            @param  password    str  SFTP用户码
            @param  filename    str  文件名
            @param  remotepath  str  SFTP路径
            @param  afadir      str  本地sysid
            @param  afasubdir   str  本地子路径
        @出参:
        @返回状态:
            @return 0  失败
            @return 1  成功
        @作    者: Z.H.
        @创建时间: 2015年9月9日
        @使用范例:
    '''
    try:
        tmp = dict()
        result = P_filedata_getconf(tmp, ["file_comm.conf", None],
                                    [["FTP2PART3", 'IP', 'CFG.IP', None], ["FTP2PART3", 'PORT', 'CFG.PORT', None],
                                     ["FTP2PART3", 'TIMEOUT', 'CFG.TIMEOUT', None]])
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        requesturl = urllib.urlencode(
            {"host": host, "user": user, "password": password, "filename": filename, "sysid": afadir,
             "subdir": afasubdir,
             "remote": remotepath, "port": str(port), "method": method.lower()})
        AFE_REQ = dict()
        AFE_REQ["ftptype"] = "rsftp"
        AFE_REQ["requesturl"] = requesturl
        result = B_NATPClient(AFE_REQ, tmp["__MC__"], "rsftp", "", tmp["CFG.IP"],
                              int(tmp["CFG.PORT"]), int(tmp["CFG.TIMEOUT"]))
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        filepath = "%s/workspace/fdir/%s%s/%s" % (
            os.getenv("HOME"), afadir, "/" + afasubdir if afasubdir else "", filename)
        if not os.path.exists(filepath):
            return [0, "A90981", "传输文件失败", [None]]
        return [1, None, None, [None]]
    except Exception as e:
        return [0, "A90982", [str(e)], [None]]