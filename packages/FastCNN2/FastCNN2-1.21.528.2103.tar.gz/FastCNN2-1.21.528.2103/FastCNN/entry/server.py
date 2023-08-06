from flask import Flask,session
from flask_restful import Api,Resource
from flask_cors import *
import datetime,os

debug = False
if os.path.exists("./debug"):
    sys.path.insert(os.path.abspath("../"))
    debug = True

"""
import api
"""
#from package.namespace.demo_ import DemoApi


app = Flask(__name__,static_folder='static/',template_folder='static/template/')
api = Api(app)
CORS(app, supports_credentials=True)

host = '0.0.0.0'
"""
set port
"""
port = 7777


app.config['SECRET_KEY'] = 'myskey'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)

"""
set api url
"""
#api.add_resource(DemoApi,'/api/namespace/demo')


def main():
    app.run(host = host,port = port,debug = debug)

if __name__ == "__main__":
    main()
