from handler import on_event
import json
event = """
{
    "RequestType": "Delete",
    "ServiceToken": "arn:aws:lambda:us-east-1:678832181077:function:StarvanityStack-ContactFlowCustomResourceContactFl-2JjZooe1NVM3",
    "ResponseURL": "https://cloudformation-custom-resource-response-useast1.s3.amazonaws.com/arn%3Aaws%3Acloudformation%3Aus-east-1%3A678832181077%3Astack/StarvanityStack/b3d60440-b903-11eb-a4a0-12c2b22562f7%7CContactFlowCustomResourceEA1343AC%7C045a021d-96f2-4e12-8e31-25c202685786?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210520T041633Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7199&X-Amz-Credential=AKIA6L7Q4OWTYMT6AIEY%2F20210520%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=2e9ac8f71c5f195594bfacb38594286586fd7349bcbc30e28fe45e9f826ad2f3",
    "StackId": "arn:aws:cloudformation:us-east-1:678832181077:stack/StarvanityStack/b3d60440-b903-11eb-a4a0-12c2b22562f7",
    "RequestId": "045a021d-96f2-4e12-8e31-25c202685786",
    "LogicalResourceId": "ContactFlowCustomResourceEA1343AC",
    "PhysicalResourceId": "b967e355-6114-4aa6-a8ed-dff9a8b6034f",
    "ResourceType": "AWS::CloudFormation::CustomResource",
    "ResourceProperties": {
        "ServiceToken": "arn:aws:lambda:us-east-1:678832181077:function:StarvanityStack-ContactFlowCustomResourceContactFl-2JjZooe1NVM3",
        "VanityFuncArn": "arn:aws:lambda:us-east-1:678832181077:function:StarvanityStack-generateVanityEA85C477-YiPE24skZ0Ii",
        "ConnectInstanceId": "arn:aws:connect:us-east-1:678832181077:instance/22b2ebf4-7b9b-4ac7-8db2-cd1756c5af70",
        "ConnectInstanceArn": "arn:aws:connect:us-east-1:678832181077:instance/22b2ebf4-7b9b-4ac7-8db2-cd1756c5af70"
    }
}
"""

print(on_event(json.loads(event),None))
