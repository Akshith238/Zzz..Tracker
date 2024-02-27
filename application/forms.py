from wtforms import DateTimeField,SubmitField,StringField,PasswordField,EmailField,BooleanField
from wtforms.validators import DataRequired,Email,Length,ValidationError,EqualTo
from flask_wtf import FlaskForm
from application.models import User

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(),Email(message='Invalid Email Address')])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField("Log In")

class SignUpForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField("username",validators=[DataRequired()])
    email = StringField("email",validators=[Email(message='Invalid Email Address'),DataRequired()])
    password = PasswordField("password",validators=[Length(min=2,max=14,message="invalid length"),DataRequired()])
    confirm_password=PasswordField("confirm_password",validators=[EqualTo(password),DataRequired()])
    submit = SubmitField("Sign Up")

class SleepForm(FlaskForm):
    startTime = DateTimeField('startTime', format='%Y-%m-%dT%H:%M:%S')
    endTime = DateTimeField('endTime', format='%Y-%m-%dT%H:%M:%S')
    submit=SubmitField("Sleep In")
    
