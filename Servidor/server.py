from bottle import request, response, run
from bottle import Bottle, post, get, redirect, HTTPResponse
import requests
import json
import threading
import time
import sys
from model import Inscrito

SHARE = 0



START = 1
END = 5
 
SIZE_MEM = 5

MAX_OF_PORT = 5010

MIN_OF_PORT = 5000

PORT_API = MIN_OF_PORT + int(sys.argv[1])

API_BASE_URL = 'http://localhost:'

server_node = [PORT_API]

mem = [0,0,0,0,0]

app = Bottle()


def alive():
    global SHARE
    time.sleep(5)
    while True:
        for port in range(MIN_OF_PORT, MAX_OF_PORT, 1):
            if port not in server_node:
                try:
                    r = requests.get(API_BASE_URL + str(port) + '/live')  
                    if add_server_know(port):
                        SHARE = 1
                    
                except requests.exceptions.ConnectionError:
                    pass
        is_new_server()
        time.sleep(15)

def is_new_server():
    global SHARE
    if SHARE == 1:
        share_memory()
        update_memory()
        print("Start-mem: {} End-mem: {} Dados: {}".format(START, END, mem ))
    SHARE = 0

def share_memory():
    global START, END , SIZE_MEM
    server_node.sort()
    
    x = [ (i+1) for i in range(len(server_node)) if PORT_API == server_node[i]]

    SIZE_MEM = len(server_node) * 5
    START = ((x[0] - 1)  * 5) + 1
    END = (x[0] * 5) 

def update_memory():
    for port in server_node:
        if port != PORT_API:
            try:
                r = requests.get(API_BASE_URL + str(port) + '/updateMemory')  
                print(r.text)
            except requests.exceptions.ConnectionError:
                print("Sem Contato {}.".format(port))

@app.route('/updateMemory')            
def updateMemory():
    share_memory()
    print("Start-mem: {} End-mem: {} Dados: {}".format(START, END, mem ))
    print('Shared memory. ')
    #update_memory()


def add_server_know(port):
    if port not in server_node:
        server_node.append(port)
        print('Server {} add'.format(port))
        return True

@app.route('/live')
def live():
    return json.dumps("Server live {} ".format(PORT_API))

@app.route('/receive', method='POST')
def receive():
    inscrito = Inscrito(  request.query.nome,
                                request.query.email,
                                request.query.matricula)
    insert(inscrito)

    
@app.route('/inscricao', method= 'POST')
def inscricao():
    print("size memoria {}".format(SIZE_MEM))
    inscrito = Inscrito(  request.query.nome,
                                request.query.email,
                                request.query.matricula)
    print(inscrito.matricula)
    
    if is_insert_local(inscrito.matricula):
        print('>> Insert local ')
        insert(inscrito)
    else:
        print(">> Insert em outro nodo")
        ind = int(hash(inscrito.matricula) / 5) + 1
        port = server_node[ind - 1] 
        print("Port: {}".format(port))

        if port != PORT_API:    
            try:
                r = requests.post(API_BASE_URL + str(port) + '/receive?nome=' + inscrito.nome + '&email=' + inscrito.email + '&matricula=' + inscrito.matricula) 
            except requests.exceptions.ConnectionError:
                print("Sem Contato {}.".format(port))        
        time.sleep(5)
    

def insert(inscrito):
    ind_normalized = hash(inscrito.matricula) % 5
    ind_zeros = [i for i in range(len(mem)) if mem[i] == 0]

    if(len(ind_zeros) == 0):
        server_node.sort()
        for port in server_node:
            if port != PORT_API:    
                try:
                    r = requests.post(API_BASE_URL + str(port) + '/receive?nome=' + inscrito.nome + '&email=' + inscrito.email + '&matricula=' + inscrito.matricula) 
                    break
                except requests.exceptions.ConnectionError:
                    print("Sem Contato {}.".format(port))        
    elif(ind_normalized in ind_zeros):
        mem[ind_normalized] = inscrito
    else:
        mem[ind_zeros[0]] = inscrito
    
    print("Dados: {}".format(mem))



def is_insert_local(value):
    return (hash(value)>= (START - 1) and hash(value) <= (END - 1))


def hash(value):
    print("Hash: {}".format(int(value) % SIZE_MEM))
    return (int(value) % SIZE_MEM)

@app.route('/todos-inscritos', method='GET') # or @route('/login')
def todos_inscritos():
    dados = []
    [dados.append(m) for m in mem if m !=0 ]
    
    text = ' '
    for port in server_node:
        if PORT_API != port:
            r = requests.get(API_BASE_URL + str(port) + '/inscrito')
            text = text + ' ' + r.text
            
    
    for d in dados:
        text = text + ' ' + d.nome + ";" + d.email + ";" + d.matricula + ","
    
    text.replace('"', ' ')
    theBody = json.dumps({'text': text}) # you seem to want a JSON response
    return HTTPResponse(status=200, body=theBody)


@app.route('/inscrito') # or @route('/login')
def inscrito():
    dados = []
    [ dados.append(m) for m in mem if m != 0]
    text = ' '
    for d in dados :
        text  = text +' '+  d.nome + ';' + d.email + ';' + d.matricula + "," 

    return json.dumps(text)


try:
    t1 = threading.Thread(target=alive)
    t1.start()

    #t2 = threading.Thread(target=receive)
    #t2.start()
except:
     print("Error at started thread.  ")

run(app,host='localhost', port=PORT_API, debug= False, reloader=False)

