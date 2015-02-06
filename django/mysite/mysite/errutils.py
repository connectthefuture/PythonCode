__author__ = 'ZT-ZH'

def error(errorcode, errormsg, transcode = None):
    return render_to_response('error.html', {'errorcode' : errorcode, 'errormsg' : errormsg})