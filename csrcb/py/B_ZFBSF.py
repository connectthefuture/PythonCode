# -*- coding: gbk -*-
'''
@文件名称: A_ZFBSF.py
@组件组: 支付宝代缴水费
@组件级别: 应用级
@项目名称: CSRCB
@应用名称: 000018
@作    者: Z.H.
@创建时间: 20150909
@创建地点: 常熟农商行
@修订说明: [每修订一次则新增如下一行 @修订: 某人    某日    修改内容及原因说明(多次修订时依次排开),其中@修订要空4个空格]
'''
from AFALogger import LoggerTrace, LoggerDebug, LoggerError
import B_Communition
import P_Amount
from P_Database import P_sql_sel, P_dml_sel, P_db_execsql, P_db_commit, P_db_rollback, P_GetDBCursor, P_CloseDBCursor, \
    P_dml_ins, P_dml_upd
import traceback
import urllib, urlparse, httplib, os
import P_Database
import P_File


def A_ParseDZFile(__REQ__):
    '''
    @组件名称: 解析支付宝对账文件
    @组件风格: 判断型
    @组件类型: 横向参数模块
    @中文注释: 解析支付宝对账文件
    @入参:
        @param __REQ__ dict 请求容器
    @出参:
    @返回状态:
        @return 0 调用失败
        @return 1 对账成功
    @author: Z.H.
    @创建地点: 常熟农商行
    @创建时间: 20150909
    '''
    __RST__, __ECD__, __MSG__ = "", "", ""
    try:
        dealstat = 'A2'
        filedir = "%s/workspace/fdir/%s/zfb" % (os.getenv("HOME"), __REQ__["__MC__"],)
        LoggerDebug("filedir=[%s]" % (filedir))
        if not os.path.exists(filedir):
            try:
                os.mkdir(filedir)
            except:
                pass
        filepath = os.path.join(filedir, __REQ__["filename"])
        fd = None
        # LONGSHINE_SDDL_DSDZ_20131012.txt
        xzjg, czjg, filetype, tmp, checkdate = __REQ__["filename"][:-4].split("_")
        __REQ__['chkdate'] = checkdate
        sql = "delete from zfbsf_chkdetailbook where sysid = '%s' and workdate = '%s'" % (__REQ__['__MC__'], checkdate)
        result = P_db_execsql(sql, True)
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        fd = open(filepath, 'r')
        lineno = 0
        totalamt, totalnum, sumtotalamt, sumtotalnum = 0, 0, 0, 0
        recordno = 0
        for line in fd:
            lineno += 1
            line = line.strip('\r').strip('\n')
            if not line:
                break
            if lineno == 1:
                row = line.split('|')
                totalamt, totalnum = row[0], row[1]
            else:
                # 户号|缴费流水号|缴费日期|交易金额|记录数|用户户号$应收标识$应收年月$#<多条时重复>|
                recordno += 1
                row = [i.strip(' ').encode('GBK') for i in unicode(line, 'GBK').split('|')]
                consno = row[0]
                serialno = row[1]
                bankdate = row[2]
                amount = row[3]
                detailno = row[4]
                sumtotalamt += int(amount)
                result = P_dml_ins("zfbsf_chkdetailbook", [
                    ["sysid", __REQ__["__MC__"]], ["workdate", checkdate], ["bankserial", serialno],
                    ["amount", amount], ["consno", consno], ["bankdate", bankdate], ["chkstatus", "0"],
                    ["detailno", detailno], ['filename', __REQ__["filename"]],
                    ['chargecnt', __REQ__.get('chargecnt', '')], ['detinfo', __REQ__.get('detinfo', '')]], True)
                if result[0] != 1:
                    return [0, result[1], result[2], None]
        if recordno != int(totalnum):
            __RST__, __ECD__, __MSG__ = 'F', 'A98200', '总笔数不符'
            return [0, "A98200", "总笔数不符", [None]]
        if int(totalamt) != sumtotalamt:
            __RST__, __ECD__, __MSG__ = 'F', 'A98200', '总金额不符'
            return [0, "A98201", "总金额不符", [None]]
        __ECD__, __MSG__ = "000000", "对账文件入库成功"
        dealstat = 'A1'
        LoggerDebug("更新zfbsf_fileserverinfo 成功")
        result = P_dml_upd("zfbsf_fileserverinfo",
                           [["dealstat", dealstat], ["dealcode", __ECD__], ["dealmsg", __MSG__]],
                           [["sysid", "=", __REQ__["__MC__"], "and"], ["transdate", "=", __REQ__["filedate"], "and"],
                            ["zfiletype", "=", "DSDZ", None]], False)
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        sql = "update zfbsf_checkinfo set chkstatus = 'A1' where sysid = '%s' and chkdate = '%s'" % (
            __REQ__['__MC__'], checkdate)
        LoggerDebug("执行SQL语句:%s" % sql)
        result = P_db_execsql(sql, True)
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        else:
            return [1, None, None, [None]]
    except Exception as e:
        dealstat = 'A0'
        LoggerError("错误码=[%s], 错误原因=[%s]" % (__ECD__, __MSG__))
        result = P_dml_upd("zfbsf_fileserverinfo",
                           [["dealstat", dealstat], ["dealcode", str(__ECD__)[:10]], ["dealmsg", '文件解析入库出错']],
                           [["sysid", "=", __REQ__["__MC__"], "and"], ["transdate", "=", __REQ__["filedate"], "and"],
                            ["zfiletype", "=", "DSDZ", None]], False)
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        sql = "update zfbsf_checkinfo set chkstatus = 'A0' where sysid = '%s' and chkdate = '%s'" % (
            __REQ__['__MC__'], checkdate)
        LoggerDebug("执行SQL语句:%s" % sql)
        result = P_db_execsql(sql, True)
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        return [0, __ECD__, __MSG__, [None]]
    finally:
        if fd:
            fd.close()
        P_db_rollback()
        LoggerError(traceback.format_exc())


