import os
from flask import Blueprint, render_template, request

from webapp.appr_type.models import Approved_types


blueprint = Blueprint('appr_types', __name__, url_prefix='/appr_types')


@blueprint.route('/', methods=['GET'], defaults={"page": 1})
@blueprint.route('/<int:page>', methods=['GET'])
def appr_types(page):
    """
    This page contains a table with approved types of measuring instruments
    with the ability to navigate through the pages

    :param page: page number
    """
    per_page = 20
    title = 'Утвержденные типы СИ'
    pagination = Approved_types.query. \
        order_by(Approved_types.id_appr_type.desc()). \
        paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'appr_types/appr_types.html',
        page_title=title,
        pagination=pagination
    )


@blueprint.route('/info/<int:id_appr_type>')
def appr_type_info(id_appr_type):
    """
    This page contains all the information about one approved type
    of measuring instrument

    :param id_appr_type: id of approved type from db.Approved_types
    """
    data_of_appr_type = Approved_types.query.get(id_appr_type)
    title = f'Сведения об утвержденном типе СИ ({data_of_appr_type.number_si})'
    file = f'webapp/appr_type/scripts/{data_of_appr_type.number_si}.json'
    status_file = os.path.exists(file)
    back_page_url = request.referrer

    return render_template(
        'appr_types/data_of_appr_type.html',
        data_of_appr_type=data_of_appr_type,
        page_title=title,
        status_file=status_file,
        back_page_url=back_page_url
    )
