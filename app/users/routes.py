from flask import Blueprint, session, flash, redirect, url_for, render_template
from app import db, bcrypt
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__, template_folder='templates', static_folder='static')

@users.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('id'):
        flash('You are already registered!', 'warning')
        return redirect(url_for('products.store_management'))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("You've been registered successfully!", 'success')
            return redirect(url_for('users.login'))
        return render_template('register.html', form=form)

@users.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('id'):
        flash('You are already logged in!', 'warning')
        return redirect(url_for('products.store_management'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session['id'] = user.id
                session['username'] = user.username
                session['email'] = user.email
                return redirect(url_for('products.store_management'))
            else:
                flash("Couldn't find the user. Please check your email and password.", 'error')
        return render_template('login.html', form=form)

@users.route('/logout')
def logout():
    if session.get('id'):
        session.clear()
        return redirect(url_for('main.home'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('users.login'))