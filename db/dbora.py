import cx_Oracle
import json
import sqlalchemy
import lib.utils as utils

from sqlalchemy.sql import text
from datetime import datetime
from flask import jsonify
from collections import namedtuple
from db.database import pool, ora_session
from lib.Checker import isNone

# Type Convert


def Convert(value):
    if type(value) is cx_Oracle.LOB:
        return value.read()
#    elif type(value) is cx_Oracle.DATETIME:
#        return value.strftime("%Y-%m-%d %H:%M:%S")
#    elif type(value) is datetime:
#        return value.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return value

# Dict


def Query(sql, **params):
    try:
        conn = pool.acquire()
        cur = conn.cursor()
        cur.execute(sql, params)
        data = [dict((cur.description[i][0], Convert(value))
                     for i, value in enumerate(row)) for row in cur.fetchall()]
        return {'status': True, 'message': 'OK', 'data': data}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        utils.logger.error(error.message)
        return {'status': False, 'message': error.message, 'data': []}
    finally:
        cur.close()
        conn.close()

# NamedTuple


def QueryN(sql, **params):
    try:
        conn = pool.acquire()
        cur = conn.cursor()
        cur.execute(sql, params)
        columnNames = [col[0] for col in cur.description]
        RowType = namedtuple('Row', columnNames)
        data = [RowType(*row)
                for row in cur.fetchall()]

        # return data
        return {'status': True, 'message': 'OK', 'data': data}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        utils.logger.error(error.message)
        return {'status': False, 'message:': error.message}
    finally:
        cur.close()
        conn.close()

# Start Transaction


def StartTransaction():
    try:
        conn = pool.acquire()
        conn.begin()
        return conn
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error.message))
        raise

# Rollback Transaction


def Rollback(conn):
    try:
        conn.rollback()
        conn.close()
        return {'status': True, 'message': 'OK'}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error.message))
        conn.close()
        return {'status': False, 'message': error.message}

# Commit Transaction


def Commit(conn):
    try:
        conn.commit()
        conn.close()
        return {'status': True, 'message': 'OK'}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error.message))
        conn.rollback()
        conn.close()
        return {'status': False, 'message': error.message}

# Execute


def ExecSQL(conn, sql, **params):
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        return {'status': True, 'message': 'OK'}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error.message))
        return {'status': False, 'message': error.message}


def ExecFunc(name, rtnType, *params):
    try:
        conn = pool.acquire()
        cur = conn.cursor()
        result = cur.callfunc(name, rtnType, params)

        # return result
        return {'status': True, 'message': 'OK', 'data': result}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        utils.logger.error(error.message)
        return {'status': False, 'message': error.message, 'data': []}
    finally:
        cur.close()
        conn.close()


#
# W/SQLAlchemy
#
def QueryA(sql, **params):
    try:
        comment = text(sql)
        session = ora_session()
        proxy = session.execute(comment, params)
        descrip = proxy._cursor_description()
        cur = proxy.fetchall()

        data = [dict((descrip[i][0], Convert(value))
                     for i, value in enumerate(row)) for row in cur]

        return data
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error(error)
        raise e
    finally:
        session.close()


# Start Transaction
def StartTransactionA():
    try:
        session = ora_session()
        return session
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error))
        raise e

# Rollback Transaction


def RollbackA(trans):
    try:
        trans.rollback()
        trans.close()
        return True
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error))
        trans.close()
        raise e

# Commit Transaction


def CommitA(trans):
    try:
        trans.commit()
        trans.close()
        return True
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error))
        trans.rollback()
        trans.close()
        raise e

# Execute


def ExecSQLA(trans, sql, **params):
    try:
        comment = text(sql)
        # proxy = trans.execute(comment, params)
        trans.execute(comment, params)
        return True
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error))
        raise e

# GenSeqNO


def GenSeqNO(seqNO):
    '''*** ORACLE KFSYSCC.FN_GET_SEQ_NO  取號 ***'''
    try:
        sql = "select FN_GET_SEQ_NO(:P_SEQ_NO, '1')  As SEQ_NO from DUAL"
        params = {}
        params['P_SEQ_NO'] = seqNO
        data = QueryA(sql, **params)
        if(not isNone(data)):
            return data[0]['SEQ_NO']
        else:
            return ''
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        utils.logger.error('oracle error:{0}'.format(error))
        raise e
