# app/admin/views.py
import os
from flask import abort, flash, redirect, render_template, url_for,request
from flask_login import current_user, login_required

from werkzeug.utils import secure_filename
import requests
from io import BytesIO
import base64
import json            

from . import face_recognition
from .forms import FaceDetectionForm,FaceAlignmentForm,FaceVerificationForm,FaceSearchForm
from flask import current_app, Flask
from face_recognition_app import app


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@face_recognition.route('/faces/detect', methods=['GET', 'POST'])
@login_required
def detect_face():
    
    check_admin()
    form = FaceDetectionForm()
    
    if form.validate_on_submit():
        
        method=form.method.data
        f = form.fileName.data
        action=form.action.data

        filename = secure_filename(f.filename)
        in_memory_file = BytesIO()
        f.save(in_memory_file)

        content = in_memory_file.getvalue()
        input_image=base64.b64encode(content).decode('utf-8')

        url = app.config['BACKEND_URI']+'/facialrecognition/face_detection'
    
        file = {"file": (filename, content,'image/jpeg')}
        data = {"method":method,"action":action}

        try:
            r = requests.post(url, files=file, data=data)
            r.raise_for_status()
             #current_app.logger.info(t)
            faces=json.loads(r.content)['faces']
            execution_time=json.loads(r.content)['execution_time']

            return render_template('face_recognition/face_detection/face_detection.html',input_image=input_image,action=action,faces=faces,execution_time=execution_time,result=True,form=form, title="Faces")
        except requests.exceptions.HTTPError as err:
            flash(err)
            #current_app.logger.info(err.response.text)
        except requests.ConnectionError as conn_err:
            flash(conn_err)
            current_app.logger.info(conn_err)
  
         
    # load face_detection template
    return render_template('face_recognition/face_detection/face_detection.html',form=form, title="Faces")


@face_recognition.route('/faces/align', methods=['GET', 'POST'])
@login_required
def align_face():
    check_admin()
    form = FaceDetectionForm()
    
    if form.validate_on_submit():
        
        #method=form.method.data
        f = form.fileName.data
        
        filename = secure_filename(f.filename)
        in_memory_file = BytesIO()
        f.save(in_memory_file)

        content = in_memory_file.getvalue()
        input_image=base64.b64encode(content).decode('utf-8')

        url = app.config['BACKEND_URI']+'/facialrecognition/face_align'
    
        file = {"file": (filename, content,'image/jpeg')}
        data = {"method":'mtcnn'}

        try:
            r = requests.post(url, files=file, data=data)
            r.raise_for_status()
             #current_app.logger.info(t)
            faces=json.loads(r.content)['faces']
            execution_time=json.loads(r.content)['execution_time']

            return render_template('face_recognition/face_align/face_align.html',input_image=input_image,faces=faces,execution_time=execution_time,result=True,form=form, title="Faces Alignment")
        except requests.exceptions.HTTPError as err:
            flash(err)
            #current_app.logger.info(err.response.text)
        except requests.ConnectionError as conn_err:
            flash(conn_err)
            current_app.logger.info(conn_err)
  
         
    # load face_detection template
    return render_template('face_recognition/face_align/face_align.html',form=form, title="Faces Alignment")



@face_recognition.route('/faces/verify', methods=['GET', 'POST'])
@login_required
def verify_face():
    
    check_admin()
    form = FaceVerificationForm()

    if form.validate_on_submit():
        fb = form.file_name_base.data
        filename_base = secure_filename(fb.filename)
        in_memory_file_base = BytesIO()
        fb.save(in_memory_file_base)

        content_base = in_memory_file_base.getvalue()
        input_image_base=base64.b64encode(content_base).decode('utf-8')

        fv = form.file_name_verified.data
        file_name_verified = secure_filename(fv.filename)
        in_memory_file_verified = BytesIO()
        fv.save(in_memory_file_verified)

        content_verified = in_memory_file_verified.getvalue()
        
        #current_app.logger.info(fv)
        
        input_image_verified=base64.b64encode(content_verified).decode('utf-8')

        url = app.config['BACKEND_URI']+'/facialrecognition/face_verification'
    
        file = {"file_base": (filename_base, content_base,'image/jpeg'),"file_verified": (file_name_verified, content_verified,'image/jpeg')}
        
        try:
            r = requests.post(url, files=file)
            r.raise_for_status()
             #current_app.logger.info(t)
            similars=json.loads(r.content)['similars']
            execution_time=json.loads(r.content)['execution_time']

            return render_template('face_recognition/face_verification/face_verification.html',input_image_base=input_image_base,input_image_verified=input_image_verified,similars=similars,execution_time=execution_time,result=True,form=form, title="Faces Alignment")
        except requests.exceptions.HTTPError as err:
            flash(err)
            #current_app.logger.info(err.response.text)
        except requests.ConnectionError as conn_err:
            flash(conn_err)
            current_app.logger.info(conn_err)
  

    # load face_detection template
    return render_template('face_recognition/face_verification/face_verification.html',form=form, title="Face Verification")


@face_recognition.route('/faces/search', methods=['GET', 'POST'])
@login_required
def search_face():
    
    check_admin()
    form = FaceSearchForm()
    
    if form.validate_on_submit():
        
        source=form.source.data
        threshold=form.threshold.data
        k=form.k.data
        f = form.fileName.data
        
        filename = secure_filename(f.filename)
        in_memory_file = BytesIO()
        f.save(in_memory_file)

        content = in_memory_file.getvalue()
        input_image=base64.b64encode(content).decode('utf-8')

        #current_app.logger.info(k)

        url = app.config['BACKEND_URI']+'/facialrecognition/face_search'
    
        file = {"file": (filename, content,'image/jpeg')}
        data = {"source":source,"threshold":threshold,"k":k}

        try:
            r = requests.post(url, files=file, data=data)
            r.raise_for_status()
             #current_app.logger.info(t)
            faces=json.loads(r.content)['search_result']
            execution_time=json.loads(r.content)['execution_time']

            return render_template('face_recognition/face_search/face_search.html',input_image=input_image,faces=faces,execution_time=execution_time,result=True,form=form, title="Face Search")
        except requests.exceptions.HTTPError as err:
            flash(err)
            #current_app.logger.info(err.response.text)
        except requests.ConnectionError as conn_err:
            flash(conn_err)
            current_app.logger.info(conn_err)
  
         
    # load face_detection template
    return render_template('face_recognition/face_search/face_search.html',form=form, title="Faces Search")
