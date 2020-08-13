class Base():
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Base):
    DEBUG = True
    DEVELOPMENT = True
    INDEXES_LOCATION = '../../data/indexes/'
    IMAGES_LOCATION='../../data/images/img_align_celeba/'
    EMBEDDINGS_LOCATION='../../data/embeddings/'
    MODEL_LOCATION='../../models/'
    
    MILVUS_HOST='localhost'
    MILVUS_PORT=19530
    MINIO_URI='http://localhost:9000'
    
class TestingConfig(Base):
    DEBUG = False
    TESTING = True
    
class ProductionConfig(Base):
    DEBUG = False
    INDEXES_LOCATION = '/data/indexes/'
    IMAGES_LOCATION='/data/images/img_align_celeba/'
    EMBEDDINGS_LOCATION='/data/embeddings/'
    MODEL_LOCATION='/models/'
    MILVUS_HOST='milvus'
    MILVUS_PORT=19530
    MINIO_URI='http://minio:9000'

