import os.path


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    LOG_DIR = os.environ.get('LOG_DIR') or './'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
    WTF_CSRF_ENABLED = True
    DEBUG = False
    MURAL_IMG_FOLDER = os.path.join(BASEDIR, 'app', 'static', 'mural_img')
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPEG', 'png'])
    MURALS_PER_PAGE = 9

    # language configuration
    LANGUAGES = [
        ('en', 'English'),
        ('de', 'Deutsch'),
    ]
    DEFAULT_LANG = 'en'

    # map configuration for the homepage
    # Kiev
    # MAP_LATITUDE = 50.450487
    # MAP_LONGITUDE = 30.519516
    # MAP_ZOOM = 12
    # Berlin
    MAP_LATITUDE = 52.5177291
    MAP_LONGITUDE = 13.3839094
    MAP_ZOOM = 13.67

    # author information
    AUTHOR_NAME = "Pavlo Dyban"
    AUTHOR_EMAIL = "info@streetartmap.berlin"
    AUTHOR_COPYRIGHT = "2019 Creative Commons License. The art works are licensed to their respective owners."

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_dev.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_prod.db')


class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig,
    'heroku': HerokuConfig
}