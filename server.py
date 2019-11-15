from bottle import request, response, run
from bottle import post, get, put, delete

import model

#import json
#import threading
#import time
import sys

SIZE_MEMORIA = 5

API_BASE_URL = 'http://localhost:'

MAXIMO_DE_PORTAS = 50010

MINIMO_DE_PORTAS = 50000

PORTA_API= 5000 + int(sys.argv[1])

NODOS_VIZINHOS = [PORTA_API]

@get('/alive')
def alive():
    [request.get(API_BASE_URL + str(porta) + '/' ) for porta in range(MINIMO_DE_PORTAS, MAXIMO_DE_PORTAS, 1) if porta != PORTA_API]

@get('')

@post('/inscricao')
def inscricao():
    
    inscrito = model.Inscrito(  request.query.nome,
                                request.query.email,
                                request.query.matricula)

    print(inscrito.matricula)
    #if True:
    #    return response(status=200)
    #else: 
    #    return response(status=204)
     

@get('/todos-inscritos') # or @route('/login')
def todos_inscritos():
    return "Todos os inscritos"

@get('/inscrito') # or @route('/login')
def inscrito():
    return "Um inscrito! "  



run(host='localhost', port=PORTA_API, debug= True)
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