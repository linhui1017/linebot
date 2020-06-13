from flask import Flask
from flask_cors import CORS

from lib import utils
from settings import Config
import logging
import os
from db.dbredis import RedisMgr
from lib.utils import get_host_ip
from datetime import datetime

app = Flask(__name__)

# from flask_restful import Resource, Api
# from api.testOne import testOne
# flask_api = Api(app)
# flask_api.add_resource(testOne, '/ttttt')


# Bind gunicorn logger
if __name__ != "__main__":
    gunicorn_logger = utils.logger
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Cross-Origin Resource Sharing
CORS(app)

# Config
app.config.from_object(Config)

#initial redis and test
# try:
#     RedisMgr.initial(app)
#     RedisMgr.get_store().set('flask-api-'+ get_host_ip() , datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  600)
# except Exception as identifier:
#     app.logger.error('redis initialize error:' + Config.REDIS_URL)
#     pass


def blueprint_validate_session_in_stock():
    #print('this is [before_request] in blueprint')
    pass

import pkgutil 
def initialize_route(flask_app):
    app.logger.info('initialize routes ...')
   
    flask_app.before_request(blueprint_validate_session_in_stock)
 
    import api.route
    flask_app.register_blueprint(api.route.apiprint, url_prefix='/{0}'.format(api.route.prefix))   


initialize_route(app)

""" 
  To use SQLAlchemy in a declarative way with your application,
  you just have to put the following code into your application module. 
  Flask will automatically remove database sessions at the end of the request
   or when the application shuts down
"""

from db.database import db_session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def help():
    """所有API列表"""
    return utils.route_info(None)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)


