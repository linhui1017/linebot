from flask import jsonify, request, Response, render_template
from flask import current_app as app
from functools import wraps
import dicttoxml

import json
import jwt
from datetime import datetime, timedelta, date

from settings import Config, Message
import time




#  Gunicorn Error Log
import logging
logger = logging.getLogger("gunicorn.error")

# # API usage document via FLASK
# def route_info(prefix):
#     """Print available functions."""
#     func_list = {}
#     for rule in app.url_map.iter_rules():
#         if rule.endpoint != 'static':
#             if (prefix == None) or ("/{}/".format(prefix) in rule.rule):
#                 func_list[rule.rule] = "[{}]:{}".format(rule.methods, app.view_functions[rule.endpoint].__doc__)

#     return jsonify(func_list)

# API usage document via FLASK
def route_info(prefix):

    """Print available functions."""
    func_list = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            if (prefix == None) or ("/{}/".format(prefix) in rule.rule):
                finc = {}
                finc['uri'] = rule.rule
                finc['method'] = 'POST' if('POST' in rule.methods) else 'GET'
                try:
                    doct = json.loads(s=app.view_functions[rule.endpoint].__doc__)
                    finc['doc'] = doct
                except Exception as e:
                    finc['doc'] = app.view_functions[rule.endpoint].__doc__

                func_list.append(finc)
    return render_template('index.html', docs=func_list)
    #return jsonify(func_list)

# JWT authenticated decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if Config.TOKEN_REQUIRED:
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'status':False, 'message': Message.TOKEN_IS_MISING}), 401

            try:
                data = jwt.decode(token, Config.SECRET_KEY)

                if not ( data['user_id'] == Config.AUTH_USER ):
                    return jsonify({'status':False, 'message': Message.TOKEN_IS_MISING}), 401     
            except:
                return jsonify({'status':False, 'message': Message.TOKEN_IS_MISING}), 401 

        return f(*args, **kwargs)
    return decorated

# JWT authenticated decorator
def before_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        print(1, request.headers.get('User-Agent'))
        return f(*args, **kwargs)
    return decorated    

import cx_Oracle
from uuid import UUID
from sqlalchemy.orm.state import InstanceState

time_offset = int((time.altzone/3600))
time_offset_str = str(time_offset) if time_offset > 0 else '+{0}'.format(str(-time_offset))

def jsonconverter(o):
    if isinstance(o,datetime):
        #o = o + timedelta(hours=time_offset) 
        #return o.strftime("%Y-%m-%dT%H:%M:%S.%f")  
        #return o.strftime("%Y-%m-%d %H:%M:%S")
        #return o.strftime("%Y-%m-%dT%H:%M:%S.%f %Z")
        #return o.strftime("%a %b %d %Y %H:%M:%S.%f GMT{0}".format(time_offset_str))  
        return o.strftime("%a %b %d %Y %H:%M:%S GMT{0}".format(time_offset_str))  
    if isinstance(o,InstanceState):
        return o.__str__()
    if isinstance(o, UUID):
        return o.__str__()
    if isinstance(o, cx_Oracle.LOB):
        return o.read()
    if isinstance(o, cx_Oracle.DATETIME): 
        #return o.strftime("%Y-%m-%d %H:%M:%S") 
        #return o.strftime("%Y-%m-%dT%H:%M:%S.%f %Z")   
        #return o.strftime("%a %b %d %Y %H:%M:%S.%f GMT{0}".format(time_offset_str))  
        return o.strftime("%a %b %d %Y %H:%M:%S GMT{0}".format(time_offset_str)) 
    else:
        return o.__str__()

# api response format
def api_response(**data):

    if not data:
        return jsonify({'status':400, 'message': 'Posted data not matched!'})

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/xml') or (content_type == 'text/xml'):
        #return Response(dict2XML(data, utf8=True).decode("utf-8"), mimetype='application/xml')
        return Response(dicttoxml.dicttoxml(data), mimetype='application/xml')
    else:
        return Response(json.dumps(data, default = jsonconverter, ensure_ascii=False), mimetype='application/json', headers={'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Credentials':'true'}) 

# api response format
def json_response(jsonstr):

    if not jsonstr:
        return jsonify({'status':400, 'message': 'Posted data not matched!'})

    return Response(jsonstr, mimetype='application/json') 
        

from  lib.AESCipher import AESCipher 



import socket

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('172.16.254.51', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


#獲取本月第一天
def first_day_of_month():
    return date.today() - timedelta(days=datetime.now().day - 1)

#獲取本週第一天
def first_day_of_week():
    return date.today() - timedelta(days=date.today().weekday())

#獲取本週最後一天
def last_day_of_week():
    return date.today() + timedelta(days=(6-date.today().weekday()))    