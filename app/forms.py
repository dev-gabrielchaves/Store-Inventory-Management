from flask import session
from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError, NumberRange
from app.models import User, Product

def validate_username(form, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username was already choosen. Please type another one.')
    
def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('This email is already in use. Please type another one.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=20), DataRequired(), validate_username])
    email = EmailField('Email', validators=[DataRequired(), validate_email])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

def validate_product_name(form, product_name):
        product = Product.query.filter_by(user_id=session.get('id'), name=product_name.data).first()
        if product:
            raise ValidationError('This product was already registered in the system.')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), validate_product_name])
    family = StringField('Type', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=0, max=1000)])
    submit = SubmitField('Add Product')