from face_recognition_app.commom import face_recognition as fr
from face_recognition_app.models.embeddings import Embeddings as eb
import numpy as np
import cv2
import time

class FacialRecognitionBus(object):
    
    def detect_faces(self,image,method='hog',crop=False):
       
        start_time = time.time()

        switcher ={
            'hog':fr.detect_faces_hog,
            'haar':fr.detect_faces_haar,
            'cnn':fr.detect_faces_cnn,
            'mtcnn':fr.detect_faces_mtcnn,
            'ssd':fr.detect_faces_mobilenet_ssd
        }

        func = switcher.get(method)
        face_location=func(image)
        
        result=[]

        if(crop):
            faces=fr.crop_faces(image,face_location)
            for face in faces:
                is_success, buffer = cv2.imencode(".jpg", face)
                if(is_success):
                    result.append(buffer)
        else:
            faces=fr.mark_faces(image,face_location)
            is_success, buffer = cv2.imencode(".jpg", faces)
            if(is_success):
                result.append(buffer)

        execution_time=time.time() - start_time

        return (result,face_location,execution_time)

    
    def detect_align_faces(self,image,method='mtcnn'):
        
        start_time = time.time()

        faces,face_locations,execution_time = self.detect_faces(image,method=method)
        
        if len(faces):
           align_faces = fr.align_faces(image,face_locations)

        execution_time=time.time() - start_time 
        
        return (align_faces,execution_time)


    def verify_faces(self,current_image,unknown_image):

        start_time = time.time()

        current_faces,execution_time=self.detect_align_faces(current_image)
        
        current_embeddings =[]
        unknown_embeddings =[] 

        # extract face embeddings 
        if(len(current_faces)):
            for face in current_faces:
                embedding = fr.get_face_embeddings(face)
                if embedding is not None:
                    current_embeddings.append((face,embedding))
        
            unknown_faces,execution_time=self.detect_align_faces(unknown_image)
            for face in unknown_faces:
                embedding = fr.get_face_embeddings(face)
                if embedding is not None:
                    unknown_embeddings.append((face,embedding))
        
        #Verify similarity beteewn embeddings
        result = []
        for ue in unknown_embeddings:
            for ce in current_embeddings:
                 if(eb.is_similar(ue[1],ce[1])):
                    result.append((ue[0],ce[0]))
        
        execution_time=time.time() - start_time 

        return (result,execution_time)
        
    
    def search_faces(self,image,threshold,k,source):
        
        start_time = time.time()

        switcher ={
            'list':eb.search_list,
            'faiss':eb.search_faiss,
            'milvus':eb.search_milvus
        }

        func = switcher.get(source)

        image_faces,execution_time=self.detect_align_faces(image)
        result = []
        for face in image_faces:
            face_embedding = fr.get_face_embeddings(face)
            if face_embedding is not None:
                start_time = time.time()                                
                result.append(func(face_embedding,threshold,k))
        
        execution_time=time.time() - start_time  

        return (result,execution_time)