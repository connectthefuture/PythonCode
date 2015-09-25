# -*- coding:gbk -*-
'''
@�ļ�����:B_ToolUtils.py
@�����:���������
@�������:���м�
@��    ��:zh
@����ʱ��:2015-01-14 09:35:23
@�����ص�:��������
@�޶�˵��:[ÿ�޶�һ������������һ�� @�޶�: ĳ��    ĳ��    �޸����ݼ�ԭ��˵��(>����޶�ʱ�����ſ�),����@�޶�Ҫ��4���ո�]
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
    @�������:����excel����
    @������:�ж���
    @�������:�������ģ��
    @����ע��:����excel�������õ��������pyExcelerator(�汾0.6.3a)
    @���:
        @param    __REQ__           dict     ���뽻��������req
        @param    title             str      excel����ı���
        @param    columnName        list     excel���������
        @param    fileData          list     ����excel��Դ����
        @param    fileAP            str      excel�������·��
    @����:
    @����״̬:
        @return    0    ʧ��
        @return    1    �ɹ�
    @��    ��:ZH
    @����ʱ��:
    @ʹ�÷���: @A_GJS_exceldata_crt(__REQ__, "20031371��ѧ����",['ѧ��','����','�༶'], [['01','����','20031371'],['02','����','20031371']] , '/home/afa/temp/stu.xls')

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
        return [0, 'A01F022', '���ɱ���ʧ��' + str(e)]


def B_CallTradeEx(__REQ__, __RSP__, MC, TC, logmode, callmethod):
    '''
    @�������: �������ӽ��׵���
    @������: ѡ����
    @�������: �������ģ��
    @����ע��: ִ���ӽ���, ����ͬ�����ÿ���ָ���ӽ����Ƿ���������־, ͬʱ����ָ�������Ƿ��첽����ͬ������, ����ͬ�����԰��սӿڵ���Ҳ���Թ���ȫ����������
    @���:
        @param    __REQ__    dict    ��������
        @param    __RSP__    dict    �������
        @param    MC         str     �ӽ���Ӧ�ô���
        @param    TC         str     �ӽ��׽��״���
        @param    logmode    str     ��־ģʽ(1-����������, 2-�ӽ��׵�������)
        @param    callmethod str     ���÷�ʽ(0-ͬ��py����,  2-�첽py����)
    @����:
    @����״̬
        @return    0    ����ʧ��
        @return    1    ���óɹ�
        @return    2    �����쳣(��ִ���������쳣)
    @��    ��: �鿬��
    @����ʱ��: 2015-2-9 09:21:07
    @ʹ�÷���:
    '''
    FLG = 0;
    Curlogname = None;
    Prevlogname = None;
    oldMC = None;
    oldTC = None;
    try:
        if ((type(__REQ__) is not dict ) or (type(__RSP__) is not dict)):
            return [0, "CTX001", "��� __REQ__ or  __RSP__ ���Ϸ�", [None]];
        if ((type(MC) is not str ) or (type(TC) is not str)):
            return [0, "CTX001", "��� MC or  TC ���Ϸ�", [None]];
        if ((type(logmode) is not str ) or (type(callmethod) is not str)):
            return [0, "CTX001", "��� logmode or callmethod ���Ϸ�", [None]];

        # ��ֹ���׵�������������ж�
        if __REQ__["__MC__"] == MC and __REQ__["__TC__"] == TC:
            return [0, "UPC001", "���׵���ʱ���������������" + TC, [None]];

        # �ӽ��׵��Ȳ���Ƕ��,���ֻ���ӽ��׵���һ��,�����__subcall_dept__��˵�����ӽ�����,����������ٽ��е����ӽ���
        # if __REQ__.has_key("__subcall_dept__"):
        # return [0,"UPC001", "�ӽ��ײ��ɵ�����������" + TC, [None]];

        # �ӽ��׵�MC��TC�滻
        oldMC = __REQ__["__MC__"];
        oldTC = __REQ__["__TC__"];
        __REQ__["__MC__"] = MC;
        __REQ__["__TC__"] = TC;
        __REQ__["templatecode"] = MC;
        __REQ__["transcode"] = TC;

        if callmethod == "0":  # ͬ��py����
            _ModuleName_ = "T" + MC + "_" + TC;
            _EntryName_ = 'M' + TC + "_ENTRY";

            _Module_ = __import__(_ModuleName_);
            _Method_ = getattr(_Module_, _EntryName_);

            if logmode == "2":  # �ӽ��׵�������
                ret = AppLoggerChange(MC, TC, "");  # ��־������
                if (ret[0] != 0):
                    return [0, "CTX002", "��־�����޸�Ϊ�ӽ�������ʱʧ��," + ret[1] + ret[2]];
                FLG = 1;
                Prevlogname = ret[3][0];
                Curlogname = ret[3][1];
                __REQ__["__LOG__"] = Curlogname;
                LoggerTrace("AppLoggerChange BEGIN:" + Curlogname + ":" + Prevlogname);

            ret = _Method_(__REQ__, __RSP__);
            FLG = 2;

            __REQ__["__MC__"] = oldMC;
            __REQ__["__TC__"] = oldTC;

            if logmode == "2":  # �ӽ��׵�������
                LoggerTrace("AppLoggerChange END:" + Prevlogname);
                ret2 = AppLoggerChange(oldMC, oldTC, "");
                if (ret2[0] != 0):
                    LoggerError("��־�����޸Ļ�ԭ��־����ʱʧ��," + ret[1] + ret[2]);
                __REQ__["__LOG__"] = Curlogname;

                FLG = 3;
            if (ret == True):
                return [1, None, None];
            else:
                return [2, "CTX003", "�ӽ��׵��÷���ֵ��True"];
        elif callmethod == "2":  # �첽py����
            __RSP__["__ASYNC__"] = True;
            __RSP__["__AMC__"] = MC;
            __RSP__["__ATC__"] = TC;
            return [1, None, None];
        else:
            return [0, "CTX002", "��֧�ֵĵ��÷�ʽ,��ֻ֧��ͬ��py����", [None]];
    except Exception, e:
        LoggerError(str(format_exc()));
        if logmode == "2":  # �ӽ��׵�������
            if (FLG >= 1 and FLG < 3 and Prevlogname != None):  # ��־���Ƹ�����ԭ����
                AppLoggerChange(oldMC, oldTC, "");
                __REQ__["__LOG__"] = Curlogname;

        return [0, "EXPT00", str(e), None];
    finally:
        if oldMC != None:
            __REQ__["__MC__"] = oldMC;
            __REQ__["__TC__"] = oldTC;


def travelquery(req, lst):
    '''
            ���ã� �����Ӳ�ѯ����
            ���ߣ�  ZH
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
    @�������: ��ҳ��ѯ���
    @������: ������
    @�������: �������ģ��
    @����ע��: ��ҳ��ѯ���
    @���:
        @param  __REQ__     dict ��������
        @param  __RSP__     dict ��������
        @param  sql         str  sql���
        @param  wherelist   list where�ֶ��б�
        @param  pageinfo    dict ��ҳ��Ϣ�ֵ�
    @����:
        @param where str where����
    @����״̬:
        @return 0  ʧ��
        @return 1  �ɹ�
        @return 2  �쳣
    @��    ��: ZH
    @����ʱ��: 2015-02-05
    @ʹ�÷���:
    '''
    try:
        DBCursor = None
        if ( DBConn == None ):
            return [0, 'A017059', '���ݿ����Ӷ���Ϊ��,�����ݿ�����', [None]]
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
        LoggerTrace("���ܲ�ѯ���Ϊ[%s]" % countsql)
        result = P_dml_sel(countsql, 0)
        if result[0] == 0:
            return [0, result[1], result[2], [None]]
        elif result[0] == 2:
            return [2, "999998", "�����������ļ�¼��", [None]]
        totalrownum = result[3][1][0][0]
        m, n = divmod(totalrownum, pagerownum)
        if n > 0:
            totalpagenum = m + 1
        else:
            totalpagenum = m
        querysql = "%s %s" % (sql, pagesql)
        LoggerTrace("�����ѯ���Ϊ[%s]" % querysql)
        DBCursor = DBConn.cursor()
        DBCursor.execute(querysql)
        result = DBCursor.fetchall()
        if not result:
            return [2, "999998", "�����������ļ�¼��", [None]]
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
    @�������: ���ݲ�ѯ
    @������: ѡ����
    @�������: �������ģ��
    @����ע��: ����sql��ѯ����ȡ��ѯ�����ݷ���һ���ֵ�
    @���:
        @param sql          str  ��ѯsql���
        @param onlyone      int  �Ƿ�ֻ��ѯ����
    @����:
        @param result       dict ��ѯ��������
    @����״̬:
        @return 0 ʧ��,���ݿ��쳣
        @return 1 �ɹ�
        @return 2 ������������¼
    @��    ��: ZH
    @����ʱ��: 2015-3-20
    @ʹ�÷���:
    '''
    global sqlErrMsg
    sqlErrMsg = ''
    DBCursor = None

    try:
        DBCursor = DBConn.cursor()
        if ( DBCursor == None ):
            return [0, 'A017060', '���ݿ��쳣,��ȡ�����α�ʱ���ؿ�', [None]]

        DBCursor.execute(sql)
        _Result_ = DBCursor.fetchall()
        if len(_Result_) == 0:
            return [2, 'A017061', '������������¼', [None]]
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
        return [0, 'A017100', '���ݿ��쳣,' + str(e), [None]]
    finally:
        if DBCursor != None:
            DBCursor.close()
            DBCursor = None


