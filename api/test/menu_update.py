from lib.utils import api_response
from api.route import api_route
from lib.web import get_parameter
from lib.Checker import isNone
from db.database import pg_session
from db.dbutils import models_to_list
from datetime import datetime
from lib.utils import  logger
import json

from models.test.vendor import VendorEntity

def find_by_id(vid):
    try:
        session = pg_session()
        res = session.query(VendorEntity).filter(VendorEntity.VENDOR_ID == vid).first()
        return  res
    except Exception as e:
        return None
    finally:
        session.close()   

req_params = {}
req_params['VENDOR_ID'] = ['required']
req_params['MENU'] = ['']


@api_route(rule = '', params=req_params, methods=['POST','GET'])
def _menu_update(args):
    '''{ "Description": "API Test", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"VENDOR_ID", "Name":"VENDOR_ID", "Required":true},
             {"Description":"MENU", "Name":"MENU", "Required":false}
         ]
    }'''


    response_data = {}
    response_data['status'] = True
    response_data['message'] = ''
    response_data['data'] = []  
   
    def _check_parameter():
        pass

    def _deal():
        pass

    def _responseData():

        try:
            vendor = find_by_id(vid=args['VENDOR_ID'])

            if(not isNone(vendor)):
                vendor.MENU = None if  isNone(args['MENU']) else args['MENU']
                session = pg_session()
                try:
                    session.add(vendor)
                except Exception as e:
                    session.rollback() 
                    logger.error('_menu_update :' +  str(e)) 
                else:
                    session.commit()
                

                response_data['data'] = models_to_list(vendor)
        except Exception as e: 
            logger.error('_menu_update :' +  str(e)) 
            pass
	



        
        return response_data
    try:
        _check_parameter()
        _deal() 
        return api_response(**_responseData())        
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': []}  
        return api_response(**rs), 400
