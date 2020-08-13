import numpy as np
from pathlib import Path
from milvus import Milvus, IndexType, MetricType, Status

if __name__ == "__main__":
    
    milvus = Milvus(host='localhost', port='19530')

    collection_name='celeba'

    encodings=np.load('encodings.npy',allow_pickle=True).tolist()
    
    vectorEncoding = []
    vectorId =[]

    for encoding in encodings:
        vectorEncoding.append(encoding['encondings'].tolist())
        vectorId.append(encoding['id'])

    status, inserted_vector_ids = milvus.insert(collection_name=collection_name, records=vectorEncoding,ids=vectorId)
    
    milvus.flush([collection_name])
   
