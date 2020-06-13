from lib.utils import api_response
from api.route import api_route
from lib.AESCipher import AESCipher
from lib.web import get_parameter
from settings import Config


    # '''*** demp 2: Query string  /hello?name=test ***'''
    # try:    
    #     req_params = {'name': ['required'] }
    #     _params = get_parameter(**req_params)
    #     rs = {'status':200, 'message': 'sample2-> Hello {0}!'.format(_params['name']), 'data': []}  
    #     return api_response(**rs)   
    # except Exception as e:
    #     rs = {'status':400, 'message': str(e), 'data': []}  
    #     return api_response(**rs), 400  

@api_route(rule='/', params=None, methods=['GET', 'POST'])
def encode():
    '''{ "Description": "AES Encrypt", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"key", "Name":"key", "Required":true},
             {"Description":"data", "Name":"data", "Required":true}
         ]
    }'''   
    try:
        req_params = {}
        req_params['key'] = ['required']
        req_params['data'] = ['required']     

        _params = get_parameter(**req_params)

        encrypt= AESCipher(_params['key']).encrypt(_params['data'])
        result={'result' : encrypt}
        rs = {'status':200, 'message': 'OK', 'data': result}
        return api_response(**rs)  

    except Exception as e:
        rs = {'status':400, 'message': str(e), 'data': []}
        return api_response(**rs)  

@api_route(rule='/', params=None, methods=['GET', 'POST'])
def decode():
    '''{ "Description": "AES Decrypt", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"key", "Name":"key", "Required":true},
             {"Description":"data", "Name":"data", "Required":true}
         ]
    }'''  

    try:
        req_params = {}
        req_params['key'] = ['required']
        req_params['data'] = ['required']  

        _params = get_parameter(**req_params)

        decrypt= AESCipher(_params['key']).decrypt(_params['data'])
        result={'result' : decrypt}
        rs = {'status':200, 'message': 'OK', 'data': result}
        return api_response(**rs)   
    except Exception as e:
        rs = {'status':400, 'message': str(e), 'data': []}
        return api_response(**rs)      

@api_route(rule='/', params=None , methods=['GET', 'POST'])
def sys_encode():
    '''{ "Description": "AES Encrypt", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"data", "Name":"data", "Required":true}
         ]
    }'''  
    try:
        req_params = {'data': ['required']}
        _params = get_parameter(**req_params)

        encrypt= AESCipher(Config.SYS_AES_KEY).encrypt(_params['data'])
        result={'result' : encrypt}
        rs = {'status':200, 'message': 'OK', 'data': result}
        return api_response(**rs)  

    except Exception as e:
        rs = {'status':400, 'message': str(e), 'data': []}
        return api_response(**rs)    

@api_route(rule='/', params=None, methods=['GET', 'POST'])
def sys_decode():
    '''{ "Description": "AES Decrypt ", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"data", "Name":"data", "Required":true}
         ]
    }'''      
    try:
        req_params = { 'data': ['required']}
        _params = get_parameter(**req_params)

        decrypt= AESCipher(Config.SYS_AES_KEY).decrypt(_params['data'])
        result={'result' : decrypt}
        rs = {'status':200, 'message': 'OK', 'data': result}
        return api_response(**rs)   
    except Exception as e:
        rs = {'status':400, 'message': str(e), 'data': []}
        return api_response(**rs)     
