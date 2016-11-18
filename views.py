# -*- coding: utf-8 -*-
from pyfcm import FCMNotification
from sensorsapi import app
from models import *
from flask import jsonify, request, render_template, url_for, redirect
import os


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('list_entries'))


@app.route('/api/entries', methods=['GET'])
def get_entries():
    entries = []
    for entry in SensorsEntry.query.order_by(SensorsEntry.timestamp.asc()):
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
        entry.notify_user()
        db.session.add(entry)
        db.session.commit()
        notify_user_about_entry(entry)
        return jsonify(entry.export_data()), 201


@app.route('/entries', methods=['GET'])
def list_entries():
    last_entries = SensorsEntry.query.order_by(SensorsEntry.timestamp.desc()).limit(10)
    all_entries = SensorsEntry.query.order_by(SensorsEntry.timestamp.desc())
    return render_template('index.html', last_entries=last_entries, all_entries=all_entries)


@app.route('/notify', methods=['POST'])
def send_warning():
    data = request.json
    push_service = FCMNotification(api_key=os.environ['FCM_KEY'])
    credentials = Credentials(serial_no=data['serial_no'], password=data['password'])
    authorized_serial_no = Device.authorize(credentials)

    if authorized_serial_no:
        result = push_service.notify_topic_subscribers(tag=2, topic_name="warnings", color="#E64A19",
                                                       message_body=data['message_body'],
                                                       message_title="Warning!")
        return jsonify(result), 200


def notify_user_about_entry(entry):
    data = 'Temp: {0}℃   Hum: {1}%'.format(round(entry.temperature, 2), round(entry.humidity, 1))
    push_service = FCMNotification(api_key=os.environ['FCM_KEY'])
    result = push_service.notify_topic_subscribers(tag=1, topic_name="warnings", color="#E64A19",
                                                   message_body=entry.timestamp.strftime("%d %B %H:%M"),
                                                   message_title=data)
    return result
