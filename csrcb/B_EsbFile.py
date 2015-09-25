# -*- coding: gbk -*-
'''
@�ļ�����: B_EsbFile.py
@�����: ESB�ļ�������
@�������: ���м�
@��    ��: Z.H.
@����ʱ��: 20150924
@�����ص�: ����ũ����
@�޶�˵��: [ÿ�޶�һ������������һ�� @�޶�: ĳ��    ĳ��    �޸����ݼ�ԭ��˵��(����޶�ʱ�����ſ�),����@�޶�Ҫ��4���ո�]
'''

import esbfile
import os
import time

cfgfile = "%s/workspace/cfg/esb_file.ini" % os.getenv("HOME")
os.putenv("ESB_CAPI_CFG", cfgfile)


def B_ftpput(localpath, filename, remotepath):
    '''
    @�������: ESB�ļ��ϴ�
    @������: �ж���
    @�������: �������ģ��
    @����ע��: ESB�ļ��ϴ�
    @���:
        @param localpath str �����ļ�·��
        @param filename str �����ļ���
        @param remotepath str Զ��·��
    @����:
    @����״̬:
        @return 0 ����ʧ��
        @return 1 ���óɹ�
    @author: Z.H.
    @�����ص�: ����ũ����
    @����ʱ��: 20150924
    @ʹ��ʾ���� B_ftpput("/home/afa/user/xx/c/esb_file/src/", "mk.sh", "/IFS/100002") AFA�ϴ����ļ�Ҫ�ŵ� /IFS֮���Ŀ¼����
    '''
    try:
        remotefile = os.path.join(remotepath, filename)
        rec = esbfile.Py_ftpput(os.path.join(localpath, filename), remotefile)
        if rec != 0:
            return [0, "ESB001", "ESB�ϴ��ļ�ʧ��", [None]]
        return [1, None, None, [None]]
    except Exception as e:
        return [0, "ESB002", str(e), [None]]


def B_ftpget(remotepath, filename, localpath):
    '''
    @�������: ESB�ļ�����
    @������: �ж���
    @�������: �������ģ��
    @����ע��: ESB�ļ�����
    @���:
        @param remotepath str Զ��·��
        @param filename str �����ļ���
        @param localpath str ����·��
    @����:
    @����״̬:
        @return 0 ����ʧ��
        @return 1 ���óɹ�
    @author: Z.H.
    @�����ص�: ����ũ����
    @����ʱ��: 20150924
    '''
    try:
        remotefile = os.path.join(remotepath, filename)
        localfile = os.path.join(localpath, filename)
        rec = esbfile.Py_ftpget(remotefile, localfile)
        if rec != 0:
            return [0, "ESB003", "ESB�ļ�����ʧ��", [None]]
        return [1, None, None, [None]]
    except Exception as e:
        return [0, "ESB004", str(e), [None]]


if __name__ == '__main__':
    # ע��Զ��Ŀ¼Ҫ�� /IFS/
    while 1:
        print(B_ftpput("/home/afa/user/xx/c/esb_file/src", "mk.sh", "/IFS"))
        B_ftpget("/IFS/", "mk.sh", "/home/afa/user/xx/c/esb_file/src/")
        time.sleep(1)