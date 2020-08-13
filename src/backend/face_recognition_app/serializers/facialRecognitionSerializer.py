from face_recognition_app.restplus import api
from flask_restplus import fields

faces_serializer = api.model('Faces', {
    'faces': fields.List(fields.String,required=True),
    'execution_time':fields.String(readonly=True)

})

encode_serializer = api.model('Enconde', {
    'id': fields.String(readonly=True),
    'encode': fields.String(required=True)
})

similarity_serializer = api.model('Similarity', {
    'id': fields.String(readonly=True),
    'similars': fields.String(required=True)
})

