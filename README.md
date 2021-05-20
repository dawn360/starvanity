# Starvanity project!

###Deployment
#####Prerequisites
1. AWS CDK installed
2. npm installed
3. AWS account with programmatic access

#### AWS credentials
before you deploy you need to set configure the aws_access_key and secret in your environment. Either by a ~/.aws file or profile or environment variables
Eg.

    export AWS_ACCESS_KEY_ID=XXX
    export AWS_SECRET_ACCESS_KEY=XXX
    export AWS_DEFAULT_REGION=XXXX
## Deploy
Clone or download this github project

Set `connectInstanceArn` and `contactFlowName` environment variables 

    export connectInstanceArn=<my-connect-instance-arn>
    export contactFlowName=<my-contact-flow-name> # optional. default is StarvanityContactFlow

Run `make deploy` at the root of the project

This will install the npm packages, build, bootstrap and deploy / redeploy the starvanity Stack to your AWS Account.

## The Component Structure
- lambda at `lib/contact-flow-resource/handler.py` makes calls to the connect instance to attach and create a contact flow
- lambda at `lib/generate-vanity/handler.py` creates and saves vanity numbers to dynamo



## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
