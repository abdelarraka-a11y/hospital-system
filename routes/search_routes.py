from flask import Blueprint, render_template, request, session, redirect
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.billing import Billing

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search():

    if not session.get('user_id'):
        return redirect('/auth/login')

    query = request.args.get('q')

    patients = Patient.query.filter(Patient.name.contains(query)).all() if query else []
    doctors = Doctor.query.filter(Doctor.name.contains(query)).all() if query else []
    appointments = Appointment.query.filter(Appointment.reason.contains(query)).all() if query else []
    billings = Billing.query.filter(Billing.patient_name.contains(query)).all() if query else []

    return render_template(
        "search/results.html",
        query=query,
        patients=patients,
        doctors=doctors,
        appointments=appointments,
        billings=billings
    )