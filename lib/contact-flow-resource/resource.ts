import * as logs from '@aws-cdk/aws-logs';
import * as cr from '@aws-cdk/custom-resources';
import lambda = require('@aws-cdk/aws-lambda');
import cdk = require('@aws-cdk/core');
import * as iam from '@aws-cdk/aws-iam';


import fs = require('fs');
import { Tags } from '@aws-cdk/core';

export interface ContactFlowCustomResourceProps {
    VanityFuncArn: string;
    ConnectInstanceId: string;
    ConnectInstanceArn: string;
    ContactFlowName: string;
}

export class ContactFlowCustomResource extends cdk.Construct {
    public readonly response: string;

    constructor(scope: cdk.Construct, id: string, props: ContactFlowCustomResourceProps) {
        super(scope, id);

        const onEvent = new lambda.Function(this, 'ContactFlowCustomResourceHandler', {
            code: new lambda.AssetCode('lib/contact-flow-resource'),
            handler: 'handler.on_event',
            description: 'Connect Contact Flow Custom Resource Handler',
            timeout: cdk.Duration.seconds(300),
            runtime: lambda.Runtime.PYTHON_3_6,
            initialPolicy: [new iam.PolicyStatement({
                effect: iam.Effect.ALLOW,
                resources: [props.ConnectInstanceArn,`${props.ConnectInstanceArn}/contact-flow/*`],
                actions: ['connect:AssociateLambdaFunction', 'connect:UpdateContactFlowContent',
                    'connect:CreateContactFlow', 'connect:TagResource','connect:UpdateContactFlowName']
            })],
            

        });

        Tags.of(onEvent).add('app', 'starvanity');

        //we need to grant this lambda permissions to attach vanity function to connect instance
        onEvent.addToRolePolicy(new iam.PolicyStatement({
            effect: iam.Effect.ALLOW,
            resources: [props.VanityFuncArn],
            actions: ['lambda:AddPermission']
        }));

        const provider = new cr.Provider(this, 'ContactFlowCustomResourceProvider', {
            onEventHandler: onEvent,
        });

        const resource = new cdk.CustomResource(this, 'ContactFlowCustomResource', { serviceToken: provider.serviceToken, properties: props });

        this.response = resource.getAtt('Response').toString();
    }
}

