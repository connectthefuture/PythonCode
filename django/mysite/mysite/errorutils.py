from django.shortcuts import render_to_response

def error(errorcode, errormsg, transcode = None):
    return render_to_response('public/error.html', {'errorcode' : errorcode, 'errormsg' : errormsg})