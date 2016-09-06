from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from errorhandlers import *
from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')
