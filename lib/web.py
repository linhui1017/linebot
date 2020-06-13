# -*- coding: utf-8 -*-
from functools import wraps
from flask import  request, jsonify
import base64
from lib.Checker import isNone


def get_parameter(**_params):
    return  _get_parameter(**_params)

def _get_parameter(**_params):
    _result = {}

    if request.method in ['POST', 'DELETE'] :
        # if request.is_json == False:
        #     raise ValueError('JSON request required.')
        #content = request.get_json()  
        
        content = request.get_json() if request.is_json else (request.form if request.form else [])
        for key, value in _params.items():
            if (key in content):
                _result[key] =  content[key]
            elif (key.lower() in content):
                _result[key] =  content[key.lower()]
            else:
                _result[key] = None

            if ('required' in value):
                if (key not in _result) or isNone(_result[key]):
                    raise ValueError('{0} is required.'.format(key))

            if('base64' in value):
                if (not isNone(_result[key])):
                    _result[key] = str(base64.b64decode(_result[key])) 
            
    elif request.method == 'GET':
        for key, value in _params.items():
            if (request.args.get(key) is not None):
                _result[key] =  request.args.get(key) 
            elif (request.args.get(key.lower()) is not None):
                _result[key] =  request.args.get(key.lower()) 
            else:
                _result[key] = None

            if ('required' in value):
                if isNone(_result[key]):
                    raise ValueError('{0} is required.'.format(key))
                    
            if('base64' in value):
                if (not isNone(_result[key])):
                    _result[key] = str(base64.b64decode(_result[key])) 

    return _result
