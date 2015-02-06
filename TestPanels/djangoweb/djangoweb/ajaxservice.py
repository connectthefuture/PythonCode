from django.http import HttpResponse, HttpResponseRedirect
import logging
import ajaxfunc
import json

logger = logging.getLogger("djangoweb.app")

def ajaxservice(request, transcode):
    if request.method == 'POST':
        logger.debug(request.body)
        jsn = json.loads(request.body)
        func = getattr(ajaxfunc, 'Tran' + transcode.encode('gbk'))
        kv = func(jsn)
        logger.debug(str(kv))
        return HttpResponse(json.dumps(kv))
    elif request.method == 'GET':
        pass
