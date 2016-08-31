from sensorsapi import app
from models import *
from flask import jsonify, request


@app.route('/')
def index():
    return '<h1>Sensors API</h1> <h2> (currently in development) </h2>'


@app.route('/entries', methods=['GET'])
def get_entries():
    entries = []
    for entry in SensorsEntry.query.all():
        entries.append(entry.export_data())

    return jsonify({'entries': entries})


@app.route('/entries/<id>', methods=['GET'])
def get_entry(id):
    return jsonify(SensorsEntry.query.get_or_404(id).export_data())


@app.route('/entries', methods=['POST'])
def post_entry():
    entry = SensorsEntry()
    entry.import_data(request.json)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.export_data()), 201
