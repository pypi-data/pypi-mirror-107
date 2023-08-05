import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from notejob.center.app.CuBackgroundScheduler import CuBackgroundScheduler
from notejob.center.config import Config, config_dict

scheduler = APScheduler(scheduler=CuBackgroundScheduler())

db = SQLAlchemy()

formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")


def create_app(config_name):
    config_name = 'production'
    config = config_dict[config_name]
    app = Flask(__name__)
    app.config.from_object(config)
    configDict[config_name].init_app(app)

    logging.basicConfig(level=logging.ERROR)

    info_handler = TimedRotatingFileHandler("%s/datas/logs/info.log" % config[config_name].BASEDIR,
                                            when="H",
                                            interval=1, backupCount=7, encoding="UTF-8", delay=False,
                                            utc=True)
    # info_handler.setLevel(logging.INFO)
    info_handler.filter = lambda record: record.levelno == logging.INFO
    info_handler.setFormatter(formatter)

    app.logger.addHandler(info_handler)

    error_handler = TimedRotatingFileHandler("%s/datas/logs/error.log" % config[config_name].BASEDIR,
                                             when="D",
                                             interval=1, backupCount=15, encoding="UTF-8", delay=False,
                                             utc=True)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    app.logger.addHandler(error_handler)

    scheduler.app = app
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from notejob.center.app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 接口对接
    from notejob.center.app.api import api as apis_bl
    app.register_blueprint(apis_bl, url_prefix='/api')

    return app
