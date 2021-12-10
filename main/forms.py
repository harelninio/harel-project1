from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User


# Register.html def all fields and check valid
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.Choose a different one ')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.Choose a different one ')

#def valid_email(email):
#        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))



# login.html def all fields and check valid
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# account.html def all fields and check valid
class UpdateAccForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), ])
    date_birth = DateField('date_birth',
                           validators=[DataRequired(), ])
    company = StringField('company',
                          validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.Choose a different one ')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.Choose a different one ')


# search.html def all fields and check valid
class SearchStockForm(FlaskForm):
    symbol = StringField('Symbol stock', validators=[DataRequired()])
    stockopen = StringField('stock open price', validators=[DataRequired()])
    stockclose = StringField('stock close price', validators=[DataRequired()])
    stockdate = StringField('Date stock value', validators=[DataRequired()])
    submit = SubmitField('Sarching in nasdak ')
