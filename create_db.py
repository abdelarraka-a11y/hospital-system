from app import app
from models.db import db
from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.billing import Billing

with app.app_context():
    db.create_all()
    print("Database updated: all tables ready")