def A_ZfbCheck(__REQ__, chkdate):
    '''
    @组件名称: 支付宝对账
    @组件风格: 判断型
    @组件类型: 横向参数模块
    @中文注释: 与支付宝对账
    @入参:
        @param __REQ__ dict 处理容器
        @param chkdate str 对账日期
    @出参:
    @返回状态:
        @return 0 调用失败
        @return 1 对账成功
    @author: Z.H
    @创建地点: 常熟农商行
    @创建时间: 20150910
    '''

    try:
        _ecd_, _msg_ = '', ''
        succFlag = False
        _no_ = 0
        sql = "select chkstatus, errflag from zfbsf_checkinfo where chkdate = '%s'" % (chkdate,)
        result = P_dml_sel(sql)
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        chkstatus = result[3][1][0][0]
        LoggerDebug("当前对账状态 [%s]" % (chkstatus,))
        if not chkstatus.strip() in ("A1", "B0"):
            return [0, "A98210", "当前状态无法对账", [None]]
        sql = "update zfbsf_checkinfo set chkstatus = 'B2' where chkdate = '%s' and sysid = '%s' and chkstatus = '%s'" % (
            chkdate, __REQ__['__MC__'], chkstatus)
        result = P_db_execsql(sql, True)
        if result[0] != 1:
            return [0, "A98211", "已经对账中", [None]]
        sql = "update sfds_maintransdtl set rem4 = '1' where sysid = '%s' and workdate = '%s' and channelcode = '%s'" % (
            __REQ__["__MC__"], chkdate, '404')
        LoggerDebug("更新sfds_maintransdtl SQL: %s" % (sql,))
        result = P_db_execsql(sql, True)
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        # sql = "delete from zfbsf_checkerrbook"
        sql = "select sysid,workdate,filename,detailno,consno,bankserial,bankdate,amount,chkstatus,chargecnt,detinfo " \
              "from zfbsf_chkdetailbook where sysid='%s' and workdate='%s' and chkstatus='0'" % (
                  __REQ__["__MC__"], chkdate);
        LoggerDebug("查询对账日期zfbsf_chkdetailbook中所有的记录：" + sql)

        _ret_ = P_GetDBCursor()
        if _ret_[0] != 1:
            return [0, _ret_[1], _ret_[2], [None]]
        dbcursor = _ret_[3][0]
        dbcursor.execute(sql)
        z_row = dbcursor.fetchone()
        while _no_ < dbcursor.rowcount:
            if z_row is None:
                break
            _no_ = _no_ + 1
            LoggerDebug("==============第 " + str(_no_) + " 笔数据==============")
            LoggerDebug("z_sysid：" + z_row[0])
            LoggerDebug("z_workdate：" + z_row[1])
            LoggerDebug("z_filename：" + z_row[2])
            LoggerDebug("z_detailno：" + z_row[3])
            LoggerDebug("z_consno：" + z_row[4])
            LoggerDebug("z_bankserial：" + z_row[5])
            LoggerDebug("z_bankdate：" + z_row[6])
            LoggerDebug("z_amount：" + z_row[7])
            LoggerDebug("z_chkstatus：" + z_row[8])
            LoggerDebug("z_chargecnt：" + z_row[9])
            LoggerDebug("z_detinfo：" + z_row[10])
            z_sysid = z_row[0];  # 系统标识
            z_workdate = z_row[1];  # 平台日期
            z_filename = z_row[2];  # 文件名称
            z_detailno = z_row[3];  # 明细序号
            z_consno = z_row[4];  # 用户号
            z_bankserial = z_row[5];  # 支付宝流水
            z_bankdate = z_row[6];  # 支付宝日期
            z_amount = z_row[7];  # 金额
            z_chkstatus = z_row[8];  # 对账状态
            z_chargecnt = z_row[9];  # 记录数
            z_detinfo = z_row[10];  # 明细信息集

            sql = "select workdate,serialno,userid,yearmonth,water,amount,znamount,hoststatus from sfds_maintransdtl " \
                  "where sysid='%s' and channelcode='404' and userid='%s' and rem2='%s' and rem3='%s'" % (
                      __REQ__["__MC__"], z_consno, z_bankserial, z_bankdate);
            LoggerDebug("查询sfds_maintransdtl SQL:%s" % (sql))
            result = P_dml_sel(sql, 0)
            if result[0] == 0:
                return [0, result[1], result[2], [None]]
            elif result[0] == 2:
                # 支付宝有平台无
                LoggerDebug("====================支付宝有平台无=====================")
                result = P_Database.P_db_sequence(__REQ__["_Sque_name_"], __REQ__["DataBaseType"],
                                                  int(__REQ__["_SequenceLength_"]))
                if result[0] != 1:
                    continue
                serialno = result[3][0]
                sql = "insert into zfbsf_checkerrbook (sysid, chkdate, workdate, serialno, bankdate, bankserial, transcode, userid, amount, difflev, difftype,  " \
                      "diffdesc, diffsour, dealtype, dealresult, dealcode, dealmsg) (select '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                      "'1', '3', '支付宝多，需补账', 'Z', 'H', '0', '000000', '登记差错表' from sysibm.sysdummy1 " \
                      "where not exists (select 1 from zfbsf_checkerrbook where bankdate = '%s' and bankserial = '%s'))" % (
                          __REQ__["__MC__"], chkdate, chkdate, serialno, z_bankdate, z_bankserial, __REQ__['__TC__'],
                          z_consno, z_amount,
                          z_bankdate, z_bankserial
                      )
                LoggerDebug("插入差异表SQL:%s" % (sql,))
                result = P_db_execsql(sql, True)
                if result[0] != 1:
                    return [0, result[0], result[1], [None]]
            else:
                LoggerDebug("====================平台有该笔记录====================")
                p_amount = result[3][1][0][5].strip()
                if p_amount != z_amount:
                    LoggerError("金额不符，平台金额%s，支付宝金额%s" % (p_amount, z_amount))
                else:
                    LoggerDebug("=================更新支付宝记录有状态=====================")
                    sql = "update sfds_maintransdtl set rem4 = '0' where sysid = '%s' and rem2 = '%s' and rem3 = '%s'" % (
                        __REQ__["__MC__"], z_bankserial, z_bankdate,
                    )
                    result = P_db_execsql(sql, True)
                    if result[0] != 1 or (result[1] == 1 and result[3][0] == 0):
                        return [0, "A98212", "更新数据库错", [None]]
                    LoggerDebug("待核实记录，平台记账失败")
            LoggerDebug("==================第%d笔记录处理完成===========================" % (_no_ - 1))
        # 现在查询出了0，2,4 的状态，是否需要全部查出来
        # sql = "insert into zfbsf_checkerrbook (sysid, chkdate, workdate, serialno, brno, teller, transcode, userid, yearmonth, amount, " \
        #       "difflev, difftype, diffdesc, diffsour, dealtype, dealresult, dealcode, dealmsg) " \
        #       "select sysid, '%s', workdate, serialno, brc, teller, '%s', userid, yearmonth, amount, '1', '2', '支付宝无平台多，需抹账', " \
        #       "'P', 'H', '0', '000000', '登记差错表' from sfds_maintransdtl m where " \
        #       "sysid = '%s' and channelcode = '404' and workdate = '%s' " \
        #       "and hoststatus in ('0', '2') and not exists (select 1 from zfbsf_checkerrbook where workdate = m.workdate and serialno = m.serialno " \
        #       "and diffsour = 'P') " % (
        #           chkdate, __REQ__["__TC__"], __REQ__["__MC__"], chkdate,
        #       )
        # LoggerDebug("插入平台多数据SQL:%s" % (sql,))
        # result = P_db_execsql(sql, True)
        # if result[0] != 1:
        #     return [0, result[1], result[2], [None]]
        # LoggerDebug("总共插入了%d条数据" %(result[3][0]))
        sql = "update zfbsf_checkinfo set chkstatus = 'B1' where sysid = '%s' and chkdate = '%s'" % (
            __REQ__['__MC__'], chkdate)
        LoggerDebug("更新对账控制表SQL:%s" % sql)
        result = P_db_execsql(sql, True)
        if result[0] != 1:
            return [0, result[1], result[2], [None]]
        else:
            succFlag = True
            return [1, None, None, [None]]
    except Exception as e:
        LoggerError(traceback.format_exc())
        return [0, 'A98213', str(e), [None]]
    finally:
        P_db_rollback()
        i = 0
        if not succFlag:
            while i < 3:
                i += 1
                sql = "update zfbsf_checkinfo set chkstatus = 'B0' where sysid = '%s' and chkdate = '%s'" % (
                    __REQ__['__MC__'], chkdate)
                result = P_db_execsql(sql, True)
                if result[0] == 1 and result[3][0] >= 1:
                    break


