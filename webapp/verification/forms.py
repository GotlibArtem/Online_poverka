from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField


class VerificationForm(FlaskForm):
    """
    Verification form
    """
    submit = SubmitField(
        'Завершить поверку',
        render_kw={"class": "btn btn-lg verification"}
    )
