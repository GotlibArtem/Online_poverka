from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """
    Search form
    """
    number_mi = StringField(
        'Номер в госреестре',
        render_kw={"class": "form-control me-1",
                   "placeholder": "Номер в госреестре"}
    )
    submit = SubmitField(
        'Поиск',
        render_kw={"class": "btn btn-primary search"}
    )
