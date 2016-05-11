from wsgiref.simple_server import make_server


def simple_app(environ, start_response):
    status = '200 OK'
    for key in environ:
        print key, environ[key]
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [u"This is hello wsgi app".encode('utf8'), ]


if __name__ == "__main__":
    httpd = make_server('', 8001, simple_app)
    print "Serving on port 8000..."
    httpd.serve_forever()
