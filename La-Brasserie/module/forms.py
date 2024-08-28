from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, IntegerField, DateField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from module.models import User, Item

room_types = Item.query.all()

choices = [(room_type.name) for room_type in room_types]

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30)])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    phone_number = StringField(label='Phone Number:', validators=[DataRequired()])
    submit = SubmitField(label='Create the Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class BookForm(FlaskForm):
    first_name = StringField(label='First Name:', validators=[DataRequired()])
    last_name = StringField(label='Last Name:', validators=[DataRequired()])
    room_type = SelectField(label='Room Type:', choices=choices ,validators=[DataRequired()])
    start_date = DateField(label='Date of Check In:', validators=[DataRequired()])
    end_date = DateField(label='Date of Check Out:', validators=[DataRequired()])
    phone_number = StringField(label='Phone Number:', validators=[DataRequired()])
    submit = SubmitField(label='Reserve')

class OffersForm(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    description = StringField(label='Description:', validators=[DataRequired()])
    code = StringField(label='Code:', validators=[DataRequired()])
    end_date = DateField(label='End Date:', validators=[DataRequired()])
    price = IntegerField(label='Price:', validators=[DataRequired()])
    submit = SubmitField(label='Add')

class FacilitiesForm(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    description = StringField(label='Description:', validators=[DataRequired()])
    code = StringField(label='Code:', validators=[DataRequired()])
    end_date = DateField(label='End Date:', validators=[DataRequired()])
    price = IntegerField(label='Price:', validators=[DataRequired()])
    submit = SubmitField(label='Add')

class ItemForm(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    description = StringField(label='Description:', validators=[DataRequired()])
    code = StringField(label='Code:', validators=[DataRequired()])
    quantity = IntegerField(label='Quantity:', validators=[DataRequired()])
    price = IntegerField(label='Price:', validators=[DataRequired()])
    submit = SubmitField(label='Add')



class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')

