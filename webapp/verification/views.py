from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user

from webapp.verification.scripts.json_parser import DictConstructor
from webapp.verification.forms import VerificationForm


blueprint = Blueprint('verification', __name__, url_prefix='/verification')


@blueprint.route('/<string:number_mi>/<string:model>')
def verification_mi(number_mi: str, model: str):
    """
    This page is intended for verification of the measuring instrument

    :param number_mi: number in the state register
    :param model: name of the measuring instrument model
    """
    title = f'Поверка {model} ({number_mi})'
    data_of_verification = DictConstructor(
        number_mi,
        model.lower()
    ).dict_for_html
    verification_form = VerificationForm()

    return render_template(
        'verification/verification.html',
        page_title=title,
        verification=data_of_verification,
        form=verification_form
    )


@blueprint.route('/get-result', methods=['POST'])
def get_result():
    """
    This page is used to receive verification results entered by the user
    """
    verification_form = VerificationForm()
    if verification_form.validate_on_submit():
        id_user = current_user.id
        result_task = {
            'limit': request.form.getlist('limit'),
            'point': request.form.getlist('point'),
            'freq': request.form.getlist('freq'),
            'meas_result': request.form.getlist('meas_result'),
            'abs_error': request.form.getlist('abs_error'),
            'meas_error': request.form.getlist('meas_error'),
            'result_meas': request.form.getlist('result_meas')
        }
        print(result_task)
        flash('Данные о поверке успешно получены')

        return redirect(url_for('tasks.task_manager'))

    flash('Что-то пошло не так')
    return redirect(url_for('verification.verification_mi'))
