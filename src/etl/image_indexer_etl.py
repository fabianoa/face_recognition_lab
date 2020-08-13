import numpy as np
import faiss                   # make faiss available


if __name__ == "__main__":

    e=np.load('encodings.npy',allow_pickle=True).tolist()
    
    vectorEncoding= np.array([x.get('encondings') for x in e],dtype=np.float32)
    vectorId= np.array([x.get('id') for x in e])
            
    d=len(vectorEncoding[0])
    print('Tamanho d do vetor: {}'.format(d))
    
    index = faiss.IndexIVFFlat(d)   # build the index
    index2 = faiss.IndexIDMap(index)
    
    index2.add_with_ids(vectorEncoding, vectorId) 

    print('Tamanho do indice: {}'.format(index2.ntotal))
    faiss.write_index(index2, '10000.index')
