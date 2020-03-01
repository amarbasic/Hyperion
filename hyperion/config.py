"""Application configuration"""
import os

from dotenv import load_dotenv


load_dotenv(verbose=True)


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")


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
