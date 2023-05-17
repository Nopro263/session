from flask import Flask, request
import session as _session

app = Flask(__name__)
session = _session.Session()


@app.route('/')
@session.require_auth
def hello_world():
    data = session.get_data(request)
    for x, y in request.args.items():
        data[x] = y
    res = "Data: " + str(data)
    return res


@app.route('/login')
def login():
    session.setloggedin(request, True)
    return b"OK"


@app.route('/logout')
def logout():
    session.setloggedin(request, False)
    return b"OK"


@app.before_request
def b():
    return session.before_request(request)


if __name__ == '__main__':
    app.run()
