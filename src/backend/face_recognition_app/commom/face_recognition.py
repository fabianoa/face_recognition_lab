
import face_recognition
import face_alignment
from mtcnn.mtcnn import MTCNN
import numpy as np
import cv2
import sys
from  face_recognition_app.commom import images_utils as ui
from face_recognition_app import app

mobilenet_ssd = cv2.dnn.readNetFromCaffe(app.config['MODEL_LOCATION']+'res10_300x300_ssd_iter_140000.prototxt.txt', app.config['MODEL_LOCATION']+'res10_300x300_ssd_iter_140000.caffemodel')


def convert_boxes_to_top_right_botton_left(face_locations):
    result=[]
    for (x, y, w, h) in face_locations:
       result.append([y, x + w,y + h,x]) 
    return np.array(result)

def image_decode(image):
    npimg = np.fromstring(image, np.uint8)
    return cv2.imdecode(npimg,flags=1)

def mark_faces(image,face_locations,text=None):

    img=image_decode(image)

    for (top,right,bottom,left) in face_locations:
      y = top - 10 if top - 10 > 10 else top + 10
      cv2.putText(img, text, (left, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
      cv2.rectangle(img,(left,bottom),(right,top),(0, 255, 0), 1)
    
    return img

def crop_faces(image,face_locations):

    img=image_decode(image)
    
    result=[]
    for (top,right,bottom,left) in face_locations:
      cropped_img=img[top:bottom, left:right]
      result.append(cropped_img)
      
    return result

def detect_faces_haar(image):
    
    img=image_decode(image)
    
    img_cvt_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(
        img_cvt_color,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )
    #convert to pattern top,right,bottom,left
    face_locations = convert_boxes_to_top_right_botton_left(faces)
    
    return face_locations


def detect_faces_hog(image):
    
    img=image_decode(image)
    
    img_cvt_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(img_cvt_color, model="hog")
    
    return face_locations


def detect_faces_cnn(image):
    
    img=image_decode(image)
        
    img_cvt_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(img_cvt_color, model="cnn")
    
    for (top,right,bottom,left) in face_locations:
        cv2.rectangle(img,(left,bottom),(right,top),(0, 255, 0), 1)
        
    return face_locations

def detect_faces_mtcnn(image):
    
    img=image_decode(image)
    
    img_cvt_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # initialise the detector class.
    detector = MTCNN()

    # detect faces from input image.
    faces = detector.detect_faces(img_cvt_color)

    faces_locations=[]
    # draw bounding box and five facial landmarks of detected face
    for face in zip(faces):
        faces_locations.append(face[0]['box'])
        #landmarks = face[0]['keypoints']
        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
        #for key, point in landmarks.items():
            #cv2.circle(img, point, 2, (255, 0, 0), 6)
    
    face_locations = convert_boxes_to_top_right_botton_left(faces_locations)
    
    return face_locations


def detect_faces_mobilenet_ssd(image):
    
    img=image_decode(image)
    
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img,(300, 300)),1.0,(300, 300),(104.0, 117.0, 123.0))
    mobilenet_ssd.setInput(blob)
    detections = mobilenet_ssd.forward()
        
    faces_location=[]

    # loop over the detections
    for i in range(detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
	    # prediction
        confidence = detections[0, 0, i, 2]

	    # filter out weak detections by ensuring the `confidence` is
	    # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
           
            faces_location.append([startY,endX,endY,startX])
		    #text = "{:.2f}%".format(confidence * 100)
		    
    return np.array(faces_location)

    

def get_face_landmark(image,face_location,model='dlib'):

    if(model=='dlib'):
       face_landmarks = face_recognition.face_landmarks(image,face_locations=[face_location])
    else:
     if (model=='sfd'):
        # sfd for SFD, dlib for Dlib and folder for existing bounding boxes.
        fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, face_detector='sfd',device='cpu')
        face_landmarks=fa.get_landmarks(image,detected_faces=[face_location])[-1]
    
    return face_landmarks

def align_faces(image,face_locations):
    # load image and face locations.
    img=image_decode(image)

    img_cvt_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result=[]

    for face in face_locations:
        face_landmarks = get_face_landmark(img_cvt_color,model='dlib',face_location=face)
        if len(face_landmarks):
            aligned_face=align_face(img,face,face_landmarks)
            result.append(aligned_face)
    
    return result

def align_face(img,face_location,face_landmarks,show_landmark=True):
    '''
    Let's find and angle of the face. First calculate 
    the center of left and right eye by using eye landmarks.
    '''
    leftEyePts = face_landmarks[0]['left_eye']
    rightEyePts = face_landmarks[0]['right_eye']
    
    leftEyeCenter = np.array(leftEyePts).mean(axis=0).astype("int")
    rightEyeCenter = np.array(rightEyePts).mean(axis=0).astype("int")

    leftEyeCenter = (leftEyeCenter[0],leftEyeCenter[1])
    rightEyeCenter = (rightEyeCenter[0],rightEyeCenter[1])
    
    if(show_landmark):
        # draw the circle at centers and line connecting to them
        cv2.circle(img, leftEyeCenter, 2, ( 0,255, 0), 2)
        cv2.circle(img, rightEyeCenter, 2, ( 0,255, 0), 2)
        cv2.line(img, leftEyeCenter, rightEyeCenter, (0,255,0), 1)

    # find and angle of line by using slop of the line.
    dY = rightEyeCenter[1] - leftEyeCenter[1]
    dX = rightEyeCenter[0] - leftEyeCenter[0]
    angle = np.degrees(np.arctan2(dY, dX))

    # to get the face at the center of the image,
    # set desired left eye location. Right eye location 
    # will be found out by using left eye location.
    # this location is in percentage.
    desiredLeftEye=(0.35, 0.35)
    #Set the croped image(face) size after rotaion.
    desiredFaceWidth = 128
    desiredFaceHeight = 128

    desiredRightEyeX = 1.0 - desiredLeftEye[0]
 
    # determine the scale of the new resulting image by taking
    # the ratio of the distance between eyes in the *current*
    # image to the ratio of distance between eyes in the
    # *desired* image
    dist = np.sqrt((dX ** 2) + (dY ** 2))
    desiredDist = (desiredRightEyeX - desiredLeftEye[0])
    desiredDist *= desiredFaceWidth
    scale = desiredDist / dist

    # compute center (x, y)-coordinates (i.e., the median point)
    # between the two eyes in the input image
    eyesCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2,(leftEyeCenter[1] + rightEyeCenter[1]) // 2)

    # grab the rotation matrix for rotating and scaling the face
    M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)

    # update the translation component of the matrix
    tX = desiredFaceWidth * 0.5
    tY = desiredFaceHeight * desiredLeftEye[1]
    M[0, 2] += (tX - eyesCenter[0])
    M[1, 2] += (tY - eyesCenter[1])

    # apply the affine transformation
    (w, h) = (desiredFaceWidth, desiredFaceHeight)
    (y2,x2,y1,x1) = face_location 
        
    output = cv2.warpAffine(img, M, (w, h),flags=cv2.INTER_CUBIC)

    is_success, buffer = cv2.imencode(".jpg", output) 

    return buffer

def get_face_embeddings(image):

    img=image_decode(image)

    img_cvt_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
    # encode the loaded image into a feature vector
    current_image_encoded = face_recognition.face_encodings(img_cvt_color,num_jitters=10)

    if len(current_image_encoded) > 0:
        return np.array([current_image_encoded[0]],dtype=np.float32)
    else:
        return None





