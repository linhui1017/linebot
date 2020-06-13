import psycopg2
import json
import sqlalchemy
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.sql import text

from datetime import datetime
from flask import jsonify
from collections import namedtuple
from db.database import pg_session
from lib import utils


# Type Convert
def Convert(value):
    return value
    #if type(value) is datetime:
    #        return value.strftime("%Y-%m-%d %H:%M:%S")
    #else: 
    #    return value

# Dict
def Query(sql, **params):
    try:
        comment = text(sql)
        session = pg_session()
        proxy =  session.execute(comment, params)
        descrip = proxy._cursor_description()
        cur = proxy.fetchall()
        data =  [dict((descrip[i][0], Convert(value)) \
               for i, value in enumerate(row)) for row in cur]
   
        #return {'status':200, 'message': 'OK', 'data': data}
        return data
    except sqlalchemy.exc.SQLAlchemyError as e:
        error, = e.args
        utils.logger.error(error)
        raise e
    finally:
        session.close()
 
# Start Transaction
def StartTransaction():
    try:
        session = pg_session()
        return session
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('pgdb error:{0}'.format(error))
        raise e

# Rollback Transaction
def Rollback(trans):
    try:
        trans.rollback()
        trans.close()
        return True
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('pgdb error:{0}'.format(error))
        trans.close()
        raise e       

# Commit Transaction
def Commit(trans):
    try:
        trans.commit()
        trans.close()
        return True
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('pgdb error:{0}'.format(error))
        trans.rollback()
        trans.close()
        raise e  
         
# Execute
def ExecSQL(trans, sql, **params):
    try:
        comment = text(sql)
        proxy =  trans.execute(comment, params)
        return True        
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('pgdb error:{0}'.format(error))
        raise e        