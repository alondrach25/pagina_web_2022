from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def crea_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Geophysics'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,Note

    crea_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.entrar'
    login_manager.init_app(app)

    @login_manager.user_loader
    def carga_usuario(id):
        return User.query.get(int(id))

    return app

def crea_database(app):
   if not path.exists('website/'+ DB_NAME):
       with app.app_context():
            db.create_all()
       print('¡Database creada!')