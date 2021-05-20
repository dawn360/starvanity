from handler import on_event
import json
event = """
{
    "RequestType": "Update",
    "ResponseURL": "http://pre-signed-S3-url-for-response",
    "StackId": "arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid",
    "RequestId": "unique id for this update request",
    "ResourceType": "Custom::CF",
    "LogicalResourceId": "CustomCF",
    "PhysicalResourceId" : "9369faa6-5b6c-4013-97b9-fc366018c161",
    "ResourceProperties": {
        "ServiceToken": "arn:aws:lambda:us-east-1:678832181077:function:StarvanityStack-ContactFlowCustomResourceContactFl-BZjUHQ6nbbI4",
        "VanityFuncArn": "arn:aws:lambda:us-east-1:678832181077:function:StarvanityStack-generateVanityEA85C477-PpR4hQ2t87Iq",
        "ConnectInstanceId": "22b2ebf4-7b9b-4ac7-8db2-cd1756c5af70"
    },
    "OldResourceProperties" : {
        "ServiceToken": "arn:aws:lambda:us-east-1:678832181077:function:StarvanityStack-ContactFlowCustomResourceContactFl-BZjUHQ6nbbI4",
        "VanityFuncArn": "arn:aws:lambda:us-east-1:678832181077:function:connectTest",
        "ConnectInstanceId": "22b2ebf4-7b9b-4ac7-8db2-cd1756c5af70"
   }
    
}
"""

print(on_event(json.loads(event),None))
