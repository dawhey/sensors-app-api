from sensorsapi import app
from models import *
from flask import jsonify, request


@app.route('/')
def index():
    return '<h1>Sensors API</h1> <h2> (currently in development) </h2>'


@app.route('/entries', methods=['GET', 'POST'])
def entries():
    if request.method == 'GET':
        entries = []
        for entry in SensorsEntry.query.all():
            entries.append(entry.export_data())
        return jsonify({'entries': entries})

    elif request.method == 'POST':
        return 'Not implemented'


@app.route('/entries/<id>', methods=['GET'])
def get_entry(id):
    return jsonify(SensorsEntry.query.get_or_404(id).export_data())
