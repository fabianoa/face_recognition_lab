
import face_recognition
import faiss   
import numpy as np
from pathlib import Path
from milvus import Milvus, IndexType, MetricType, Status
from  face_recognition_app.models.images import Images
from face_recognition_app import app

index=faiss.read_index(app.config['INDEXES_LOCATION']+'faiss.index')
embeddings=np.load(app.config['EMBEDDINGS_LOCATION']+'embeddings.npy',allow_pickle=True).tolist()  

milvus = Milvus(host=app.config['MILVUS_HOST'], port=app.config['MILVUS_PORT'])

MAX_RESULT=64

class Embeddings():   

  def is_similar(current_image_encoded,unknown_face_encodings):
    # match your image with the image and check if it matches
    result = face_recognition.compare_faces(unknown_face_encodings,current_image_encoded, tolerance=0.6)
      
    # check if it was a match
    if result[0] == True:
       return True
    else:
       return False
  
  def distance(current_image_encoded,unknown_face_encodings):
      return face_recognition.face_distance(unknown_face_encodings,current_image_encoded)
       

  def search_faiss(face_embedding,threshold,k=None):
      
      if(k is None):
          k=MAX_RESULT

      distances, indices=index.search(face_embedding, k)
      indices=indices[0].tolist()
      distances=distances[0].tolist()
      
      result=[]
   
      x = range(len(indices))
      for n in x:
         if distances[n]<=threshold :
            img=Images.get_image_from_s3(indices[n])
            result.append((img[0],img[1],distances[n])) 

      return result          
  
  def search_milvus(face_embedding,threshold,k=None):
      
      search_param = {'nprobe': 16}
      if(k is None):
          k=MAX_RESULT
      status,search_results=milvus.search(collection_name='celeba', query_records=face_embedding.tolist(), top_k=k, params=search_param)
      result=[]
      
      for row in search_results:
          for item in row:
            if item.distance<=threshold:
                img=Images.get_image_from_s3(int(item.id))
                result.append((img[0],img[1],item.distance))
            
      return result          
 

  def search_list(face_embedding,threshold,k=None):
      
      result=[]
      k_count=0

      if(k is None):
          k=MAX_RESULT

      for embedding in embeddings:
         distance = Embeddings.distance(face_embedding,embedding.get('encondings'))[0] 
         if (distance<=threshold):
             img=Images.get_image_from_s3(int(Path( embedding.get('image')).stem))
             result.append((img[0],img[1],distance))
             k_count+= 1
             if(k_count==k):
                 return result   

      return result 