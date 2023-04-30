from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField

from wtforms.validators import DataRequired


class ManageTaskForm(FlaskForm):
    """
    Task management form
    """
    delete_submit = SubmitField(
        'Удалить',
        render_kw={"class": "border-0 btn-transition btn btn-outline-danger delete"}
    )
    change_submit = SubmitField(
        'Изменить',
        render_kw={"class": "border-0 btn-transition btn btn-outline-success change"}
    )
    create_submit = SubmitField(
        'Создать задание',
        render_kw={"class": "btn create-task"}
    )


class SearchTaskForm(FlaskForm):
    """
    Form for searching tasks
    """
    search_num = StringField(
        'Заводской номер',
        render_kw={"class": "form-control me-1",
                   "placeholder": "Заводской номер"}
    )
    search_submit = SubmitField(
        'Поиск',
        render_kw={"class": "btn btn-primary"}
    )


class CreateTaskForm(FlaskForm):
    """
    Verification task registration form
    """
    number_mi = StringField(
        'Номер в госреестре',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg item"}
    )
    name_mi = StringField(
        'Наименование СИ',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg item dis"}
    )
    designation_mi = StringField(
        'Тип СИ',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg item dis"}
    )
    model_mi = SelectField(
        'Модель (модификация) СИ',
        validators=[DataRequired()],
        choices=[],
        validate_choice=False,
        render_kw={"class": "form-select form-select-lg mb-3 item"}
    )
    serial_number = StringField(
        'Заводской (серийный) номер СИ',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg item"}
    )
    protocol_number = StringField(
        'Номер протокола',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg item"}
    )
    submit = SubmitField(
        'Зарегистрировать задание',
        render_kw={"class": "btn btn-lg create-task"}
    )
