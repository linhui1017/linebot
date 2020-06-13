from lib.utils import api_response
from api.route import api_route


@api_route(rule = '/', params=None,methods=['GET', 'POST'])
def k1():
    '''{ "Description": "demo 1: basic", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[]
    }'''    
    rs = {'status':200, 'message': 'sample1 success!', 'data': []}  
    return api_response(**rs)

@api_route(rule = '/inner', params=None,methods=['GET', 'POST'])
def k2():
    '''{ "Description": "routing by rule", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[]
    }'''     
    rs = {'status':200, 'message': 'sample1-> inner success!', 'data': []}  
    return api_response(**rs)

