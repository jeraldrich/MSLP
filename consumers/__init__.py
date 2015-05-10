import logging
import os

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import *
from models import Base, ChatMessage

logger = logging.getLogger('chat_message_parser') 



def create_mysql_pool():
    mysql_host = MYSQL_HOST
    mysql_port = MYSQL_PORT
    mysql_db = MYSQL_DB
    mysql_user = MYSQL_USER
    mysql_passwd = MYSQL_PASSWD

    # max_connections default for mysql = 100
    # set mysql connections to 90 and 5 for sqlalchemy buffer
    mysql_pool = sa.create_engine(
        'mysql://{user}:{passwd}@{host}'.format(
            user=mysql_user,
            passwd=mysql_passwd,
            host=mysql_host
        ),
        pool_size=10,
        max_overflow=5,
        pool_recycle=3600,
    )
    try:
        mysql_pool.execute("USE {db}".format(
            db=mysql_db)
        )
    except sa.exc.OperationalError:
        logger.info('DATABASE {db} DOES NOT EXIST. CREATING...'.format(
            db=mysql_db)
        )
        mysql_pool.execute("CREATE DATABASE {db}".format(
           db=mysql_db)
        ) 
        mysql_pool.execute("USE {db}".format(
            db=mysql_db)
        )
    mysql_pool = sa.create_engine(
        'mysql://{user}:{passwd}@{host}/{db}'.format(
            user=mysql_user,
            passwd=mysql_passwd,
            host=mysql_host,
            db=mysql_db
        ),
        pool_size=10,
        pool_recycle=3600,
    )
    return mysql_pool

init_mysql_pool = create_mysql_pool()
Base.metadata.create_all(init_mysql_pool, checkfirst=True)
init_mysql_pool.dispose()


def batch_insert(session, result):
    """
    Start transactional insert
    """
    # save to sql database
    batch_insert = []
    for batch_object in result:
        record = session.query(ChatMessage).get({batch_object.id})
        if record:
            #logger.info('duplicate entry in db {0}'.format(batch_object.id))
            continue
        batch_insert.append(batch_object)
    if batch_insert:
        try:
            session.add_all(batch_insert)
            session.commit()
        except sa.exc.IntegrityError:
            logger.info('something HORRIBLE has happened')
            session.rollback()
    session.close()
    return True
