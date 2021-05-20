import boto3
import logging as log
import json
import time
log.getLogger().setLevel(log.INFO)
client = boto3.client('connect')

def on_event(event, context):
    log.debug(event)
    request_type = event['RequestType']
    if request_type == 'Create': return on_create(event)
    if request_type == 'Update': return on_update(event)
    if request_type == 'Delete': return on_delete(event)
    raise Exception("Invalid request type: %s" % request_type)


def attach_lambda(funcArn, connectInstanceId):
    # attach vanity function for connect instance
    try:
        client.associate_lambda_function(InstanceId=connectInstanceId,
                                        FunctionArn=funcArn)
    except Exception as ex:
        log.error(ex)
        raise ex


def on_create(event):
    props = event["ResourceProperties"]
    
    # attach vanity function for connect instance
    attach_lambda(props['VanityFuncArn'], props['ConnectInstanceId'])
    # create contact flow
    try:
        with open('contact-flow-template.json') as f:
            # replace placeholder with arn
            contactFlowContent = f.read() % props['VanityFuncArn']
            log.debug(contactFlowContent)
    
            createCFResp = client.create_contact_flow(
            InstanceId=props['ConnectInstanceId'],
            Name=props['ContactFlowName'],
            Type='CONTACT_FLOW',
            Description='Reads out top 3 vanity numbers from a contacts phone number',
            Content=contactFlowContent,
            Tags={'app': 'starvanity'}
            )
    except Exception as ex:
        log.error(ex)
        raise ex

    log.debug(createCFResp)
    attributes = {
        'Response': 'Created Contact Flow',
        'ContactFlowId': createCFResp['ContactFlowId']
    }
    log.info(attributes)
    return {'Data': attributes, 'PhysicalResourceId': createCFResp['ContactFlowId']}

def on_update(event):
    physical_id = event["PhysicalResourceId"] #contact flow ID
    props = event["ResourceProperties"]
    old_props = event['OldResourceProperties']
    log.debug("update resource %s" % physical_id)

    # attaching same function multiple times is fine with connect
    attach_lambda(props['VanityFuncArn'], props['ConnectInstanceId'])

    # if OldResourceProperties VanityFuncArn is different then disassociate
    # so we don't have limbo functions attached to the connect instance
    try:
        if old_props['VanityFuncArn'] != props['VanityFuncArn']:
            client.disassociate_lambda_function(InstanceId=props['ConnectInstanceId'],
                                                FunctionArn=old_props['VanityFuncArn'])
    except Exception as ex:
        log.error(ex)

    # update contact flow content with PhysicalResourceId
    try:
        with open('contact-flow-template.json') as f:
            # replace placeholder with arn
            contactFlowContent = f.read() % props['VanityFuncArn']
            log.debug(contactFlowContent)

            client.update_contact_flow_content(
                InstanceId=props['ConnectInstanceId'],
                ContactFlowId=physical_id,
                Content=contactFlowContent
            )
    except Exception as ex:
        log.error(ex)
        raise ex
    

    attributes = {
        'Response': 'Updated Contact Flow Content',
        'ContactFlowId': physical_id,
    }
    log.info(attributes)
    return { 'Data': attributes }

def on_delete(event):
    physical_id = event["PhysicalResourceId"]
    props = event["ResourceProperties"]
    log.debug("delete resource %s" % physical_id)

    # delete contact flow and detach lambda from instance
    try:
        client.disassociate_lambda_function(InstanceId=props['ConnectInstanceId'],
                                            FunctionArn=props['VanityFuncArn'])
    except Exception as ex:
        log.error(ex)

    # Rename Function XDeletedStarVanity<last 5digits of VanityFuncArn reversed>
    new_name = 'xDeletedStarVanity_{}'.format(props['VanityFuncArn'][-10:]) #unique name
    log.info(new_name)

    try:
        client.update_contact_flow_name(
            InstanceId=props['ConnectInstanceId'],
            ContactFlowId=physical_id,
            Name=new_name,
            Description='Deleted StartVanity ContactFlow'
        )
    except:
        pass
    attributes = {
        'Response': 'Contact Flow Renamed to {}'.format(new_name),
        'ContactFlowId': physical_id
    }
    log.info(attributes)
    return { 'Data': attributes }
