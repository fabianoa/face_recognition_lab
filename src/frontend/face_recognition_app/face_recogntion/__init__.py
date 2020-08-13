from flask import Blueprint

face_recognition = Blueprint('face_recognition', __name__)

from . import views