def A_ZfbHostCheck(__REQ__, chkdate, ):
    '''
    @组件名称: 支付宝核心对账
    @组件风格: 判断型
    @组件类型: 横向参数模块
    @中文注释: 与支付宝对账
    @入参:
        @param __REQ__ dict 处理容器
        @param chkdate str 对账日期
    @出参:
    @返回状态:
        @return 0 调用失败
        @return 1 对账成功
    @author: Z.H
    @创建地点: 常熟农商行
    @创建时间: 20150910
    '''
    try:
        succFlag = False
        totalNum, succNum = 0, 0

        sql = "select initkey, initvalue from afa_initmsgmap where sysid = '%s' and msgtype = 'ZFBSF'"
        result = P_dml_sel(sql, 0)
        if result[0] == 0:
            return result
        elif result[0] == 1:
            for i, j in result[3][1]:
                __REQ__[i] = j

        sql = "select chkstatus from zfbsf_checkinfo where sysid = '%s' and chkdate = '%s'" % (
            __REQ__["__MC__"], chkdate)
        result = P_dml_sel(sql, 0)
        if result[0] == 0:
            return result[:3] + [None]
        elif result[0] == 2:
            return [0, "A98247", "查询无对账记录", [None]]
        chkstatus = result[3][1][0][0]
        if not chkstatus in ("B1", "C0", "C1"):
            return [0, None, None, [None]]
        elif chkstatus == "C1":
            return [1, None, None, [None]]
        result = P_File.P_filedata_getconf(__REQ__, ["inter_comm.conf", None], [
            [__REQ__["sysid"] + "_HOST", 'IP', 'host.ip', None],
            [__REQ__["sysid"] + "_HOST", 'PORT', 'host.port', None],
            [__REQ__["sysid"] + "_HOST", 'TIMEOUT', 'host.timeout', None]
        ])
        if result[0] == 0:
            return [0, result[1], result[2], [None]]

        sql = "select workdate, serialno, hoststatus, swstatus, rem4, rem2, rem3, userid, amount from sfds_maintransdtl where sysid = '%s' and workdate = '%s'" % (
            __REQ__["__MC__"], chkdate,)
        LoggerDebug("查询对账记录表SQL:" % (sql,))
        transdtl = P_dml_sel(sql, 0)
        if transdtl[0] == 0:
            return [0, transdtl[1], transdtl[2], [None]]
        elif transdtl[0] == 2:
            pass
        else:
            for p_workdate, p_serialno, p_hoststatus, p_swstatus, p_zfbstatus, p_bankserial, p_bankdate, p_userid, p_amount in \
                    transdtl[3][1]:
                p_zfbstatus = p_zfbstatus.strip(' ')
                p_hoststatus = p_hoststatus.strip(' ')
                p_swstatus = p_swstatus.strip(' ')
                sql = "select workdate, serialno from djsf_hostcheckdtl where sysid = '%s' and workdate = '%s'" % (
                    __REQ__["__MC__"], chkdate,)
                # rem4 == 0 支付宝有
                hostchkdtl = P_dml_sel(sql, 0)
                if hostchkdtl[0] == 0:
                    return [0, result[1], result[2], [None]]
                elif hostchkdtl[0] == 1:
                    # 平台有，核心有
                    if p_zfbstatus == '0':
                        # 支付宝有
                        sql = "update sfds_maintransdtl set hoststatus = '0' where sysid = '%s' and workdate = '%s' and serialno = '%s'" % (
                            __REQ__["__MC__"], p_workdate, p_serialno
                        )
                        LoggerDebug("更新记账状态成功")
                        result = P_db_execsql(sql, True)
                        if result[0] == 0:
                            LoggerError("更新数据失败，%s %s" % (result[1], result[2]))
                            return [0, result[1], result[2], [None]]
                    else:
                        # 支付宝无
                        sql = "insert into zfbsf_checkerrbook (sysid, chkdate, workdate, serialno, bankdate, bankserial, transcode, userid, amount, difflev, difftype,  " \
                              "diffdesc, diffsour, dealtype, dealresult, dealcode, dealmsg) (select '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' " \
                              "'1', '2', '核心多，需抹账，无法柜面处理', 'H', 'H', '0', '000000', '登记差错表' from sysibm.sysdummy1 " \
                              "where not exists (select 1 from zfbsf_checkerrbook where bankdate = '%s' and bankserial = '%s'))" % (
                                  __REQ__["__MC__"], chkdate, chkdate, p_serialno, p_bankdate, p_bankserial,
                                  __REQ__["__TC__"], p_userid, p_amount, p_userid, p_amount, p_bankdate, p_bankserial
                              )
                else:
                    # 平台有，核心无
                    if p_zfbstatus == '0':
                        # 支付宝有, 需要去补记账
                        sql = "insert into zfbsf_checkerrbook (sysid, chkdate, workdate, serialno, bankdate, bankserial, transcode, userid, amount, difflev, difftype,  " \
                              "diffdesc, diffsour, dealtype, dealresult, dealcode, dealmsg) (select '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' " \
                              "'1', '3', '支付宝多，需补账', 'Z', 'H', '0', '000000', '登记差错表' from sysibm.sysdummy1 " \
                              "where not exists (select 1 from zfbsf_checkerrbook where bankdate = '%s' and bankserial = '%s'))" % (
                                  __REQ__["__MC__"], chkdate, chkdate, p_serialno, p_bankdate, p_bankserial,
                                  __REQ__["__TC__"], p_userid, p_amount,
                                  p_userid, p_amount, p_bankdate, p_bankserial
                              )
                        LoggerDebug("插入差异表SQL：" % (sql,))
                        result = P_db_execsql(sql, True)
                        if result[0] == 0:
                            return [0, result[1], [2], [None]]
                    else:  # 平台有，核心无， 支付宝无
                        if p_swstatus == '9':
                            sql = "update sfds_maintransdtl set hoststatus = '1' where sysid = '%s' and workdate = '%s' " \
                                  "and serialno = '%s'" % (__REQ__["__MC__"], p_workdate, p_serialno)
                            result = P_db_execsql(sql, True)
                            if result[0] == 0:
                                return [0, result[1], result[2], [None]]
                        else:
                            sql = "update sfds_maintransdtl set hoststatus = '3' where sysid = '%s' and workdate = '%s' " \
                                  "and serialno = '%s'" % (__REQ__["__MC__"], p_workdate, p_serialno)
                            result = P_db_execsql(sql, True)
                            if result[0] == 0:
                                return [0, result[1], result[2], [None]]

        sql = "update sfds_maintransdtl set hoststatus = '1' where workdate = '%s' and rem4 != '0' and serialno not in (select serialno " \
              "from djsf_hostcheckdtl where sysid = '000018' and workdate = '%s' and frntno = '%s' )" % (
                  chkdate, chkdate, __REQ__['_FrntNo_'],
              )
        LoggerTrace("更新平台有，核心无记录记账失败SQL: " % sql)

        result = P_db_execsql(sql, True)
        if result[0] != 0:
            return result[:3] + [None]
        else:
            LoggerTrace("更新了%d条记录" % result[3][0])
    except Exception as e:
        LoggerError(traceback.format_exc())
        return [0, "A98216", "处理支付宝水费差错异常", [None]]
    finally:
        P_db_rollback()
        LoggerTrace("成功处理了%d笔差错" % succNum)
        if succNum == totalNum:
            sql = "update zfbsf_checkinfo set chkstatus = 'C1', errmsg = '与核心对账成功' where sysid = '%s' and chkdate = '%s'" % (
                __REQ__["__MC__"], chkdate,)
            LoggerTrace("==============更新支付宝核心对账对账成功 SQL:" + sql)
            P_db_execsql(sql, True)


