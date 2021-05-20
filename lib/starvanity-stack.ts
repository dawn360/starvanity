import * as cdk from '@aws-cdk/core';
import dynamodb = require('@aws-cdk/aws-dynamodb');
import lambda = require('@aws-cdk/aws-lambda');
import { ContactFlowCustomResource } from './contact-flow-resource/resource';
import { CfnParameter, Tags } from '@aws-cdk/core';
export class StarvanityStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //CDK params
    const connectInstanceArn = new CfnParameter(this, "connectInstanceArn", {
      type: "String",
      description: "Arn of connect instance where the Vanity Contact Flow will be installed"
    });
    const contactFlowName = new CfnParameter(this, "contactFlowName", {
      type: "String",
      description: "Contact Flow Name"
    });

    // DB
    const dynamoTable = new dynamodb.Table(this, 'vanityContactLog', {
      partitionKey: {
        name: 'contactId',
        type: dynamodb.AttributeType.STRING
      },
      tableName: 'vanityContactLog',
      // DESTROY, cdk destroy will delete the table (even if it has data in it)
      // NOT recommended for production code but for this project we need to be able to clean up
      removalPolicy: cdk.RemovalPolicy.DESTROY, 
    });
    Tags.of(dynamoTable).add('app', 'starvanity');

    // Contact Flow Lambda
    const generateVanity = new lambda.Function(this, 'generateVanity', {
      code: new lambda.AssetCode('lib/generate-vanity'),
      handler: 'handler.handler',
      description: 'Return best 5 vanity numbers given a caller number in a DynamoDB table. Also invoked by connect contact flow',
      timeout: cdk.Duration.seconds(10),
      runtime: lambda.Runtime.PYTHON_3_6,
      environment: {
        TABLE_NAME: dynamoTable.tableName
      }
    });

    Tags.of(generateVanity).add('app', 'starvanity');
    // lambda function permissions
    dynamoTable.grantReadWriteData(generateVanity);

    
    // Contact Flow Custom CF Resource

    // arn:aws:connect:us-east-1:678832181077:instance/22b2ebf4-7b9b-4ac7-8db2-cd1756c5af70
    let connectInstanceId = connectInstanceArn.valueAsString.split('/').pop(); //get id from arn
    const contactFlowResource = new ContactFlowCustomResource(this, 'ContactFlowCustomResource', {
      VanityFuncArn: generateVanity.functionArn,
      ConnectInstanceId: connectInstanceId!,
      ConnectInstanceArn: connectInstanceArn.valueAsString,
      ContactFlowName: contactFlowName.valueAsString
    });
    Tags.of(contactFlowResource).add('app', 'starvanity');

    // Publish the custom resource output
    new cdk.CfnOutput(this, 'ResponseMessage', {
      description: 'The message that came back from ContactFlowCustomResource',
      value: contactFlowResource.response
    });

  }
}
