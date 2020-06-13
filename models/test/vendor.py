import datetime
from sqlalchemy import Column, String, Integer, DateTime, event, Boolean, JSON 

from db.database import pg_Base, pg_engine, pg_session
import uuid
import json
from lib.Checker import isNone
from lib.utils import  logger
from db.dbutils import  clzs_to_dicts


import pandas as pd
import io



class VendorEntity(pg_Base):
    __tablename__ = 'VENDOR'
    RELATIONSHIPS_TO_DICT = False

    VENDOR_ID = Column(String(200), primary_key=True)
    VENDOR_NAME = Column(String(4000))
    MENU = Column(JSON())
    ADDRESS_CODE = Column(String(10))

    ADDRESS = Column(String(2000))
    LONGITUDE = Column(String(200))
    LATITUDE = Column(String(200))
    
    TLE = Column(String(100))
    MOBILE = Column(String(100))


    def __init__(self):
        pass
    def __repr__(self):
        return '<VENDOR_ID: {0}, APPLY_USER_IDNO:{1}>'.format(self.VENDOR_ID, self.VENDOR_NAME)
    def __str__(self):
        return '<VENDOR_ID: {0}, APPLY_USER_IDNO:{1}>'.format(self.VENDOR_ID, self.VENDOR_NAME)


  