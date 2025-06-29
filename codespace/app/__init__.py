from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config
import os

from app.services.code_executor import CodeExecutor, make_celery
from .extensions import db, socketio

login_manager = LoginManager()
migrate = Migrate()

executor = CodeExecutor()
celery_app = None

login_manager.login_view = 'auth_bp.login'
login_manager.login_message_category = 'info'

from app.routes.log_routes import log_bp

def create_app():
    from app.models import models  # ensure models are registered

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

    migrate.init_app(app, db)

    global celery_app
    if app.config.get('CELERY_BROKER_URL'):
        celery_app = make_celery(app)
        executor.execute_code_task = celery_app.task(executor.execute_code_task)
        app.logger.info("Celery is configured and code execution tasks are routed to Celery.")
    else:
        app.logger.warning("CELERY_BROKER_URL not found. Falling back to local code execution.")

    with app.app_context():
        db.create_all()

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(log_bp)

    return app

# 👇 Обязательно: загрузка пользователя по ID
from app.models.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
