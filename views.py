from sensorsapi import app
from models import *
from flask import jsonify, request, render_template, url_for, redirect


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('list_entries'))


@app.route('/api/entries', methods=['GET'])
def get_entries():
    entries = []
    for entry in SensorsEntry.query.order_by(SensorsEntry.timestamp.desc()):
        entries.append(entry.export_data())

    return jsonify({'entries': entries})


@app.route('/api/latest', methods=['GET'])
def get_latest_entries():
    last_entries = []
    for entry in SensorsEntry.query.order_by(SensorsEntry.timestamp.desc()).limit(10):
        last_entries.append(entry.export_data())

    return jsonify({'entries': last_entries})


@app.route('/api/entries/<id>', methods=['GET'])
def get_entry(id):
    return jsonify(SensorsEntry.query.get_or_404(id).export_data())


@app.route('/api/entries', methods=['POST'])
def post_entry():
    entry = SensorsEntry()
    entry.import_data(request.json)
    authorized_serial_no = Device.authorize(entry.credentials)
    if authorized_serial_no:
        entry.device_serial_no = authorized_serial_no
        db.session.add(entry)
        db.session.commit()
        return jsonify(entry.export_data()), 201


@app.route('/entries', methods=['GET'])
def list_entries():
    last_entries = SensorsEntry.query.order_by(SensorsEntry.timestamp.desc()).limit(10)
    all_entries = SensorsEntry.query.order_by(SensorsEntry.timestamp.desc())
    return render_template('index.html', last_entries=last_entries, all_entries=all_entries)