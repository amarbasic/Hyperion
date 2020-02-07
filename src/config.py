"""Application configuration"""


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


DEV_CONFIG = "dev"
TEST_CONFIG = "test"
PROD_CONFIG = "prod"

configuration = {
    DEV_CONFIG: DevelopmentConfig,
    TEST_CONFIG: TestingConfig,
    PROD_CONFIG: ProductionConfig,
}
