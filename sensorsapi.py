from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dawhey:password@localhost/sensorsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')