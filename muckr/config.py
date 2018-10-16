import environs

env = environs.Env()
env.read_env()

BCRYPT_LOG_ROUNDS = env.int('BCRYPT_LOG_ROUNDS', default=12)
SECRET_KEY = env.str('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
