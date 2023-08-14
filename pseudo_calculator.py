"""
This pseudo calculator should support the following operations:

  * Positive
  * Negative

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/positive/5' then the response
body in my browser should be `true`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/positive/5  => 'true'
  http://localhost:8080/positive/0  => 'false'
  http://localhost:8080/positive/-5 => 'false'
  http://localhost:8080/negative/0  => 'false'
  http://localhost:8080/negative/-2 => 'true'
```

"""


def home():
    body = """<html>
    <body>
    <p>Here's how to use this page: </p>
    <p> After localhost:8080, add a slash and choose between positive and negative</p>
    <p> Follow it with another slash then type a random integer to check whether it is positive or negative!</p>
    </body>
    </html>"""
    return body


def positive(args):
    try:
        arg_int = int(args)
        if arg_int > 0:
            response = True
            body = "{}".format(str(response))
        else:
            response = False
            body = "{}".format(str(response))
    except (ValueError, TypeError):
        body = "not a number."

    return body


def negative(args):
    try:
        arg_int = int(args)
        if arg_int < 0:
            response = True
            body = "{}".format(str(response))
        else:
            response = False
            body = "{}".format(str(response))
    except (ValueError, TypeError):
        body = "not a number."

    return body


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments, based on the path.
    """

    funcs = {
        '': home,
        'positive': positive,
        'negative': negative,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
        print(func)
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
