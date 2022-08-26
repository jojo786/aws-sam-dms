# dms

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. The application is a starting point to build a serverless document management system. It allows you to upload files to Amazon S3, which then invokes a Lambda that does various analysis of the document, and stores the results of the analysis on Amazon DynamoDB. You cna then query the results via an API exposed using Amazon API Gateway.
The analysis can include:
- doing facial analysis on pictures using Amazon Rekognition
- extracting text using Amazon Textract
- and much more

When uploading the document to S3, you can specifiy some metadata, which allows to link to to an ID in your application:
`aws s3 cp id.jpg s3://dms-sam/id-pic.jpg --metadata '{"dms-id":"DMS-34533452"}'`

Then query the results of the analysis via an API call, which is secured using an API Key:
`curl https://k54pftijm4.execute-api.us-east-1.amazonaws.com/Prod\?DMS-34533452 -H "x-api-key: xzcczxc"`


Or you can directly query DynamoDB:

`aws dynamodb get-item --table-name DocumentOCR  --key '{"dms": {"S":"DMS-34533452"}, "document":{"S": "id-pic.jpg"} }' `

`aws dynamodb query --table-name DocumentOCR --key-condition-expression "dms = :name" --expression-attribute-values  '{":name":{"S":"DMS-34533452"}}'`

