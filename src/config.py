import os


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def create_db_url(user, pw, url, db):
    return f"mysql+mysqlconnector://{user}:{pw}@{url}/{db}"


MYSQL_USER = get_env_variable("MYSQL_USER") if get_env_variable("MYSQL_USER") is not None else "root"
MYSQL_PW = get_env_variable("MYSQL_PW") if get_env_variable("MYSQL_PW") is not None else "leeoeol312!!"
MYSQL_URL = get_env_variable("MYSQL_URL") if get_env_variable("MYSQL_URL") is not None else "db-connect-people.cluster-cgyszlfeotqz.ap-northeast-2.rds.amazonaws.com:3306"
MYSQL_DB = get_env_variable("MYSQL_DB") if get_env_variable("MYSQL_DB") is not None else "DB_CORE"

# DB
DB_URL = create_db_url(MYSQL_USER, MYSQL_PW, MYSQL_URL, MYSQL_DB)

# S3
S3_HOST = "https://connect-people.s3.ap-northeast-2.amazonaws.com"
S3_BUCKET = "connect-people"


class Config(object):
    # ...
    ERROR_404_HELP = False
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_VALIDATE = True
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
