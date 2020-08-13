# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import  SubmitField,RadioField,DecimalField,IntegerField
from wtforms.validators import DataRequired,Optional
from flask_wtf.file import FileField, FileRequired


class FaceDetectionForm(FlaskForm):
    """
    Form for detect faces
    """
    fileName = FileField('File', validators=[FileRequired()])
    method = RadioField('Face Detection Method', validators=[DataRequired()], choices=[('haar','Haar method'),('hog','Hog method'),('cnn','CNN method'),('mtcnn','MTCNN method'),('ssd','MobileNet SSD method')], default='mtcnn')
    action = RadioField('Face Detection Action', validators=[DataRequired()], choices=[('mark','Mark image'),('crop','Crop image')], default='mark')
    submit = SubmitField('Submit')

class FaceAlignmentForm(FlaskForm):
    """
    Form for align faces
    """
    fileName = FileField('File', validators=[FileRequired()])
    #method = RadioField('Face Detection Method', validators=[DataRequired()], choices=[('haar','Haar method'),('hog','Hog method'),('cnn','CNN method'),('mtcnn','MTCNN method')], default='hog')
    submit = SubmitField('Submit')

class FaceVerificationForm(FlaskForm):
    """
    Form for verify
    """
    file_name_base = FileField('File Base', validators=[FileRequired()])
    file_name_verified = FileField('File Verified', validators=[FileRequired()])
    submit = SubmitField('Submit')

class FaceSearchForm(FlaskForm):
    """
    Form for detect faces
    """
    fileName = FileField('File', validators=[FileRequired()])
    source = RadioField('Source of Search', validators=[DataRequired()], choices=[('list','List source'),('faiss','Faiss source'),('milvus','Milvus Source')], default='faiss')
    threshold = DecimalField('Distance Threshold', validators=[DataRequired()], default=0.2)
    k = IntegerField('K (number of faces returned)', validators=[Optional()])
    
    submit = SubmitField('Submit')
