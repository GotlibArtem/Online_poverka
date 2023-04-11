"""Imports"""
import os
from flask import Flask, render_template
from flask_migrate import Migrate
from json_parser import DictConstructor, JsonHandler
from model import db, Approved_types


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    # migrate = Migrate(app, db)

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
        data_of_appr_type = Approved_types.query.get(id_appr_type)
        file = f'scripts/{data_of_appr_type.number_si}.json'
        status_file = os.path.exists(file)

        return render_template(
            'data_of_appr_type.html',
            data_of_appr_type=data_of_appr_type,
            status_file=status_file
            )

    @app.route('/poverka/<string:number_mi>/<string:model>')
    def verification_mi(number_mi: str, model: str):
        data_of_verification = DictConstructor(number_mi, model).dict_for_html

        return render_template('verification.html',
                               verification=data_of_verification)

    @app.route('/poverka/<string:number_mi>')
    def choose_model(number_mi: str):
        file = f'scripts/{number_mi}.json'
        if os.path.exists(file):
            data_file = JsonHandler(file)
            models = data_file.get_models()

        return render_template('choose_model.html',
                               models=models)

    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