def B_Checkorgan(organo):
    '''
        @�������: ��֯��������У��
        @������: �ж���
        @�������: �������ģ��
        @����ע��: У����֯��������,֤��ΪXXXXXXXX-X��00000000-0ֱ��ͨ��
        @���:
            @param  organo        str ��������
        @����:
            @param  errorcode     str ������
            @param  errormsg����  str ������Ϣ
        @����״̬:
            @return 0  ʧ��
            @return 1  �ɹ�
        @��    ��: �鿬��
        @����ʱ��: 2015��3��25��
        @ʹ�÷���:
    '''
    try:
        if (organo in ['XXXXXXXX-X', '00000000-0']):
            errorcode = '000000';
            errormsg = '��֯�ṹ����У�����';
            return [1, None, None, [errorcode, errormsg]];

        if (len(organo) != 10):
            errorcode = 'CKFAL01';
            errormsg = '��֯�ṹ�����ʽ����,���ȱ�����10';
            return [0, None, None, [errorcode, errormsg]];
        chkno = organo[0:8];
        if (organo[-2] != '-'):
            errorcode = 'CKFAL01';
            errormsg = "��֯�ṹ�����ʽ����,�����ڶ�λ��'-'";
            return [0, None, None, [errorcode, errormsg]];
        chklst = list(chkno);
        ai = [];
        si = ['3', '7', '9', '10', '5', '8', '4', '2'];
        for i, j in enumerate(chklst):
            if (ord(j) >= 48 and ord(j) <= 57):  # ����ȡ����
                ai.append(j);
            elif (ord(j) >= 65 and ord(j) <= 90):  # ��д��ĸȡ16���Ʊ�������
                ai.append(j.encode('hex'));
            else:
                errorcode = 'CKFAL02';
                errormsg = '��֯�ṹ���������ֻ��д��ĸ';
                return [0, None, None, [errorcode, errormsg]];
        # �����ֵ 10��ӦУ��ֵ11 11��ӦУ��ֵ0 ����Ϊ��Ӧ��ֵ
        wi = {'10': 'X', '11': '0'};
        checkvalue = abs(11 - reduce((lambda x, y: x + y), map(lambda x, y: int(x) * int(y), ai, si)) % 11);
        LoggerTrace("У��ֵӦΪ:" + str({'10': 'X', '11': '0'}.get(str(checkvalue), str(checkvalue))));
        if (str(checkvalue) in wi):
            if (wi[str(checkvalue)] == organo[-1]):
                errorcode = '000000';
                errormsg = 'У��ɹ�';
                return [1, None, None, [errorcode, errormsg]];
            else:
                errorcode = 'CKFAL03';
                errormsg = 'У�鲻ͨ��';
                return [0, None, None, [errorcode, errormsg]];
        elif (str(checkvalue) == organo[-1]):
            errorcode = '000000';
            errormsg = 'У��ɹ�';
            return [1, None, None, [errorcode, errormsg]];
        else:
            errorcode = 'CKFAL03';
            errormsg = 'У�鲻ͨ��';
            return [0, None, None, [errorcode, errormsg]];


    except Exception, e:
        LoggerError("------------------>У����֯���������쳣" + str(format_exc()));
        errorcode = 'CKFAL00';
        errormsg = 'У����֯���������쳣';
        return [0, 'CKFAL00', 'У����֯���������쳣' + str(e), [errorcode, errormsg]]


def SFTP2Internet(__REQ__, method, host, port, user, password, filename, remotepath, afadir, afasubdir, ):
    '''
        @�������: �ϴ������ļ���������SFTP������
        @������: �ж���
        @�������: �������ģ��
        @����ע��: �ϴ������ļ���������SFTP������
        @���:
            @param  __REQ__     dict ��������
            @param  method      str  �ϴ����� GET������ PUT���ϴ�
            @param  host        str  SFTP��������ַ
            @param  port        str  SFTP�������˿�
            @param  user        str  SFTP�û���
            @param  password    str  SFTP�û���
            @param  filename    str  �ļ���
            @param  remotepath  str  SFTP·��
            @param  afadir      str  ����sysid
            @param  afasubdir   str  ������·��
        @����:
        @����״̬:
            @return 0  ʧ��
            @return 1  �ɹ�
        @��    ��: Z.H.
        @����ʱ��: 2015��9��9��
        @ʹ�÷���:
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
            return [0, "A90981", "�����ļ�ʧ��", [None]]
        return [1, None, None, [None]]
    except Exception as e:
        return [0, "A90982", [str(e)], [None]]