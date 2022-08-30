import boto3
import os
import urllib.parse

rekog = boto3.client('rekognition', region_name='eu-west-1')

dynamodb = boto3.resource('dynamodb')
document_table = dynamodb.Table(os.environ["DocumentTable"])

s3 = boto3.resource('s3')

def start_rekognition_bytes(bucket, doc, eventTime, metadata):
    
    print("downloading file from S3: " + doc + " in " + bucket)
    s3.Bucket(bucket).download_file(doc, '/tmp/'+doc)

    #process using bytes
    with open("/tmp/"+doc, 'rb') as doc_file:
        doc_bytes = {'Bytes': doc_file.read()}
    print("Saved image, now going to Rekognition:")
    rekog_response = rekog.detect_faces(
        Image=doc_bytes, 
        Attributes=['ALL']
        )

    print("from Rekognition: " + str(rekog_response))
    
    try:
        if rekog_response['FaceDetails']:
            response = document_table.put_item(
                Item={
                    'dms_id': metadata,
                    'document': doc,
                    'datetime': eventTime,
                    'contains_face': True,
                    'face_confidence': round(rekog_response['FaceDetails'][0]['Confidence']),
                    'face_brightness': round(rekog_response['FaceDetails'][0]['Quality']['Brightness']),
                    'face_sharpness': round(rekog_response['FaceDetails'][0]['Quality']['Sharpness']),
                    'face_gender': rekog_response['FaceDetails'][0]['Gender']['Value'],
                    'face_eyeglasses': rekog_response['FaceDetails'][0]['Eyeglasses']['Value'],
                    'face_sunglasses': rekog_response['FaceDetails'][0]['Sunglasses']['Value'],
                    'face_smile': rekog_response['FaceDetails'][0]['Smile']['Value'],
                    'face_beard': rekog_response['FaceDetails'][0]['Beard']['Value'],
                    'face_mustache': rekog_response['FaceDetails'][0]['Mustache']['Value'],
                    'face_age_range': rekog_response['FaceDetails'][0]['AgeRange'],
                    #'face_emotions': rekog_response['FaceDetails'][0]['Emotions'][0],
                    }
                )
    except Exception as err:
            print("Exception: Rekognition to DDB")
            print (err)

def start_rekognition_s3object(bucket, doc, eventTime, metadata):
    
    print("Started Rekognition with file from S3: " + doc + " in " + bucket)
  
    #process using S3 object
    rekog_response = rekog.detect_faces(
        Image={
            'S3Object': 
            {
                'Bucket': bucket,
                'Name': doc
            }
        },
        Attributes=['ALL']
    )

    print("from Rekognition: " + str(rekog_response))
    
    try:
        if rekog_response['FaceDetails']:
            response = document_table.put_item(
                Item={
                    'dms_id': metadata,
                    'document': doc,
                    'datetime': eventTime,
                    'contains_face': True,
                    'face_confidence': round(rekog_response['FaceDetails'][0]['Confidence']),
                    'face_brightness': round(rekog_response['FaceDetails'][0]['Quality']['Brightness']),
                    'face_sharpness': round(rekog_response['FaceDetails'][0]['Quality']['Sharpness']),
                    'face_gender': rekog_response['FaceDetails'][0]['Gender']['Value'],
                    'face_eyeglasses': rekog_response['FaceDetails'][0]['Eyeglasses']['Value'],
                    'face_sunglasses': rekog_response['FaceDetails'][0]['Sunglasses']['Value'],
                    'face_smile': rekog_response['FaceDetails'][0]['Smile']['Value'],
                    'face_beard': rekog_response['FaceDetails'][0]['Beard']['Value'],
                    'face_mustache': rekog_response['FaceDetails'][0]['Mustache']['Value'],
                    'face_age_range': rekog_response['FaceDetails'][0]['AgeRange'],
                    #'face_emotions': rekog_response['FaceDetails'][0]['Emotions'][0],
                    }
                )
    except Exception as err:
            print("Exception: Rekognition to DDB")
            print (err)

  

def lambda_handler(event, context):

    print("Started Processing S3 Event")
    print(event)
    eventTime = event['Records'][0]['eventTime']
    bucket = event['Records'][0]['s3']['bucket']['name']
    doc = urllib.parse.unquote_plus(urllib.parse.unquote(event['Records'][0]['s3']['object']['key']))  #S3 event contains document name in URL encoding, needs to be decoded before sending to textract - https://github.com/aws-samples/amazon-textract-enhancer/issues/2
    print ("Document Name: " + doc)

    doc_metadata = s3.Object(bucket, doc)
    doc_metadata = str(doc_metadata.get()['Metadata']['dms-id'])
    print ("Metadata: " + doc_metadata)

    #Call Rekognition, passing the location of the file in S3. Only works in S3 and Rekognition are in the same region
    #start_rekognition_s3object(bucket, doc, eventTime, doc_metadata)

    #Call Rekognition, downloading and passing the file as a byte stream.
    start_rekognition_bytes(bucket, doc, eventTime, doc_metadata)
    print("Completed Processing from S3 to Rekognition to DDB")