from flask import Blueprint, session, redirect, url_for, render_template

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def home():
    if session.get('id'):
        return redirect(url_for('products.store_management'))
    else:    
        return render_template('home.html')