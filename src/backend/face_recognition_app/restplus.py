import traceback
from face_recognition_app.log import log
from flask_restplus import Api

api = Api(version='1.0', title='Facial Recognition API')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    return {'message': message}, 500
