import cx_Oracle
from settings import Config
import threading



from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from db.dbutils import to_dict, models_to_list, OutputMixin
from db.dbutils import ExeQueryByModel as db_ExeQuery

# SQLLite
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.to_dict = to_dict

# #  PostgreSQL
import psycopg2
#from psycopg2.pool import PersistentConnectionPool

pg_engine = create_engine(Config.PG_CONNECTION_STRING, pool_size=30, pool_recycle=600, pool_timeout=30, pool_pre_ping=False, max_overflow=10, convert_unicode=True, isolation_level="AUTOCOMMIT")
#engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
pg_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=pg_engine))
pg_Base = declarative_base(cls=OutputMixin)
pg_Base.query = pg_session.query_property() 
#pg_Base.to_dict = to_dict   
pg_Base.ExeQuery = db_ExeQuery



