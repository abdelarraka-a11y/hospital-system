from flask import Blueprint, render_template, request, redirect, session, flash
from models.patient import Patient
from models.db import db

patient_bp = Blueprint('patient', __name__)


def login_required():
    return session.get('user_id')


def admin_required():
    return session.get('role') == "admin"


# LIST + SEARCH
@patient_bp.route('/patients')
def patients():

    if not login_required():
        flash("Login required")
        return redirect('/auth/login')

    search = request.args.get('search')

    if search:
        all_patients = Patient.query.filter(
            Patient.name.contains(search)
        ).all()
    else:
        all_patients = Patient.query.all()

    return render_template(
        "patients/list.html",
        patients=all_patients
    )


# ADD
@patient_bp.route('/patients/add', methods=['GET', 'POST'])
def add_patient():

    if not login_required():
        flash("Login required")
        return redirect('/auth/login')

    if request.method == 'POST':

        new_patient = Patient(
            name=request.form['name'],
            age=request.form['age'],
            gender=request.form['gender'],
            phone=request.form['phone']
        )

        db.session.add(new_patient)
        db.session.commit()

        flash("Patient added")
        return redirect('/patients')

    return render_template("patients/add.html")


# DELETE
@patient_bp.route('/patients/delete/<int:id>')
def delete_patient(id):

    if not login_required():
        flash("Login required")
        return redirect('/auth/login')

    if not admin_required():
        flash("Admin only action")
        return redirect('/patients')

    patient = Patient.query.get(id)

    db.session.delete(patient)
    db.session.commit()

    flash("Patient deleted")
    return redirect('/patients')


# EDIT
@patient_bp.route('/patients/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    if not login_required():
        flash("Login required")
        return redirect('/auth/login')

    if not admin_required():
        flash("Admin only action")
        return redirect('/patients')

    patient = Patient.query.get(id)

    if request.method == 'POST':

        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.gender = request.form['gender']
        patient.phone = request.form['phone']

        db.session.commit()

        flash("Patient updated")
        return redirect('/patients')

    return render_template("patients/edit.html", patient=patient)