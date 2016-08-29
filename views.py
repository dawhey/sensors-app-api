from sensorsapi import app

@app.route('/')
def index():
    return '<h1>test</h1>'
