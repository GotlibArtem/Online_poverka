from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db import db


blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    """
    This page contains user authorization
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    title = 'Авторизация пользователя'
    login_form = LoginForm()

    return render_template(
        'user/login.html',
        page_title=title,
        form=login_form
    )


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    """
    This page checks the data entered by the user for authorization
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Авторизация выполнена!')

            return redirect(url_for('main_page'))

    flash('Неправильная почта или пароль!')

    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    """
    This page logs out the current user
    """
    logout_user()

    return redirect(url_for('main_page'))


@blueprint.route('/registration')
def registration():
    """
    This page contains the registration of a new user
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    title = 'Регистрация пользователя'
    registration_form = RegistrationForm()

    return render_template(
        'user/registration.html',
        page_title=title,
        form=registration_form
    )


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    """
    This page checks the data entered by the user for registration on the site
    and returns an error if the user is already registered
    """
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        new_user = User(
            username=registration_form.username.data,
            surname=registration_form.surname.data,
            email=registration_form.email.data,
            organization=registration_form.organization.data,
            role='user'
        )
        new_user.set_password(registration_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')

        return redirect(url_for('user.login'))

    for field, errors in registration_form.errors.items():
        for error in errors:
            flash(error)

    return redirect(url_for('user.registration'))
