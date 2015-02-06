import models
import logging

logger = logging.getLogger("djangoweb.app")

def Tran1000(imp):
    project = imp[u'project']
    exp = {}
    try:
        result = models.ProjectDef.objects.get(project=project)
        for key in ('project', 'projectname', 'msgtype', 'trancodexpath', 'serialnoxpath'):
            exp[key] = getattr(result, key)
        exp['RspCode'] = '0000'
    except Exception as e:
        exp['RspCode'] = '0100'
    return exp