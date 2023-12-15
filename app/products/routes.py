from flask import Blueprint, redirect, url_for, render_template, session, flash
from app import db
from app.products.models import Product
from app.products.forms import ProductForm

products = Blueprint('products', __name__, template_folder='templates', static_folder='static')

@products.route('/store-management')
def store_management():
    if session.get('id'):
        products = Product.query.filter_by(user_id=session.get('id'))
        return render_template('store_management.html', products=products)
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('users.login'))

@products.route('/add-product', methods=['POST', 'GET'])
def add_product():
    if session.get('id'):
        form = ProductForm()
        if form.validate_on_submit(): 
            product = Product(name=form.name.data, family=form.family.data, amount=form.amount.data, user_id=session.get('id'))
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('products.store_management'))
        return render_template('add_product.html', form=form)
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('users.login'))

@products.route('/delete-product/<id>')
def delete_product(id):
    if session.get('id'):
        try:
            product = Product.query.filter_by(id=id, user_id=session.get('id')).first()
            db.session.delete(product)
            db.session.commit()
            return redirect(url_for('products.store_management'))
        except:
            flash("Product not found!", 'error')
            return redirect(url_for('products.store_management'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('users.login'))

@products.route('/increase-product-amount/<id>')
def increase_product_amount(id):
    if session.get('id'):
        try:
            product = Product.query.filter_by(id=id, user_id=session.get('id')).first()
            if product.amount == 999:
                flash('The amount can\'t exceed the value of 999.', 'warning')
            else:
                product.amount += 1
                db.session.commit()
            return redirect(url_for('products.store_management'))
        except:
            flash("Product not found!", 'error')
            return redirect(url_for('products.store_management'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('users.login'))

@products.route('/decrease-product-amount/<id>')
def decrease_product_amount(id):
    if session.get('id'):
        try:
            product = Product.query.filter_by(id=id, user_id=session.get('id')).first()
            if product.amount == 0:
                flash('The amount can\'t be less than 0.', 'warning')
            else:
                product.amount -= 1
                db.session.commit()
            return redirect(url_for('products.store_management'))
        except:
            flash("Product not found!", 'error')
            return redirect(url_for('products.store_management'))
    else:
        flash("You haven't logged in yet!", 'error')
        return redirect(url_for('users.login'))