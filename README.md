# lambdafunction
AWSTemplateFormatVersion: '2010-09-09'
Parameters:
  # KMSKeyId:
  #   Type: "String"
  #   Description: The id (final part of the key's ARN) of a KMS key used to encrypt and decrypt your Datadog API amd APP keys.
  DatadogKeys:
    Type: "String"
    Description: "The id (final part of the key's ARN) of a KMS key used to encrypt and decrypt your Datadog API amd APP keys."
  Lambdas3Key:
    Type: "String"
    Default: "funtion.zip"
  Lambdas3Bucket:
    Type: "String"
    Description: "The name of the s3bucket that contains the source code of the Lambda"
  lambdaFuntionName:
    Type: "String"
    Default: "VPCFlowlogs-funtion" 
Resources:
  DatadogKeys: 
    Type: AWS::KMS::Key
    Properties: 
    Description: "kmsEncryptedKeys"
    KeyPolicy: 
      Version: "2012-10-17"
      Id: "Datadog-FlowlogKeys"
      Statement: 
        - 
          Effect: "Allow"
          Principal: 
            AWS: !Ref ""
          Action: 
            - "kms:Create*"
            - "kms:Describe*"
            - "kms:Enable*"
            - "kms:List*"
            - "kms:Put*"
            - "kms:Update*"
            - "kms:Get*"
          Resource: "*"
  vpcflowlambdaddfunction:
    Type: AWS::Serverless::Function
    Properties:
      Code: 
       S3Bucket: !Ref "Lambdas3Bucket"
       S3Key:    !Ref "Lambdas3Key"
       Handler: "index.handler"
        
      Environment:
        Environment
      FunctionName: !Ref "lambdaFuntionName"
      Handler: lambda_funtion.lambda_handler
      KmsKeyArn: 
        !Sub
         - 'arn:aws:logs:${AWS::Region}:${AWS::AccountId}:key/${keyId}'
         - {keyId: !Ref Datadog-FlowlogKeys}
      MemorySize: 128
      Role: !GetAtt "lambdaIAMRole.Arn"
      Runtime: python2.7
      Timeout: 10
  
  lambdaIAMRole:
    Type: "AWS::IAM::Role"
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Action:
              - "sts:AssumeRole"
            Effect: "Allow"
            Principal:
              Service:
                - "lambda.amazonaws.com"
      Policies:
        - PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Action:
                  - "*"
                Effect: "Allow"
                Resource:
                  - !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/${lambdaFunctionName}:*"
          PolicyName: "lambda"
  
    

     
