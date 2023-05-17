from flask import Request, Response, request
import random
import string


class Session:
    """Represents a Session-Manager, should be global"""
    cookie_name = "SESSION"
    http_only = True
    _data = {}

    def require_auth(self, func):
        """Annotation to require a valid SESSION cookie"""
        s = self

        def f(*args):
            nonlocal func, s
            data = s._get_data(request)
            if data is None or \
                    "logged_in" not in data or \
                    not data["logged_in"]:
                return Response("Forbidden", 403)
            return func(*args)

        f.__name__ = func.__name__
        return f

    def _get_data(self, req: Request):
        """gets the raw data, ought not to be used"""
        if self.cookie_name not in req.cookies.keys():
            return None
        if req.cookies.get(self.cookie_name) not in self._data.keys():
            return None
        return self._data[req.cookies.get(self.cookie_name)]

    def get_data(self, req: Request):
        """gets the data pointed to by the user's cookie"""
        d = self._get_data(req)
        if d is None:
            return None

        return d['data']

    def setloggedin(self, req: Request, b: bool):
        """states if the user should be considered to be logged in"""
        d = self._get_data(req)
        if d is not None:
            d["logged_in"] = b

    def before_request(self, req: Request):
        """ought to be called in app.before_request. Initializes the SESSION cookie"""
        if self.cookie_name not in req.cookies.keys() or req.cookies.get(self.cookie_name) not in self._data.keys():
            r = Response()
            ses = self._generate_secure_string(10)
            r.set_cookie(self.cookie_name,
                         ses,
                         None,
                         httponly=self.http_only)
            r.location = req.url
            r.status = 302
            self._data[ses] = {"data": {}, "logged_in": False}
            return r

    def _generate_secure_string(self, _len=10):
        code = "".join([random.choice(string.ascii_letters) for _ in range(_len)])
        while code in self._data:
            code = "".join([random.choice(string.ascii_letters) for _ in range(_len)])

        return code

