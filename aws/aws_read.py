import boto3
import json
import os

AWS_ACCESS_KEY_ID = 'AKIAJONJ4JMC5ZSSNAAQ'
AWS_SECRET_ACCESS_KEY = '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'

bucket = AWS_ACCESS_KEY_ID.lower() + '-dump'

def file_read(filename, UPLOAD_FOLDER):
    fileName= os.path.join(UPLOAD_FOLDER, filename)

    client=boto3.client('rekognition','us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID,
         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    print('yolo bucket', bucket)
    response = client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})
    return response
    # print(json.dumps(response, indent=2))

    # print('Detected labels for ' + fileName)
    # for label in response['Labels']:
    #     print (label['Name'] + ' : ' + str(label['Confidence']))
