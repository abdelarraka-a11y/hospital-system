from flask import Blueprint, render_template, request, redirect, session, flash
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor
from models.db import db

appointment_bp = Blueprint('appointment', __name__)


def login_required():
    return session.get('user_id')


def admin_required():
    return session.get('role') == "admin"


# LIST
@appointment_bp.route('/appointments')
def appointments():

    if not login_required():
        return redirect('/auth/login')

    all_appointments = Appointment.query.all()

    return render_template(
        "appointments/list.html",
        appointments=all_appointments
    )


# ADD
@appointment_bp.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():

    if not login_required():
        return redirect('/auth/login')

    patients = Patient.query.all()
    doctors = Doctor.query.all()

    if request.method == 'POST':

        new_app = Appointment(
            patient_id=request.form['patient_id'],
            doctor_id=request.form['doctor_id'],
            date=request.form['date'],
            reason=request.form['reason']
        )

        db.session.add(new_app)
        db.session.commit()

        flash("Appointment created")

        return redirect('/appointments')

    return render_template(
        "appointments/add.html",
        patients=patients,
        doctors=doctors
    )


# DELETE
@appointment_bp.route('/appointments/delete/<int:id>')
def delete_appointment(id):

    if not login_required():
        return redirect('/auth/login')

    if not admin_required():
        flash("Admin only")
        return redirect('/appointments')

    appointment = Appointment.query.get(id)

    db.session.delete(appointment)
    db.session.commit()

    flash("Appointment deleted")

    return redirect('/appointments')


# EDIT
@appointment_bp.route('/appointments/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):

    if not login_required():
        return redirect('/auth/login')

    if not admin_required():
        flash("Admin only")
        return redirect('/appointments')

    appointment = Appointment.query.get(id)

    patients = Patient.query.all()
    doctors = Doctor.query.all()

    if request.method == 'POST':

        appointment.patient_id = request.form['patient_id']
        appointment.doctor_id = request.form['doctor_id']
        appointment.date = request.form['date']
        appointment.reason = request.form['reason']

        db.session.commit()

        flash("Appointment updated")

        return redirect('/appointments')

    return render_template(
        "appointments/edit.html",
        appointment=appointment,
        patients=patients,
        doctors=doctors
    )