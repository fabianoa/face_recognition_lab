
import os
import sys
import commom.face_encoding as fe
import numpy as np

import logging
import time


logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

    
def criaListaEncoding(encondings,imagepath):
        e=fe.get_image_face_encondings(imagepath)
        if e is not None:
            encondings.append(e)

def get_image_face_encondings_folder(folder):
    
    import  multiprocessing 

    start_time = time.time()
    images = os.listdir(folder)
   
    result = []
    manager = multiprocessing.Manager()
    encondings = manager.list()
          
    pool=multiprocessing.Pool(processes= multiprocessing.cpu_count()*5-1)

    for image in images:
        # load the image
        imagepath=folder +"/"+image
        pool.apply_async(criaListaEncoding,(encondings,imagepath))
    
    pool.close()
    pool.join()
    
    result=list(encondings) 
    print("--- Tempo de processamento de  {} imagens em segundos: {} segundos ---".format(len(result), ((time.time() - start_time))))
    
    return result

if __name__ == "__main__":
    
    folder = sys.argv[1] if len(sys.argv) > 1 else "data/imagens"
    e=get_image_face_encondings_folder(folder)
    np.save('encodings.npy',e)


    