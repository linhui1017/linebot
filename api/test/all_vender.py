from lib.utils import api_response
from api.route import api_route
from lib.web import get_parameter
from lib.Checker import isNone
from db.database import pg_session
from db.dbutils import models_to_list
from datetime import datetime

from models.test.vendor import VendorEntity



req_params = {}
req_params['PARAM'] = ['']


@api_route(rule = '', params=req_params, methods=['POST','GET'])
def _all_vender(args):
    '''{ "Description": "API Test", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"PARAM", "Name":"PARAM", "Required":false}
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
        session = pg_session()
        verdors = session.query(VendorEntity).all()
        session.close()

        response_data['data'] = models_to_list(verdors)

        return response_data
    try:
        _check_parameter()
        _deal() 
        return api_response(**_responseData())        
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': []}  
        return api_response(**rs), 400
