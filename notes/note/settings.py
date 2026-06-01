import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-2026")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = True
    # 原来的
    # SQLALCHEMY_DATABASE_URI = "sqlite:///instance/data.db"

    # 改成这个（直接存在根目录）
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///prod.db"

config_map = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}