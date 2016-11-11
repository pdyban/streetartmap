import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    WTF_CSRF_ENABLED = True
    DEBUG = False
    MURAL_IMG_FOLDER = os.path.join(basedir, 'app', 'static', 'mural_img')
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPEG', 'png'])
    LANGUAGES = {
        'en': 'English',
        'uk': 'Ukraininan'
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app_dev.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app_prod.db')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}