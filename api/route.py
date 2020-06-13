from flask import Blueprint
from settings import Config
from lib.utils import token_required, route_info, api_response, logger
from lib.web import get_parameter
from lib.Checker import isNone
import re 
import pkgutil 

prefix = 'api'
apiprint = Blueprint(prefix, __name__)
@apiprint.route('/', methods=['GET'])
def index():
    """API列表 (＊Token required )"""
    return route_info(prefix)

urlcheck = re.compile(r'^api(\.\w+)+') 

def api_route(bpt=apiprint, rule=None, params=None, **options):
    def decorator(func):
        encode_rule = rule
        if (rule is not None and rule == '/'):
            '''routing by function name'''
            encode_rule = '/{0}'.format(func.__name__)
        elif (rule is None or len(str(rule)) == 0):
            '''routing by file name'''
            encode_rule = ''
        
        path = ''

        if(urlcheck.match(func.__module__) is None):
            logger.error('API Blueprint: invalid api path!')
            if(Config.DEBUG):
                raise Exception('API Blueprint: invalid api path!')   
        else:
            path = '/{0}{1}'.format('/'.join(re.split(r'\b\.\b', func.__module__)[1:]), encode_rule)

        options.update( {'endpoint' : path} )
        
        @bpt.route(path, **options)
        def route_wrapper(*args, **kwargs):
            try:
                if(not isNone(params)):
                    kwargs['args'] = get_parameter(**params)
                return func(*args, **kwargs)                         
            except ValueError as e:
                rs = {'success':False, 'message': str(e), 'data': []}  
                return api_response(**rs), 400
        route_wrapper.__doc__ = func.__doc__    
        return route_wrapper
    return decorator
