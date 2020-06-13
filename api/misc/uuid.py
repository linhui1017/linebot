from lib.utils import api_response
from api.route import api_route
from settings import Config
import uuid

@api_route(rule='/', params=None, methods=['GET', 'POST'])
def uuid1():
    '''{ "Description": "Python UUID1 基於MAC地址，時間戳，隨機數來生成唯一的uuid，可以保證全球範圍內的唯一性", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[]
    }'''   
    try:
        response_data = {}
        response_data['UUID'] = uuid.uuid1()
        return api_response(**response_data)  
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': []}
        return api_response(**rs) , 400 


req_params = {}
req_params['name'] = ['required']

@api_route(rule='/', params=req_params, methods=['GET', 'POST'])
def uuid3(args):
    '''{ "Description": "Python UUID3", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"Name", "Name":"name", "Required":true}

         ]
    }'''   
    try:
        response_data = {}
        response_data['UUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, args['name'])
        return api_response(**response_data)  
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': []}
        return api_response(**rs) , 400 

@api_route(rule='/', params=None, methods=['GET', 'POST'])
def uuid4():
    '''{ "Description": "Python UUID4 通過偽隨機數得到uuid，是有一定概率重複的", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[]
    }'''   
    try:
        response_data = {}
        response_data['UUID'] = uuid.uuid4()
        return api_response(**response_data)  
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': []}
        return api_response(**rs) , 400 

@api_route(rule='/', params=req_params, methods=['GET', 'POST'])
def uuid5(args):
    '''{ "Description": "Python UUID5", "Methods":"GET, POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"Name", "Name":"name", "Required":true}

         ]
    }'''   
    try:
        response_data = {}
        response_data['UUID'] = uuid.uuid5(uuid.NAMESPACE_URL, args['name'])
        return api_response(**response_data)  
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': []}
        return api_response(**rs) , 400         
