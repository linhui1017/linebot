from lib.utils import api_response
from api.route import api_route
from lib.web import get_parameter

@api_route(rule = '', params=None ,methods=['GET','POST'])
def r_by_filename():
    '''{ "Description": "routing by file name", "Methods":"POST", "Content-Type":"application/json",
         "Parameters":[]
    }'''     
    rs = {'status':200, 'message': 'routing by file name success!', 'data': []}  
    return api_response(**rs)
   
@api_route(rule = '/' , params=None ,methods=['GET','POST'])
def func_name():
    '''{ "Description": "demp 2: routing by function name", "Methods":"POST", "Content-Type":"application/json",
         "Parameters":[]
    }''' 
    rs = {'status':200, 'message': 'routing by function name success!', 'data': []}  
    return api_response(**rs)

@api_route(rule = '/hello', params=None ,methods=['GET','POST'])
def k2():
    '''{ "Description": "Query string  /hello?name=test", "Methods":"POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"參數", "Name":"name", "Required":true}
         ]
    }'''    
    try:    
        req_params = {}
        req_params['name'] = ['required']    
        _params = get_parameter(**req_params)
        rs = {'status':200, 'message': 'sample2-> Hello {0}!'.format(_params['name']), 'data': []}  
        return api_response(**rs)   
    except Exception as e:
        rs = {'status':400, 'message': str(e), 'data': []}  
        return api_response(**rs), 400  

  
