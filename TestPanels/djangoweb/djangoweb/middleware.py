class disablecsrf:
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

class check_login:
    def process_request(self, request):
        if request.POST.get('User') is None:
            pass
