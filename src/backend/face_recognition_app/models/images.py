import boto3
from botocore.client import Config
from face_recognition_app import app


s3 = boto3.resource('s3',
                    endpoint_url=app.config['MINIO_URI'],
                    aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
                    aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')


class Images():

    def get_image(id):
        file_name=str(id).zfill(6)+'.jpg'
        image_path=app.config['IMAGES_LOCATION']+file_name
        with open(image_path, "rb") as image_file:
            data = image_file.read()
        return (file_name,data)

    def get_image_from_s3(id):
        file_name=str(id).zfill(6)+'.jpg'
        image_path='img_align_celeba/'+file_name
        # download the object 'piano.mp3' from the bucket 'songs' and save it to local FS as /tmp/classical.mp3
        # Get a full object.
        object = s3.Object('images', image_path)
        data = object.get()['Body'].read()  
        
        return (file_name,data)


