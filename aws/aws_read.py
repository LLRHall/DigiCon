import boto3
import json

AWS_ACCESS_KEY_ID = 'AKIAJONJ4JMC5ZSSNAAQ'
AWS_SECRET_ACCESS_KEY = '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'
TEST_FILE = 'test_2.jpg'

bucket = AWS_ACCESS_KEY_ID.lower() + '-dump'

if __name__ == "__main__":
    fileName= TEST_FILE
    
    client=boto3.client('rekognition','us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID,
         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    response = client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})
    print(json.dumps(response, indent=2))

    # print('Detected labels for ' + fileName)    
    # for label in response['Labels']:
    #     print (label['Name'] + ' : ' + str(label['Confidence']))