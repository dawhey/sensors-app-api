from flask_sqlalchemy import SQLAlchemy
from sensorsapi import app
import datetime

db = SQLAlchemy(app)


class ValidationError(ValueError):
    pass


class SensorsEntry(db.Model):
    __tablename__ = 'sensors_entries'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=True, default=datetime.datetime.utcnow())
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

    def __init__(self, timestamp=datetime.datetime.utcnow(), temperature=0.0, humidity=0.0):
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity

    def __repr__(self):
        print('Entry no. {0} \nTimestamp = {1} \nTemperature = {2} \nHumidity = {3}\n ',
              self.id, self.timestamp, self.temperature, self.humidity)

    def export_data(self):
        data = {
            'id': self.id,
            'timestamp': self.timestamp,
            'temperature': self.temperature,
            'humidity': self.humidity
        }
        return data

    def import_data(self, data):
        try:
            self.timestamp = data['timestamp']
            self.temperature = data['temperature']
            self.humidity = data['humidity']
        except KeyError as e:
            raise ValidationError('Missing key in data ' + e.args[0])
        return self
