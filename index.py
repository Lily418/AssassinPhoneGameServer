from flask import *
import threading
import socket
import queue
app = Flask(__name__)

messages = queue.Queue()

def socket_handler():
    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', 3500))
    serversocket.listen(5)
    #accept connections from outside
    accept_and_send(serversocket)



def accept_and_send(serversocket):
    try:
        (clientsocket, address) = serversocket.accept()
        while True:
            try:
                item = messages.get(True, 2)
                d = send_data(clientsocket, str(item).encode('ascii'))
            except queue.Empty:
                d = send_data(clientsocket, "ping".encode('ascii'))
    except BrokenPipeError:
        accept_and_send(serversocket);

def send_data(sock, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/voice')
def voice():
    f = open('nums.txt', 'a+')
    f.write(str(request.args.get('From')) + "\n")
    f.close()
    messages.put(request.args.get('CallStatus'))
    response = make_response(render_template("Response.xml"))
    response.headers['Content-Type'] = "text/xml"
    return response

@app.route('/status')
def status():
    messages.put(request.args.get('CallStatus'))
    return "";

if __name__ == '__main__':
    threading.Thread(target=socket_handler).start()
    print("I'm still going")
    app.run(host='0.0.0.0', debug=True)
