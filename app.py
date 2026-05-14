from flask import Flask, render_template, session, redirect

from models.db import db

from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.billing import Billing

from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.appointment_routes import appointment_bp
from routes.billing_routes import billing_bp
from routes.search_routes import search_bp


app = Flask(__name__)

# =========================
# CONFIG
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret"

db.init_app(app)

# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(search_bp)


# =========================
# HOME
# =========================
@app.route('/')
def home():
    return redirect('/auth/login')


# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
def dashboard():

    if not session.get('user_id'):
        return redirect('/auth/login')

    stats = {
        "patients": Patient.query.count(),
        "doctors": Doctor.query.count(),
        "appointments": Appointment.query.count(),
        "billings": Billing.query.count()
    }

    chart_data = {
        "labels": ["Patients", "Doctors", "Appointments", "Billing"],
        "values": [
            stats["patients"],
            stats["doctors"],
            stats["appointments"],
            stats["billings"]
        ]
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        chart_data=chart_data,
        role=session.get('role')
    )


# =========================
# DEPLOY FIX (IMPORTANT)
# =========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)