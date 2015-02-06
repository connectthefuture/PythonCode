#coding=gbk

def parseCoreFile(filename, req):
    '''
    @组件名称: 解析核心返回文件
    @组件风格: 判断型
    @组件类型: 横向参数模块
    @中文注释: 解析核心返回文件
    @入参:
        @param filename         str         文件名
    @出参:
        @param req              dict        字典
    @返回状态:
        @return 0 失败
        @return 1 成功
    @作    者: ZH
    @创建时间: 2014-10-16
    @使用范例:
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





