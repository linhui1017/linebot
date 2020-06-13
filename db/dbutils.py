import cx_Oracle, re ,inspect, sqlalchemy
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.sql import text
from sqlalchemy.orm import class_mapper
from datetime import datetime
from uuid import UUID
from lib.utils import logger
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import jsonify, Response
from lib.Checker import isNone
import time 
from lib.utils import jsonconverter

  

def to_dict(self):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(self.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(self, c)) for c in columns)


def o_to_d(obj, func = None):
    '''object to dictionary'''
    result = None
    dict1 = {}
    try:
        method = func if not isNone(func) else 'to_dict'
        if hasattr(obj, method):
            dict1 = getattr(obj, method)()
        else:
            dict1 = dict((t, getattr(obj, t)) for t in obj.__dict__.keys() if not t.startswith('_'))
         #dict1 = getattr(obj, method)() if hasattr(obj, method) else obj.__dict__
    except Exception as identifier:
        logger.error(str(identifier))  
    else:
        oths = {}
        if isNone(func):
            oths = {p: getattr(obj, p) for p in dir(obj.__class__) if isinstance(getattr(obj.__class__,p),property)}
        result = dict(dict1, **oths)
    return result


def clzs_to_dicts(objects, func = None):
    '''object list to dictionary'''
    if objects is not None and  isinstance(objects, list):
        result = []
        for obj in objects:
            res = o_to_d(obj, func)            
            if res is not None:
                result.append(res) 
        return result
    elif objects is not None : 
        return  o_to_d(objects, func)
    else:
        return []

def models_to_list(models):
    '''ORM list to dictionary'''
    return clzs_to_dicts(models)

def models_to_json(models):
    result = clzs_to_dicts(models)
    if result is not None and  isinstance(result, list):
        return json.dumps(result, default = jsonconverter, ensure_ascii=False)
    else:
        return None


 # Type Convert
def db_convert(value):
    if type(value) is datetime:
        return value   
    elif type(value) is cx_Oracle.DATETIME:
        return value
    elif type(value) is cx_Oracle.LOB:
        return value.read()
    elif type(value) is UUID:
        return str(value)        
    else: 
        return value        

#使用Data model 執行 SQL Command
@classmethod
def ExeQueryByModel(clz, session, sql, **params):
    '''使用Data model 執行 SQL Command'''
    try:
        comment = text(sql)
        proxy =  session.execute(comment, params)
        descrip = proxy._cursor_description()
        cur = proxy.fetchall()
        data = []
        if len(cur) > 0:
            properties = dict((c.key.lower(), c.key) for c in class_mapper(clz).columns )
            for row in cur :
                instance = clz()
                for i, value in enumerate(row):
                    if descrip[i][0].lower() in properties:
                        p = properties[descrip[i][0].lower()]
                        setattr(instance, p, db_convert(value))
                    elif (re.sub(r"[\W_]+","",descrip[i][0]).lower()) in  properties:
                        p = properties[re.sub(r"[\W_]+","",descrip[i][0]).lower()]  
                        setattr(instance, p, db_convert(value))
                    else:
                        setattr(instance, descrip[i][0], db_convert(value))
                data.append(instance)
        else:
            data = None 
        return data
    except sqlalchemy.exc.SQLAlchemyError as e:
        error, = e.args
        logging.error(error)
        raise e
    finally:
        session.close()


class OutputMixin(object):
    '''ORM 物件轉 dictionary 外掛'''
    RELATIONSHIPS_TO_DICT = False
    def __iter__(self):
        return self.to_dict().iteritems()
    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        
        #clolist = list(res.keys())
        oths = {p: getattr(self, p)
               for p in dir(self.__class__) if isinstance(getattr(self.__class__,p),property)}
        res=dict(res, **oths)
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            return jsonconverter(x)
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)     
        #return Response(json.dumps(self.to_dict(rel), default = extended_encoder, ensure_ascii=False), mimetype='application/json') 

    def c_to_ds(self, objects):
        return clzs_to_dicts(objects)
 

def exe_query_by_clz(clz, session, sql, **params):
    '''使用Data class 執行 SQL Command'''
    try:
        comment = text(sql)
        proxy =  session.execute(comment, params)
        descrip = proxy._cursor_description()
        cur = proxy.fetchall()
        data = []
        if len(cur) > 0:
            instance = clz()
            properties = [dict((t.lower(), t ) for t in instance.__dict__.keys() if not t.startswith('_')) ][0]

            oths = {p.lower(): p
               for p in dir(instance.__class__) if isinstance(getattr(instance.__class__, p), property) }          
            
            properties = dict(properties, **oths)

            for row in cur :
                instance = clz()
                for i, value in enumerate(row):
                    try:
                        if descrip[i][0].lower() in properties:
                            p = properties[descrip[i][0].lower()]
                            setattr(instance, p, db_convert(value))
                        elif (re.sub(r"[\W_]+","",descrip[i][0]).lower()) in  properties:
                            p = properties[re.sub(r"[\W_]+","",descrip[i][0]).lower()]  
                            setattr(instance, p, db_convert(value))
                        else:
                            continue
                            #如果要把沒有定義在clz中欄位顯示出來,再把它打開
                            #setattr(instance, descrip[i][0], Convert(value))
                    except Exception as e:
                        continue

                data.append(instance)
        else:
            data = None 
        return data
    except sqlalchemy.exc.SQLAlchemyError as e:
        error, = e.args
        logger.error(error)
        raise e
    finally:
        session.close()      

 #使用Data model 執行 SQL Command
@classmethod
def exe_query(clz, session, sql, **params):
    '''使用Data model 執行 SQL Command'''
    return exe_query_by_clz(clz, session, sql, **params)
    
