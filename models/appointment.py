from models.db import db

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patients.id'),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey('doctors.id'),
        nullable=False
    )

    date = db.Column(db.String(50), nullable=False)

    reason = db.Column(db.String(200))