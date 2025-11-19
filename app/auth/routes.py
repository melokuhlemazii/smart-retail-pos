from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm
from app.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful! Welcome to Smart-Retail POS.', 'success')
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('main.staff_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template("login.html", form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=hashed_password,
            role=form.role.data
        )

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in to Smart-Retail POS.', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html", form=form)

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out from Smart-Retail POS.', 'info')
    return redirect(url_for('main.landing'))



