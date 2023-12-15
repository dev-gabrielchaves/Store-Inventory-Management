from flask import session
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from app.products.models import Product

def validate_product_name(form, product_name):
        product = Product.query.filter_by(user_id=session.get('id'), name=product_name.data).first()
        if product:
            raise ValidationError('This product was already registered in the system.')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), validate_product_name])
    family = StringField('Type', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=0, max=1000)])
    submit = SubmitField('Add Product')