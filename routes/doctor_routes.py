from flask import Blueprint, render_template, request, redirect, session, flash
from models.doctor import Doctor
from models.db import db

doctor_bp = Blueprint('doctor', __name__)


def login_required():
    return session.get('user_id')


def admin_required():
    return session.get('role') == "admin"


# LIST + SEARCH
@doctor_bp.route('/doctors')
def doctors():

    if not login_required():
        return redirect('/auth/login')

    search = request.args.get('search')

    if search:
        all_doctors = Doctor.query.filter(
            Doctor.name.contains(search)
        ).all()
    else:
        all_doctors = Doctor.query.all()

    return render_template(
        "doctors/list.html",
        doctors=all_doctors
    )


# ADD
@doctor_bp.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():

    if not login_required():
        return redirect('/auth/login')

    if not admin_required():
        flash("Admin only")
        return redirect('/doctors')

    if request.method == 'POST':

        new_doctor = Doctor(
            name=request.form['name'],
            specialty=request.form['specialty'],
            phone=request.form['phone']
        )

        db.session.add(new_doctor)
        db.session.commit()

        flash("Doctor added")

        return redirect('/doctors')

    return render_template("doctors/add.html")


# DELETE
@doctor_bp.route('/doctors/delete/<int:id>')
def delete_doctor(id):

    if not login_required():
        return redirect('/auth/login')

    if not admin_required():
        flash("Admin only")
        return redirect('/doctors')

    doctor = Doctor.query.get(id)

    db.session.delete(doctor)
    db.session.commit()

    flash("Doctor deleted")

    return redirect('/doctors')