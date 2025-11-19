from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from app.models import User, Product

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Administrator'), ('staff', 'Cashier')], validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email address is already registered.')
        
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class AddUserForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Administrator'), ('staff', 'Cashier')], validators=[DataRequired()])
    submit = SubmitField('Add User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email address is already registered.')

class EditUserForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('admin', 'Administrator'), ('staff', 'Cashier')], validators=[DataRequired()])
    password = PasswordField('New Password (leave blank to keep current)', validators=[Optional(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[Optional()])
    submit = SubmitField('Update User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != self.user_id:
            raise ValidationError('This email address is already in use.')
    
    def validate_confirm_password(self, confirm_password):
        if self.password.data and self.password.data != confirm_password.data:
            raise ValidationError('Passwords must match.')




class AddProductForm(FlaskForm):
    product_code = StringField('Product Code', validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=50)])
    price = FloatField('Price (ZAR)', validators=[DataRequired(), NumberRange(min=0.01)])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')

    def validate_product_code(self, product_code):
        product = Product.query.filter_by(product_code=product_code.data).first()
        if product:
            raise ValidationError('This product code already exists.')

class EditProductForm(FlaskForm):
    product_code = StringField('Product Code', validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=50)])
    price = FloatField('Price (ZAR)', validators=[DataRequired(), NumberRange(min=0.01)])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Update Product')

    def validate_product_code(self, product_code):
        product = Product.query.filter_by(product_code=product_code.data).first()
        if product and product.id != self.product_id:
            raise ValidationError('This product code already exists.')


class SearchProductForm(FlaskForm):
    search_query = StringField('Search by Name or Product Code', validators=[Optional(), Length(min=1, max=100)])
    submit = SubmitField('Search')


class AddToCartForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=10000)])
    submit = SubmitField('Add to Cart')


class UpdateCartForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=10000)])
    submit = SubmitField('Update')


class CheckoutForm(FlaskForm):
    payment_method = SelectField('Payment Method', 
                                 choices=[('cash', 'Cash'), ('card', 'Card')], 
                                 validators=[DataRequired()])
    submit = SubmitField('Complete Sale')





