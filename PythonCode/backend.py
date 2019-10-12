from flask import Flask

app = Flask(__name__)

@app.route('/<name>')
def index(name):
    return '<h1>Hello {}!</h1>'.format(name)

<<<<<<< HEAD
    #Nick Commit
=======
#this is a test
>>>>>>> bd46894e26f8d4e787e40849a62814fe98e7db7c
