from api.route import api_route
from lib.utils import route_info


@api_route(rule='', params=None, methods=['GET'])
def index():
    '''{ "Description": "MISC APIs", "Methods":"GET", "Content-Type":"application/json",
         "Parameters":[]
    }'''
    return route_info('misc')
