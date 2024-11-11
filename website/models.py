from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Ensure this is defined
    password = db.Column(db.String(150), nullable=False)
  

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    medical_records = db.Column(db.Text)
    appointments_list = db.relationship('Appointment', cascade='all, delete-orphan', back_populates='assigned_patient')

class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact_info = db.Column(db.String(200))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    status = db.Column(db.String(50))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    date = db.Column(db.DateTime, nullable=False)  # This should be a Date field, or DateTime if you need time too

    caregiver = db.relationship('Caregiver', backref='appointments')
    patient = db.relationship('Patient', backref='appointments')
    assigned_patient = db.relationship('Patient', back_populates='appointments_list')

    def __repr__(self):
        return f'<Appointment {self.id}>'