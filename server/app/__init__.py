# coding=utf-8
from flask import Flask

# local imports
from config import app_config

# login_manager = LoginManager()

import logging


# 配置日志
def init_logger():
    logger = logging.getLogger('home')
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.DEBUG)
    return logger


logger = init_logger()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app