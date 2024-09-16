# Sample Application Use DynamoDB

```
  DynamoDB:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: messages
      AttributeDefinitions:
        - AttributeName: uuid
          AttributeType: S
      KeySchema:
        - AttributeName: uuid
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST
```