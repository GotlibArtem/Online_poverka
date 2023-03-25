"""Imports"""
from flask import Flask, render_template, Response
from flask_migrate import Migrate

from model import db, Approved_types


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/appr_types/<int:page>/<int:per_page>', methods=['GET'])
    def return_appr_types(page=1, per_page=20):
        appr_types = Approved_types.query. \
            order_by(Approved_types.id_appr_type.desc()). \
            paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            'appr_types.html',
            appr_types=appr_types
            )

    @app.route('/appr_type/<int:id_appr_type>')
    def return_appr_type(id_appr_type):
        id_appr_type = int(id_appr_type)
        data_of_appr_type = Approved_types.query.get(id_appr_type)

        return render_template(
            'data_of_appr_type.html',
            data_of_appr_type=data_of_appr_type
            )

    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