def A_DealZfbError(__REQ__, seqtype, date, serno):
    '''
    @组件名称: 支付宝差错处理
    @组件风格: 判断型
    @组件类型: 横向参数模块
    @中文注释: 与支付宝对账
    @入参:
        @param __REQ__ dict 处理容器
        @param seqtype str 流水类型
        @param date str 日期
        @param serno str 流水号
    @出参:
    @返回状态:
        @return 0 调用失败
        @return 1 对账成功
    @author: Z.H
    @创建地点: 常熟农商行
    @创建时间: 20150910
    '''
    try:
        if seqtype == 'P':
            workdate, serialno = date, serno
            sql = "select workdate, serialno, bankdate, bankserial, brno, teller, transcode, userid, yearmonth, amount, difflev, difftype, diffsour, " \
                  "dealtype from zfbsf_checkerrbook where sysid = '%s' and workdate = '%s' and serialno = '%s'" % (
                      __REQ__['__MC__'], workdate, serialno)
        else:
            bankdate, bankserial = date, serno
            sql = "select workdate, serialno, bankdate, bankserial, brno, teller, transcode, userid, yearmonth, amount, difflev, difftype, diffsour, " \
                  "dealtype from zfbsf_checkerrbook where sysid = '%s' and workdate = '%s' and serialno = '%s'" % (
                      __REQ__['__MC__'], bankdate, bankserial)
        result = P_dml_sel(sql, 0)
        if result[0] == 0:
            return result
        elif result[0] == 2:
            return [0, "A98310", "查询无差错记录", [None]]
        else:
            pass
        workdate = result[3][1][0][0]
        serialno = result[3][1][0][1]
        bankdate = result[3][1][0][2]
        bankserial = result[3][1][0][3]
        brno = result[3][1][0][4]
        teller = result[3][1][0][5]
        transcode = result[3][1][0][6]
        userid = result[3][1][0][7]
        amount = result[3][1][0]
        yearmonth = result[3][1][0][8]
        difflev = result[3][1][0][9]
        difftype = result[3][1][0][10]
        diffsour = result[3][1][0][11]
        dealtype = result[3][1][0][12]
        if dealtype == '0':
            return [0, "A98312", "该异常已经处理", [None]]
        if dealtype == 'H':
            return [0, "A98311", "无法从柜面发起处理交易", [None]]
        if difftype == '3':
            pass
        # sfds_maintransdtl表里已有记录
        sql = "select hoststatus from sfds_maintransdtl where workdate = '%s' and serialno = '%s'" % (
            workdate, serialno)
        result = P_dml_sel(sql, True)
        if result[0] == 0:
            return result[:3] + [None]
        elif result[2] == 0:
            LoggerError("流水%s查询无记录,异常,程序无法处理!" % (serialno))
        else:
            t_hoststatus = result[3][1][0][0]
            if t_hoststatus in ('1', '2'):
                LoggerTrace("==============流水%s记账超时或失败" % (serialno,))
                A99002_REQ = {}
                A99002_REQ['FrntNo'] = __REQ__['frntno']
                A99002_REQ['OrigFrntNo'] = serialno
                A99002_REQ['Teller'] = __REQ__['_Teller_']
                A99002_REQ['Brc'] = __REQ__['_Brc_']
                A99002_REQ['ChannelId'] = __REQ__['_ChannelId_']
                A99002_REQ['BeginDate'] = workdate
                A99002_REQ['EndDate'] = workdate
                a99002result = B_Communition.B_NATPClient(A99002_REQ, __REQ__["__MC__"], "A99002",
                                                          "",
                                                          __REQ__["host.ip"], int(__REQ__["host.port"]),
                                                          int(__REQ__["host.timeout"]))
                if a99002result[0] != 1:
                    LoggerTrace("A99002错误码%s,错误原因%s" % (a99002result[1], a99002result[2]))
                else:
                    if a99002result[3][0]["RspCode"] == "000000":
                        if int(a99002result[3][0]['TotalCount']) > 0:
                            LoggerTrace("流水%s记账成功" % serialno)
                            A80012_RSP = a99002result[3][0]
                            accoutingFlag = True
        if not accoutingFlag:
            A80012_REQ = {}
            A80012_REQ['FrntNo'] = __REQ__['_FrntNo_']
            A80012_REQ['RegDate'] = workdate
            A80012_REQ['SendDate'] = workdate
            A80012_REQ['TranSeq'] = serialno
            A80012_REQ['TranDate'] = workdate
            A80012_REQ['Ccy'] = "01"
            A80012_REQ['Teller'] = __REQ__['_Teller_']
            A80012_REQ['Brc'] = __REQ__['_Brc_']
            A80012_REQ['ChannelId'] = __REQ__['_ChannelId_']
            A80012_REQ['TradeCode'] = "A80012"
            A80012_REQ['Memo1'] = "支付宝代缴水费"
            A80012_REQ['TranAmt'] = P_Amount.P_amount_InsDot(amount)[3][0]
            a80012result = B_Communition.B_NATPClient(A80012_REQ, __REQ__["__MC__"], "A80012",
                                                      "",
                                                      __REQ__["host.ip"], int(__REQ__["host.port"]),
                                                      int(__REQ__["host.timeout"]))
            if a80012result[0] != 1:
                LoggerError("A80012交易处理异常[%s][%s]" % (a80012result[1], a80012result[2]))
            A80012_RSP = a80012result[3][0]
            if A80012_RSP["RspCode"] != "000000":
                LoggerError("核心返回错误[%s][%s]" % (A80012_RSP["RspCode"], A80012_RSP["RspMsg"]))
            sql = "update sfds_maintransdtl set hostserialno = '%s', hostdate = '%s', hosterrorcode = '%s', hosterormsg = '%s', " \
                  "hoststatus = '%s' where workdate = '%s' and serialno = '%s'" % (
                      A80012_RSP.get("", "SerSeqNo"), A80012_RSP.get("", "TranDate"),
                      A80012_RSP.get("RspCode", "000000"), A80012_RSP.get("", "RspMsg"),
                      workdate, serialno)
            result = P_db_execsql(sql, False)
            if result[0] != 1:
                LoggerError("更新 sfds_maintransdtl 失败 %s %s" % (result[1], result[2]))
                P_db_rollback()
            sql = "update zfbsf_checkerrbook set dealresult = '0' where sysid = '%s', bankdate = '%s' and bankserial = '%s'" % (
                __REQ__["__MC__"], bankdate, bankserial)
            result = P_db_execsql(sql, False)
            if result[0] != 1:
                LoggerError("更新 zfbsf_checkerrbook %s %s" % (result[1], result[2]))
                P_db_rollback()
            else:
                P_db_commit()
    except Exception as e:
        pass
    finally:
        pass