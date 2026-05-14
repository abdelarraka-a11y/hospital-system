from models.db import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))

    appointments = db.relationship(
        'Appointment',
        backref='patient',
        lazy=True,
        cascade="all, delete"
    )