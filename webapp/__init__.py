from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager

from webapp.db import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.appr_type.views import blueprint as appr_types_blueprint
from webapp.task.views import blueprint as tasks_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.verification.views import blueprint as verification_blueprint


def create_app() -> Flask:
    """
    Function of creating a web application on flask

    :return: flask application
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(appr_types_blueprint)
    app.register_blueprint(tasks_blueprint)
    app.register_blueprint(verification_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def main_page():
        return render_template(
            'main.html'
        )

    return app


def main():
    """
    Function to launch the Flask Application
    """
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
