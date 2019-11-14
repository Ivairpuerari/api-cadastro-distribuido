from bottle import request, response
from bottle import post, get, put, delete

#import json
#import threading
#import time
import sys

@post('/inscricao')
def inscricao():
    """
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"
    """

@get('/todos-inscritos') # or @route('/login')
def todos_inscritos():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@get('/inscrito') # or @route('/login')
def inscrito():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''


bottle.run(host='localhost', port=int(sys.argv[1]))
"""
peers = sys.argv[2:]

@bottle.route('/inscricao')
def index():
    return json.dumps(peers)

def client():
    time.sleep(5)
    while True:
        time.sleep(1)
        np = []
        for p in peers:
            r = requests.get(p + '/peers')
            np = np + json.loads(r.text)
            print(np)
            time.sleep(1)
        peers[:] = list(set(np + peers))

        print(peers)

t = threading.Thread(target=client)
t.start()

"""