from flask import Flask, Blueprint
from face_recognition_app.restplus import api

import os

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object('face_recognition_app.config.DevelopmentConfig')
app.config.from_pyfile('config.py')

app.config['RESTPLUS_VALIDATE'] = True
app.config['ERROR_404_HELP'] = False

from face_recognition_app.endpoints.facialRecognitionFacade import ns_facialrecognition
from face_recognition_app.log import log
from face_recognition_app import  config


#config_db(app)
blueprint = Blueprint('api', __name__)
api.init_app(blueprint)
api.add_namespace(ns_facialrecognition)
app.register_blueprint(blueprint)

