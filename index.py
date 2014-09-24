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
    (clientsocket, address) = serversocket.accept()
    while True:
        item = messages.get()
        send_data(clientsocket, str(item).encode('ascii'))

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
    messages.put(request.args.get('CallSid'))
    response = make_response(render_template("Response.xml"))
    response.headers['Content-Type'] = "text/xml"
    return response

if __name__ == '__main__':
    threading.Thread(target=socket_handler).start()
    print("I'm still going")
    app.run()
