from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from resumemake.config import Config
from flask_migrate import Migrate
from utils import mail

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'account.login'
login_manager.login_message = "Login to see this page!"

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate()

    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app,db)
        db.create_all()
    login_manager.init_app(app)

    from resumemake.account.views import account
    from resumemake.dashboard.views import dashboard
    from resumemake.public.views import public
    from resumemake.resume.views import resume
    from resumemake.settings.views import settings
    from resumemake.messages.views import messages
    from resumemake.payment.views import payment

    app.register_blueprint(account)
    app.register_blueprint(public)
    app.register_blueprint(dashboard)
    app.register_blueprint(resume)
    app.register_blueprint(settings)
    app.register_blueprint(messages)
    app.register_blueprint(payment)

    return app
