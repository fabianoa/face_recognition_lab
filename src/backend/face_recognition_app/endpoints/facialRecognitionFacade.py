from face_recognition_app.restplus import api
from face_recognition_app.serializers.facialRecognitionSerializer import encode_serializer,faces_serializer
from face_recognition_app.serializers.facialRecognitionSerializer import similarity_serializer
from face_recognition_app.business.facialRecognitionBus import FacialRecognitionBus

from werkzeug.datastructures import FileStorage
import base64

from flask_restplus import Resource
from flask import jsonify
from flask import abort, send_file

ns_facialrecognition = api.namespace('facialrecognition',
                            description='Operations related to facial recognition')


face_detection_parser = api.parser()
face_detection_parser.add_argument('file', location='files',
                   type=FileStorage, required=True)
face_detection_parser.add_argument('method', required=True, location='form')
face_detection_parser.add_argument('action', required=True, location='form')

face_alignment_parser = api.parser()
face_alignment_parser.add_argument('file', location='files',
                   type=FileStorage, required=True)
face_alignment_parser.add_argument('method', required=True, location='form')

face_verification_parser = api.parser()
face_verification_parser.add_argument('file_base', location='files',
                   type=FileStorage, required=True)
face_verification_parser.add_argument('file_verified', location='files',
                   type=FileStorage, required=True)

face_search_parser = api.parser()
face_search_parser.add_argument('file', location='files',
                   type=FileStorage, required=True)
face_search_parser.add_argument('source', required=True, location='form')
face_search_parser.add_argument('threshold', required=True, location='form')
face_search_parser.add_argument('k', required=False, location='form')

@ns_facialrecognition.route('/')
class FacialRecognitionCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(FacialRecognitionCollection, self).__init__(api, args, kwargs)
        self.bus = FacialRecognitionBus()


@ns_facialrecognition.route('/face_detection')
@api.expect(face_detection_parser)
@api.response(404, 'Face detection  not found.')
class FaceDetectionItem(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(FaceDetectionItem, self).__init__(api, args, kwargs)
        self.bus = FacialRecognitionBus()

    @api.marshal_with(faces_serializer, code=201)
    def post(self):
        args = face_detection_parser.parse_args()
        method=args['method']
        uploaded_file = args['file']
        action=args['action']

        file_content=uploaded_file.read()

        if(action=='mark'):
            faces,face_locations,execution_time=self.bus.detect_faces(file_content,method,False)
        else:
            faces,face_locations,execution_time=self.bus.detect_faces(file_content,method,True)

        result=[]
        print(type(execution_time))
        for face in faces:
            result.append(base64.b64encode(face).decode('utf-8'))
        
        return {'faces':result,'face_locations':face_locations,'execution_time':execution_time}
        #return send_file(result, mimetype='image/jpeg')

@ns_facialrecognition.route('/face_align')
@api.expect(face_alignment_parser)
@api.response(404, 'Align Faces not found.')
class FaceAlignItem(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(FaceAlignItem, self).__init__(api, args, kwargs)
        self.bus = FacialRecognitionBus()

    #@api.marshal_with(encode_serializer, code=201)
    def post(self):
        args = face_alignment_parser.parse_args()
        uploaded_file = args['file']
        method=args['method']
        file_content=uploaded_file.read()

        align_faces,execution_time=self.bus.detect_align_faces(file_content,method)
        
        result=[]

        for face in align_faces:
            result.append(base64.b64encode(face).decode('utf-8'))

        return {'faces':result,'execution_time':execution_time}
        #return send_file(result, mimetype='image/jpeg')


@ns_facialrecognition.route('/face_verification')
@api.expect(face_verification_parser)
@api.response(404, 'Face verification not found.')
class FaceVerificationItem(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(FaceVerificationItem, self).__init__(api, args, kwargs)
        self.bus = FacialRecognitionBus()

    #@api.marshal_with(faces_serializer, code=201)
    def post(self):
        args = face_verification_parser.parse_args()
        uploaded_file_base = args['file_base']
        file_content_base=uploaded_file_base.read()
        
        uploaded_file_verified = args['file_verified']
        file_content_verified=uploaded_file_verified.read()
        
        similars,execution_time=self.bus.verify_faces(file_content_base,file_content_verified)
        
        result=[]
        for similar in similars:
            result.append([base64.b64encode(similar[0]).decode('utf-8'),base64.b64encode(similar[1]).decode('utf-8')])

        return {'similars':result,'execution_time':execution_time}
        #return send_file(result, mimetype='image/jpeg')



@ns_facialrecognition.route('/face_search')
@api.expect(face_search_parser)
@api.response(404, 'Face Search not found.')
class FaceSearchItem(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(FaceSearchItem, self).__init__(api, args, kwargs)
        self.bus = FacialRecognitionBus()

    #@api.marshal_with(similarity_serializer, code=201)
    def post(self):
        args = face_search_parser.parse_args()
        uploaded_file = args['file']
        source=args['source']
        if(args['k'] is not None):
            k=int(args['k'])
        else:
            k=None
        threshold=float(args['threshold'])
        file_content=uploaded_file.read()
        search_result,execution_time=self.bus.search_faces(file_content,threshold,k,source)
        
        result=[]
        #print(search_result)
        for row in search_result:
          for face in row:
            result.append({'file_name':face[0],'image':base64.b64encode(face[1]).decode('utf-8'),'distance':face[2]})
        
        return {'search_result':result,'execution_time':execution_time} 
