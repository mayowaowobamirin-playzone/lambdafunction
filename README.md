AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Pushes VPC Flow Log metrics to Datadog.
Parameters:
  KMSAWSPrincipal:
    Type: "String"
    Description: "AWS Principal for KMS"
  # DatadogflowlogKeys:
  #   Type: "String"
  #   Description: "The id (final part of the key's ARN) of a KMS key used to encrypt and decrypt your Datadog API amd APP keys."
  # DatadogKeys:
  #   Default: "api_key":"<YOUR_API_KEY>", "app_key":"<YOUR_APP_KEY>" 
  #   Description: "Keys Provided by Datadog"
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
  DatadogKMS: 
    Type: AWS::KMS::Key
    Properties: 
     Description: "kmsEncryptedKeys"
     KeyPolicy: 
      Version: "2012-10-17"
      Id: "key-default-1"
      Statement: 
        - 
          Sid: "Allow administration of the key"
          Effect: "Allow"
          Principal: 
            AWS: !Ref "KMSAWSPrincipal"
          Action: 
            - "kms:*"
          Resource: "*"
  vpcflowlambdaddfunction:
    Type: "AWS::Serverless::Function"
    Properties:
      CodeUri: "s3://vpc-datadog-testing/lambda_function.zip" 
      Environment:
        Variables:
          kmsEncryptedKeys: 'YOUR_KEY'
      FunctionName: !Ref "lambdaFuntionName"
      Handler: lambda_function.lambda_handler
      KmsKeyArn: !GetAtt "DatadogKMS.Arn"
      MemorySize: 128
      Role: !GetAtt "lambdaIAMRole.Arn"
      Runtime: python2.7
      Timeout: 10
    Type: AWS::Serverless::Function
  
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
      ManagedPolicyArns:
        - "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
      Policies:
        - PolicyDocument:
            Statement:
              - Action: "kms:Decrypt"   
                Effect: "Allow"
                Resource: !GetAtt "DatadogKMS.Arn"   
          PolicyName: "lambda"         

  lambdaLogGroup:
    Type: "AWS::Logs::LogGroup"
    Properties:
      RetentionInDays: 90

  LambdaInvokePermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !GetAtt "vpcflowlambdaddfunction.Arn"
      Principal: "logs.us-east-1.amazonaws.com"
      Action: "lambda:InvokeFunction"
      SourceAccount: "341947552535"
      SourceArn: "arn:aws:logs:us-east-1:341947552535:log-group:cyber/vpcflow:*"
    

     
