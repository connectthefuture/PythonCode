# -*- coding: gbk -*-
'''
@文件名称: B_EsbFile.py
@组件组: ESB文件传输类
@组件级别: 银行级
@作    者: Z.H.
@创建时间: 20150924
@创建地点: 常熟农商行
@修订说明: [每修订一次则新增如下一行 @修订: 某人    某日    修改内容及原因说明(多次修订时依次排开),其中@修订要空4个空格]
'''

import esbfile
import os
import time

cfgfile = "%s/workspace/cfg/esb_file.ini" % os.getenv("HOME")
os.putenv("ESB_CAPI_CFG", cfgfile)


def B_ftpput(localpath, filename, remotepath):
    '''
    @组件名称: ESB文件上传
    @组件风格: 判断型
    @组件类型: 横向参数模块
    @中文注释: ESB文件上传
    @入参:
        @param localpath str 本地文件路径
        @param filename str 传输文件名
        @param remotepath str 远程路径
    @出参:
    @返回状态:
        @return 0 调用失败
        @return 1 调用成功
    @author: Z.H.
    @创建地点: 常熟农商行
    @创建时间: 20150924
    @使用示例： B_ftpput("/home/afa/user/xx/c/esb_file/src/", "mk.sh", "/IFS/100002") AFA上传的文件要放到 /IFS之后的目录下面
    '''
    try:
        remotefile = os.path.join(remotepath, filename)
        rec = esbfile.Py_ftpput(os.path.join(localpath, filename), remotefile)
        if rec != 0:
            return [0, "ESB001", "ESB上传文件失败", [None]]
        return [1, None, None, [None]]
    except Exception as e:
        return [0, "ESB002", str(e), [None]]


def B_ftpget(remotepath, filename, localpath):
    '''
    @组件名称: ESB文件下载
    @组件风格: 判断型
    @组件类型: 横向参数模块
    @中文注释: ESB文件下载
    @入参:
        @param remotepath str 远程路径
        @param filename str 传输文件名
        @param localpath str 本地路径
    @出参:
    @返回状态:
        @return 0 调用失败
        @return 1 调用成功
    @author: Z.H.
    @创建地点: 常熟农商行
    @创建时间: 20150924
    '''
    try:
        remotefile = os.path.join(remotepath, filename)
        localfile = os.path.join(localpath, filename)
        rec = esbfile.Py_ftpget(remotefile, localfile)
        if rec != 0:
            return [0, "ESB003", "ESB文件下载失败", [None]]
        return [1, None, None, [None]]
    except Exception as e:
        return [0, "ESB004", str(e), [None]]


if __name__ == '__main__':
    # 注意远程目录要填 /IFS/
    while 1:
        print(B_ftpput("/home/afa/user/xx/c/esb_file/src", "mk.sh", "/IFS"))
        B_ftpget("/IFS/", "mk.sh", "/home/afa/user/xx/c/esb_file/src/")
        time.sleep(1)