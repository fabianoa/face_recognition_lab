# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
#from .. import db
from ..models import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User()
        user.email=form.email.data
        user.first_name=form.first_name.data
        user.last_name=form.last_name.data
        user.password=form.password.data

        # add employee to the database
        ##db.session.add(employee)
        ##db.session.commit()
        flash('You have successfully registered! You may now login.', 'success')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        user = User()
        user.is_active=True
        user.id=1
        if user is not None and user.verify_password(
                form.password.data):
            # log employee in
            login_user(user)

            # redirect to the appropriate dashboard page
            if user.is_admin:
                return redirect(url_for('face_recognition.detect_face'))
            else:
                return redirect(url_for('home.welcome'))

        # when login details are incorrect
        else:
            flash('Invalid email or password', 'error')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))