import psycopg2 as pg
from sqlalchemy import create_engine
import hidden.database_config as config


def connect():
    # connect to
    con = pg.connect(database=config.db_name, user=config.db_user, password=config.db_user_pass,
                     host=config.host, port=5432)
    return con


def return_enginge():
    engine = create_engine(
        'postgresql://' + config.db_user + ':' + config.db_user_pass + '@' + config.host + '/' + config.db_name)
    return engine
