import os
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from webapp.appr_type.models import Approved_types
from webapp.task.forms import CreateTaskForm, ManageTaskForm, SearchTaskForm
from webapp.task.models import Tasks, Status_task
from webapp.verification.scripts.json_parser import JsonHandler
from webapp.db import db


blueprint = Blueprint('tasks', __name__, url_prefix='/tasks')


@blueprint.route('/', methods=['GET'], defaults={"page": 1})
@blueprint.route('/<int:page>', methods=['GET'])
def task_manager(page):
    """
    This page is used to manage tasks and create new tasks.
    """
    per_page = 10
    title = "Задания на проведение поверки"
    manage_task_form = ManageTaskForm()
    search_task_form = SearchTaskForm()
    tasks_info = db.session.query(Tasks). \
        join(Status_task, Tasks.id_status == Status_task.id_status). \
        filter(Tasks.id_user == current_user.id). \
        paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'tasks/task_manager.html',
        page_title=title,
        manage_task_form=manage_task_form,
        search_task_form=search_task_form,
        pagination=tasks_info
    )


@blueprint.route('/search/<string:search_num>/', methods=['GET'], defaults={"page": 1})
@blueprint.route('/search/<string:search_num>/<int:page>', methods=['GET'])
def search_task(search_num, page):
    """
    This page
    """
    per_page = 10
    title = "Задания на проведение поверки"
    manage_task_form = ManageTaskForm()
    search_task_form = SearchTaskForm()
    tasks_info = Tasks.query. \
        filter(Tasks.id_user == current_user.id). \
        filter(Tasks.serial_number.like(f'%{search_num}%')). \
        paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'tasks/search_task.html',
        page_title=title,
        manage_task_form=manage_task_form,
        search_task_form=search_task_form,
        pagination=tasks_info,
        search_num=search_num
    )


@blueprint.route('/process-search', methods=['POST'])
def process_search():
    """
    This page
    """
    search_task_form = SearchTaskForm()
    if search_task_form.validate_on_submit():
        search_num = str(search_task_form.search_num.data)
        if search_num != '':
            return redirect(url_for('tasks.search_task',
                                    search_num=search_num,
                                    page=1))

    return redirect(url_for('tasks.task_manager'))


@blueprint.route('/create_task/<string:number_mi>')
def create_task(number_mi: str):
    """
    This page is used to register a verification task

    :param number_mi: number in the state register
    """
    title = 'Регистрация задания на проведение поверки'
    task_form = CreateTaskForm()
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
    task_form = CreateTaskForm()
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
        flash(f"""
        Задание на поверку зарегистрировано!
        (Заводской (серийный) номер СИ: {task_form.serial_number.data};
        номер протокола: {task_form.protocol_number.data})
        """)

        return redirect(url_for(
            'verification.verification_mi',
            number_mi=task_form.number_mi.data,
            model=task_form.model_mi.data
        ))

    flash('Что-то пошло не так!')

    return redirect(url_for('main_page'))
