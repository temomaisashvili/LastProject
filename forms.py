from flask_wtf import FlaskForm
from wtforms import FormField
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, \
    IntegerField, TextAreaField, SelectMultipleField, FileField
from wtforms.validators import data_required, length, email, ValidationError
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):

    email = EmailField('Email', validators=[data_required(), email()],
                       render_kw={'placeholder': 'შეიყვანეთ ემეილი', 'class': 'form-control'})
    password = PasswordField('Password', validators=[data_required()],
                             render_kw={'class': 'form-control', 'placeholder': 'შეიყვანეთ პაროლი'})
    submit = SubmitField('Login', render_kw={'class': 'btn btn-primary', 'style': 'text-align: center;'})


class RegistrationForm(LoginForm):
    first_name = StringField('First Name', validators=[data_required()],
                             render_kw={'placeholder': 'შეიყვანეთ სახელი', 'class': 'form-control'})
    last_name = StringField('Last Name', validators=[data_required()],
                            render_kw={'placeholder': 'შეიყვანეთ გვარი', 'class': 'form-control'})
    age = IntegerField('Age', validators=[data_required()], render_kw={'class': 'form-control',
                                                                       'placeholder': 'შეიყვანეთ ასაკი'})
    address = StringField('Address', validators=[data_required()],
                          render_kw={'placeholder': 'შეიყვანეთ მისამართ', 'class': 'form-control'})
    submit = SubmitField('Registration', render_kw={'class': 'btn btn-primary', 'style': 'text-align: center;'})


class TourForm(FlaskForm):
    title = StringField('Title', validators=[data_required()],
                        render_kw={'placeholder': 'შეიყვანეთ პოსტის სათაური', 'class': 'form-control'})
    content = TextAreaField('content', validators=[data_required()],
                            render_kw={'placeholder': 'შეიყვანეთ პოსტის კონტენტი', 'class': 'form-control'})
    submit = SubmitField('Create Post', render_kw={'class': 'btn btn-primary', 'style': 'text-align: center;'})