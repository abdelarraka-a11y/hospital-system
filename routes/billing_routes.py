from flask import Blueprint, render_template, request, redirect, session, flash, send_file
from models.billing import Billing
from models.db import db

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os

billing_bp = Blueprint('billing', __name__)


def login_required():
    return session.get('user_id')


def admin_required():
    return session.get('role') == "admin"


# LIST BILLING
@billing_bp.route('/billing')
def billing():

    if not login_required():
        return redirect('/auth/login')

    all_bills = Billing.query.all()

    return render_template("billing/list.html", bills=all_bills)


# ADD BILL
@billing_bp.route('/billing/add', methods=['GET', 'POST'])
def add_bill():

    if not login_required():
        return redirect('/auth/login')

    if not admin_required():
        flash("Admin only")
        return redirect('/billing')

    if request.method == 'POST':

        new_bill = Billing(
            patient_name=request.form['patient_name'],
            amount=request.form['amount'],
            status=request.form['status']
        )

        db.session.add(new_bill)
        db.session.commit()

        flash("Bill created")
        return redirect('/billing')

    return render_template("billing/add.html")


# =========================
# 🧾 PDF INVOICE ROUTE
# =========================
@billing_bp.route('/billing/invoice/<int:id>')
def invoice(id):

    if not login_required():
        return redirect('/auth/login')

    bill = Billing.query.get(id)

    if not bill:
        flash("Bill not found")
        return redirect('/billing')

    file_path = f"invoice_{id}.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    c.drawString(100, 750, "🏥 Hospital Invoice")
    c.drawString(100, 720, f"Patient: {bill.patient_name}")
    c.drawString(100, 700, f"Amount: {bill.amount}")
    c.drawString(100, 680, f"Status: {bill.status}")

    c.save()

    return send_file(file_path, as_attachment=True)