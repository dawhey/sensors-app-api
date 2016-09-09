from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sensorsapi import app
import datetime

db = SQLAlchemy(app)


class ValidationError(ValueError):
    pass


class AuthorizationError(ValueError):
    pass


class ApiError:
    def __init__(self, status, error, message):
        self.status = status
        self.error = error
        self.message = message

    def export(self):
        error = {'status': self.status,
                 'error': self.error,
                 'message': self.message
                 }
        return error


class Device(db.Model):
    __tablename__ = 'devices'

    serial_no = db.Column(db.String, primary_key=True, unique=True)
    device_name = db.Column(db.String)
    password_hash = db.Column(db.String(128))

    def __init__(self, serial_no, password, device_name='Rapberry Pi'):
        self.device_name = device_name
        self.serial_no = serial_no
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256:100000')

    def __repr__(self):
        print(self.device_name + ' serial no. ' + self.serial_no)

    @staticmethod
    def authorize(serial_no, password):
        device = Device.query.filter(Device.serial_no == serial_no).first()
        if device is not None:
            authorized = check_password_hash(device.password_hash, password)
            if authorized:
                return True
            else:
                return AuthorizationError("Wrong password for serial number: " + serial_no)
        else:
            return AuthorizationError("Device with this serial number does not exist")


class SensorsEntry(db.Model):
    __tablename__ = 'sensors_entries'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=True, default=datetime.datetime.now())
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

    def __init__(self, timestamp=datetime.datetime.now(), temperature=0.0, humidity=0.0):
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
