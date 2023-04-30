from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FileField, SubmitField
from wtforms.validators import DataRequired

from webapp.appr_type.models import Approved_types, Verification_data

class AddJsonForm(FlaskForm):
    """
    Verification form
    """
    number_si = SelectField(
        'Выберите госреестр из базы',
        validators=[DataRequired()],
        render_kw={"class": "form-select"}
    )

    model_si = StringField(
        'Наименование модели(ей)',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )

    ver_data = FileField(
        'Веберите json',
        validators=[DataRequired()],
        render_kw={"class": "custom-file-input"}
    )

    submit = SubmitField(
        'Добавить файл',
        render_kw={"class": "btn btn-primary btn-lg verification"}
    )
