from flask import render_template, redirect, url_for, flash, session, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ProductForm
from app.models import User, Product

@app.route('/')
def home():
    if session.get('id'):
        return redirect(url_for('store_management'))
    else:    
        return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('id'):
        flash('You are already registered!', 'warning')
        return redirect(url_for('store_management'))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("You've been registered successfully!", 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('id'):
        flash('You are already logged in!', 'warning')
        return redirect(url_for('store_management'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session['id'] = user.id
                session['username'] = user.username
                session['email'] = user.email
                return redirect(url_for('store_management'))
            else:
                flash("Couldn't find the user. Please check your email and password.", 'error')
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if session.get('id'):
        session.clear()
        return redirect(url_for('home'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('login'))

@app.route('/store-management')
def store_management():
    if session.get('id'):
        products = Product.query.filter_by(user_id=session.get('id'))
        return render_template('store_management.html', products=products)
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('login'))

@app.route('/add-product', methods=['POST', 'GET'])
def add_product():
    if session.get('id'):
        form = ProductForm()
        if form.validate_on_submit(): 
            product = Product(name=form.name.data, family=form.family.data, amount=form.amount.data, user_id=session.get('id'))
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('store_management'))
        return render_template('add_product.html', form=form)
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('login'))

@app.route('/delete-product/<id>')
def delete_product(id):
    if session.get('id'):
        try:
            product = Product.query.filter_by(id=id, user_id=session.get('id')).first()
            db.session.delete(product)
            db.session.commit()
            return redirect(url_for('store_management'))
        except:
            flash("Product not found!", 'error')
            return redirect(url_for('store_management'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('login'))

@app.route('/increase-product-amount/<id>')
def increase_product_amount(id):
    if session.get('id'):
        try:
            product = Product.query.filter_by(id=id, user_id=session.get('id')).first()
            if product.amount == 999:
                flash('The amount can\'t exceed the value of 999.', 'warning')
            else:
                product.amount += 1
                db.session.commit()
            return redirect(url_for('store_management'))
        except:
            flash("Product not found!", 'error')
            return redirect(url_for('store_management'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('login'))

@app.route('/decrease-product-amount/<id>')
def decrease_product_amount(id):
    if session.get('id'):
        try:
            product = Product.query.filter_by(id=id, user_id=session.get('id')).first()
            if product.amount == 0:
                flash('The amount can\'t be less than 0.', 'warning')
            else:
                product.amount -= 1
                db.session.commit()
            return redirect(url_for('store_management'))
        except:
            flash("Product not found!", 'error')
            return redirect(url_for('store_management'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('login'))