import os, sys, logging
from datetime import datetime, timedelta
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, render_template, flash, redirect, url_for, g, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from flask_babel import _, get_locale

from celery import Celery

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    celery.conf.update(app.config)

#     from app.main import bp as main_bp
#     app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from app.message import bp as message_bp
    app.register_blueprint(message_bp, url_prefix='/message')

    from app.case_his import bp as case_his_bp
    app.register_blueprint(case_his_bp, url_prefix='/case_his')

    from app.case_new import bp as case_new_bp
    app.register_blueprint(case_new_bp, url_prefix='/case_new')

    from app.component import bp as component_bp
    app.register_blueprint(component_bp, url_prefix='/component')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Seeker Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/seeker.log', maxBytes=1000000, backupCount=10)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Seeker startup')

    @app.before_first_request
    def before_first_request():
        app.logger.info("run: app.before_first_request")
        app.permanent_session_lifetime = timedelta(minutes=30)
        # if current_user.is_authenticated:
        #    session['components'] = get_components()

    @app.before_request
    def before_request():
        app.logger.info("run: app.before_request")
        # session.permanent = True
        # app.permanent_session_lifetime = timedelta(minutes=1)
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()
            session['components'] = get_components()
            # session['component'] = get_component()
        g.locale = str(get_locale())

    @app.context_processor
    def inject_conf_var():
        return dict(CURRENT_LANGUAGE=session.get('language'), CURRENT_COMPONENTS=session.get('components'))

    @app.route('/language/<language>')
    @login_required
    def set_language(language=None):
        session['language'] = language
        # return redirect(request.path, 204)
        return redirect(url_for('index'))

    @app.route('/component/<component>')
    @login_required
    def set_component(component):
        session['component'] = component
        current_user.last_component = component
        db.session.commit()
        if 'new_case_id_list' in session:
            current_app.logger.info("pop session['new_case_id_list'] due to set component")
            session.pop('new_case_id_list')
        return redirect(url_for('index'))

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index', methods=['GET', 'POST'])
    @login_required
    def index():
        return redirect(url_for('case_his.case'))

    return app


@babel.localeselector
def get_locale():
#     return request.accept_languages.best_match(current_app.config['LANGUAGES'])
#     return 'es'
#     return 'zh_Hans_CN'
    try:
        language = session['language']
    except KeyError:
        language = None
    if language is not None:
        return language
    lan = request.accept_languages.best_match(current_app.config['LANGUAGES'])
    session['language'] = lan
    return lan

# def get_component():
#     try:
#         component = session['component']
#     except KeyError:
#         component = None
#     if component is not None:
#         return component
#     return current_user.last_component


def get_components():
    try:
        components = session['components']
    except KeyError:
        components = None
    if components is not None:
        return components
    # return Component.query.with_entities(Component.component).all()
    # return Component.query(Component.component).all()
    component_list = []
    for component in Component.query.all():
        component_list.append(component.component)
    return component_list


from app import models
from app.models import Component
from app.models import Cases
