from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    """
    User login form
    """
    email = EmailField(
        'Почта',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )
    remember_me = BooleanField(
        'Запомнить меня',
        validators=[DataRequired()],
        default=True,
        render_kw={"class": "form-check-input login"}
    )
    submit = SubmitField(
        'Войти',
        render_kw={"class": "btn btn-lg login"}
    )


class RegistrationForm(FlaskForm):
    """
    User registration form
    """
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )
    surname = StringField(
        'Фамилия пользователя',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )
    organization = StringField(
        'Организация',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )
    email = EmailField(
        'Почта',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
        )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )
    submit = SubmitField(
        'Зарегистрироваться',
        render_kw={"class": "btn btn-lg registration-user"}
    )

    def validate_email(self, email):
        """
        Function to check for the existence of a user with the same email

        :param email: entered email
        """
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError(
                'Пользователь с такой почтой уже зарегистрирован!'
            )
