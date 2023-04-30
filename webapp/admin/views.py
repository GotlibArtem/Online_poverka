from flask import Blueprint, render_template
from webapp.user.decorators import admin_required

from webapp.admin.forms import AddJsonForm
from webapp.appr_type.models import Verification_data
from webapp.db import db


blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    """
    This page contains admin panel management
    """
    title = 'Добавление json в базу'

    return render_template(
        'admin/index.html',
        page_title=title,
    )

