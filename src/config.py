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


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
