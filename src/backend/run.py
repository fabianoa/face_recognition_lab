from face_recognition_app import app
from face_recognition_app.log import log

if __name__ == '__main__':
    log.info(
        '>>>>> Starting development server at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(host='0.0.0.0')