# dms

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. The application is a starting point to build a serverless document management system (DMS). It allows you to upload files to Amazon S3, which then invokes a Lambda that does various analysis of the document, and stores the results of the analysis on Amazon DynamoDB. You can then query the results via an API exposed using Amazon API Gateway.
The analysis can include:
- doing facial analysis on pictures using Amazon Rekognition
- extracting text using Amazon Textract
- and much more

The idea is that you have an existing application where your users need to upload documents, e.g. ID or proof of residence documents. Its in-efficient and expensive to store and manage these documents locally in your application file system or relational database, and requires manual effort to verify their authenticity. Using this sample DMS application on AWS, you can store these documents safely and cheaply in AWS, and automate the verification and extraction of data.

When uploading the document to S3, you can specifiy some metadata, which allows to link to to an ID in your application:
`aws s3 cp id.jpg s3://dms-sam/id-pic.jpg --metadata '{"dms-id":"DMS-34533452"}'`

Then query the results of the analysis via an API call, which is secured using an API Key:
`curl https://k54pftijm4.execute-api.us-east-1.amazonaws.com/Prod\?DMS-34533452 -H "x-api-key: xzcczxc"`


Or you can directly query DynamoDB:

`aws dynamodb get-item --table-name DocumentOCR  --key '{"dms": {"S":"DMS-34533452"}, "document":{"S": "id-pic.jpg"} }' `

`aws dynamodb query --table-name DocumentOCR --key-condition-expression "dms = :name" --expression-attribute-values  '{":name":{"S":"DMS-34533452"}}'`

# How to build and deploy
- Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html), and  [configure it](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)
- Install [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Run `sam build`
- Run `sam deploy --guided` the first time, which will guide to choose a stack name, region, etc. These options will be saved, so in subsequent runs after making changes, you only need to run `sam build && sam deploy`

