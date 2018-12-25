"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import environs

env = environs.Env()
env.read_env()

ADMIN_USERNAME = env.str("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = env.str("ADMIN_EMAIL", "admin@localhost")
ADMIN_PASSWORD = env.str("ADMIN_PASSWORD")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=12)
SECRET_KEY = env.str("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
