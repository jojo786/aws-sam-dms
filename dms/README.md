# dms

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

aws s3 cp id.jpg s3://dms-sam/id-pic.jpg --metadata '{"dms-id":"DMS-34533452"}'


aws dynamodb get-item --table-name DocumentOCR  --key '{"dms": {"S":"DMS-34533452"}, "document":{"S": "id-pic.jpg"} }' 

aws dynamodb query --table-name DocumentOCR --key-condition-expression "dms = :name" --expression-attribute-values  '{":name":{"S":"DMS-34533452"}}'

curl https://k54pftijm4.execute-api.us-east-1.amazonaws.com/Prod\?DMS-34533452 -H "x-api-key: xzcczxc"