#coding=gbk

def parseCoreFile(filename, req):
    '''
    @�������: �������ķ����ļ�
    @������: �ж���
    @�������: �������ģ��
    @����ע��: �������ķ����ļ�
    @���:
        @param filename         str         �ļ���
    @����:
        @param req              dict        �ֵ�
    @����״̬:
        @return 0 ʧ��
        @return 1 �ɹ�
    @��    ��: ZH
    @����ʱ��: 2014-10-16
    @ʹ�÷���:
    '''
    begintag, endtag = False, False
    fld_lst = list()
    map = dict()
    line_row = list()
    try:
        with open (filename) as fd:
            for line in fd:
                line = line.lstrip();
                if line[0] == '{':
                    begintag = True
                if line[0] == '}':
                    endtag = True
                if begintag and line.startswith('fld='):
                    tmp = line.split('~')
                    field = tmp[0][4:]
                    fld_lst.append(field)
                if endtag and line.count('~') > 0:
                    tmp = [ f.strip('"').strip() for f in line.split('~')]
                    line_row.append(tmp)
            zipped = zip(*line_row)
            for i, field in enumerate(fld_lst):
                map[field] = zipped[i]
        return [1, None, None, [map]]
    except Exception as e:
        return [0, "A01001", str(e), [None]]





