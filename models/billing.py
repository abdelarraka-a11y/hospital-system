from models.db import db

class Billing(db.Model):
    __tablename__ = "billings"

    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")