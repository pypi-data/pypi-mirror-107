import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from .configs import configs

basedir = os.path.abspath(os.path.dirname(__file__))

redis_host = configs('redis_host')


class Config:
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SCHEDULER_API_ENABLED = False

    CRON_DB_URL = configs('cron_db_url')

    BASEDIR = basedir

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=configs('cron_db_url'))
    }
    SCHEDULER_EXECUTORS = {
        'default': {
            'type': 'threadpool',
            'max_workers': 30
        }
    }
    # 'misfire_grace_time':30
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 20,
        'misfire_grace_time': 50
    }

    JOBS = [
        {
            'id': 'cron_check',
            'func': 'notejob.center.app.crons:cron_check',
            'args': None,
            'replace_existing': True,
            'trigger': 'cron',
            'day_of_week': "*",
            'day': '*',
            'hour': '*',
            'minute': '*/30'
        },
        {
            'id': 'cron_del_job_log',
            'func': 'notejob.center.app.crons:cron_del_job_log',
            'args': None,
            'replace_existing': True,
            'trigger': 'cron',
            'day_of_week': "*",
            'day': '*',
            'hour': '*/8'
        },
        {
            'id': 'cron_check_db_sleep',
            'func': 'notejob.center.app.crons:cron_check_db_sleep',
            'args': None,
            'replace_existing': True,
            'trigger': 'cron',
            'day_of_week': "*",
            'day': '*',
            'hour': '*',
            'minute': '*/10',
        }
    ]

    LOGIN_PWD = configs('login_pwd')

    @staticmethod
    def init_app(app):
        logs_path = os.path.join(basedir, 'datas/logs')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = configs('cron_job_log_db_url')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = configs('cron_job_log_db_url')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
