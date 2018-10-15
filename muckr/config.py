import environs

env = environs.Env()
env.read_env()

class Config:
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL', default='sqlite:////tmp/test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
