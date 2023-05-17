# session

a simple tool to manage Sessions

## Usage
````python
import session
s = session.Session(cookie_name="example-session", 
                    http_only=False)
````
creates a Session Object

````python
import session
s = session.Session(cookie_name="example-session", 
                    http_only=False)
@app.before_request
def x():
    s.before_request(request)
````
assigns every user a session-cookie


````python
import session
s = session.Session(cookie_name="example-session", 
                    http_only=False)
@app.route("/")
@s.require_auth
def y:
    ...
@app.before_request
def x():
    s.before_request(request)
````
requires the user to be signed in

````python
import session
s = session.Session(cookie_name="example-session", 
                    http_only=False)
s.setloggedin(request, True)

@app.route("/")
@s.require_auth
def y:
    ...
@app.before_request
def x():
    s.before_request(request)
````
logges the user in / out

````python
import session
s = session.Session(cookie_name="example-session", 
                    http_only=False)
s.setloggedin(request, True)

@app.route("/")
@s.require_auth
def y:
    data = s.get_data(request)
    ...
@app.before_request
def x():
    s.before_request(request)
````
gets the users data. data is a empty dict which is unique to every session