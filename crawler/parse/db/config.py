#coding=utf-8
class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class TestConfig(Config):
    """
    Testing configurations
    """

    TESTING = True
    # 业务主库 只读
    MYSQL_DATABASE_HOST = 'rm-2ze2ft19418h992c7.mysql.rds.aliyuncs.com'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_USER = 'jindi'
    MYSQL_DATABASE_PASSWORD ='J1ndiNmZsks'
    MYSQL_DATABASE_DB = 'zsks'
    MYSQL_DATABASE_CHARSET = 'utf8'


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    # 业务主库 只读


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
