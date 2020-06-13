from lib.utils import api_response
from api.route import api_route
from lib.web import get_parameter
from lib.Checker import isNone

from datetime import datetime



req_params = {}
req_params['PARAM'] = ['required']


@api_route(rule = '', params=req_params, methods=['POST','GET'])
def _test(args):
    '''{ "Description": "API Test", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"PARAM", "Name":"PARAM", "Required":true}
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


        return response_data
    try:
        _check_parameter()
        _deal() 
        return api_response(**_responseData())        
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': []}  
        return api_response(**rs), 400

