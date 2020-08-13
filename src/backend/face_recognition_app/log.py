import logging


def initialize_log():
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler("face_recognition_lab.log")
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    return log


log = initialize_log()
