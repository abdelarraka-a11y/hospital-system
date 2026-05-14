from models.db import db

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))

    appointments = db.relationship(
        'Appointment',
        backref='doctor',
        lazy=True,
        cascade="all, delete"
    )