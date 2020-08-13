
import face_recognition
import numpy as np
import cv2
from pathlib import Path

def check_rotation_image(img):
    
    image_returned = img
    face_locations = face_recognition.face_locations(img, model="hog")

    if not len(face_locations):
        for angle in [90,-90,180,-180]:
            rimg = rotateAndScale(img, degreesCCW=angle)
            face_locations = face_recognition.face_locations(rimg, model="hog")

            if len(face_locations):
                image_returned = rimg
                break
        
    
    return (image_returned,face_locations)


def rotateAndScale(img, scaleFactor = 1.0, degreesCCW = 90):
    (oldY,oldX) = img.shape[:2] #note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
    M = cv2.getRotationMatrix2D(center=(oldX/2,oldY/2), angle=degreesCCW, scale=scaleFactor) #rotate about center of image.

    #choose a new image size.
    newX,newY = oldX*scaleFactor,oldY*scaleFactor
    #include this if you want to prevent corners being cut off
    r = np.deg2rad(degreesCCW)
    newX,newY = (abs(np.sin(r)*newY) + abs(np.cos(r)*newX),abs(np.sin(r)*newX) + abs(np.cos(r)*newY))

    #the warpAffine function call, below, basically works like this:
    # 1. apply the M transformation on each pixel of the original image
    # 2. save everything that falls within the upper-left "dsize" portion of the resulting image.

    #So I will find the translation that moves the result to the center of that region.
    (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
    M[0,2] += tx #third column of matrix holds translation, which takes effect after rotation.
    M[1,2] += ty

    rotatedImg = cv2.warpAffine(img, M, dsize=(int(newX),int(newY)))
    return rotatedImg


def get_image_face_encondings(imagePath):
    current_image = face_recognition.load_image_file(imagePath)
    (current_image,face_locations) = check_rotation_image(current_image)

    # encode the loaded image into a feature vector
    current_image_encoded = face_recognition.face_encodings(current_image,known_face_locations=face_locations)

    if len(current_image_encoded) > 0:
        imageId=int(Path(imagePath).stem)
        return ({'id':imageId,'encondings':current_image_encoded[0]})
    else:
        return None
