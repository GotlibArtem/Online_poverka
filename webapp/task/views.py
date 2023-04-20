import os
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from webapp.appr_type.models import Approved_types
from webapp.task.forms import TaskForm
from webapp.task.models import Tasks
from webapp.verification.scripts.json_parser import JsonHandler
from webapp.db import db


blueprint = Blueprint('tasks', __name__, url_prefix='/tasks')


@blueprint.route('/create_task/<string:number_mi>')
def create_task(number_mi: str):
    """
    This page is used to register a verification task

    :param number_mi: number in the state register
    """
    title = 'Регистрация задания на проведение поверки'
    task_form = TaskForm()
    appr_type_info = Approved_types.query. \
        filter(Approved_types.number_si == number_mi).first()
    file = f'webapp/appr_type/scripts/{number_mi}.json'
    if os.path.exists(file):
        data_file = JsonHandler(file)
        models = data_file.get_models()
    task_form.model_mi.choices = models

    return render_template(
        'tasks/new_task.html',
        page_title=title,
        appr_type_info=appr_type_info,
        form=task_form
    )


@blueprint.route('/process-reg-task', methods=['POST'])
def process_reg_task():
    """
    This page is used to register the task in the database
    """
    task_form = TaskForm()
    appr_type_info = Approved_types.query. \
        filter(Approved_types.number_si == task_form.number_mi.data).first()
    if task_form.validate_on_submit():
        new_task = Tasks(
            id_user=current_user.id,
            id_appr_type=appr_type_info.id_appr_type,
            model_mi=task_form.model_mi.data,
            serial_number=task_form.serial_number.data,
            protocol_number=task_form.protocol_number.data,
            id_status=1
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Задание на поверку зарегистрировано!')

        return redirect(url_for(
            'verification.verification_mi',
            number_mi=task_form.number_mi.data,
            model=task_form.model_mi.data
        ))

    flash('Что-то пошло не так!')

    return redirect(url_for('main_page'))
