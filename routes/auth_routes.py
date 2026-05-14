from flask import Blueprint, render_template, request, redirect, session, flash
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # If already logged in → go dashboard
    if session.get('user_id'):
        return redirect('/dashboard')

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.verify(username, password)

        if user:
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            flash("Login successful")
            return redirect('/dashboard')

        flash("Invalid credentials")

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():

    session.clear()
    flash("Logged out successfully")

    return redirect('/auth/login')