from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/voice')
def voice():
    response = make_response(render_template("Response.xml"))
    response.headers['Content-Type'] = "text/xml"
    return response
    
if __name__ == '__main__':
    app.run()
