"""Imports"""
from flask import Flask, render_template, Response
from flask_migrate import Migrate

from model import db, Approved_types


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route("/appr_types/<page_num>/<page_size>")
    def return_appr_types(page_num=1, page_size=20):
        try:
            page_num = int(page_num)
            page_size = int(page_size)
            appr_types = Approved_types.query. \
                order_by(Approved_types.id_appr_type.desc()). \
                slice((page_num - 1) * page_size, page_num * page_size)

            return render_template(
                'appr_types.html',
                appr_types=appr_types
                )

        except ValueError:
            return Response(
                '<h1>Bad request</h1>',
                status=400
                )

    @app.route("/appr_type/<id_appr_type>")
    def return_appr_type(id_appr_type):
        id_appr_type = int(id_appr_type)
        data_of_appr_type = Approved_types.query.filter(
            Approved_types.id_appr_type == id_appr_type
            ).first()

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
