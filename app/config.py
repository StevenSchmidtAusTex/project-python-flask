import os
import sys
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///users.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key-not-for-production"


# Validate production config only when it's actually used
def validate_production_config():
    if not os.getenv("SECRET_KEY"):
        print("ERROR: SECRET_KEY environment variable is required.", file=sys.stderr)
        print(
            'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"',
            file=sys.stderr,
        )
        sys.exit(1)
