"""
Helper Function for getting json version of a contact flow
"""

#064dc65a-b8d1-4a88-900d-a9b0d6b5666c
import boto3
import logging as log
import json
# log.getLogger().setLevel(log.ERROR)
log.getLogger().setLevel(log.INFO)
client = boto3.client('connect')

try:
    response = client.describe_contact_flow(
        InstanceId='22b2ebf4-7b9b-4ac7-8db2-cd1756c5af70',
    ContactFlowId='064dc65a-b8d1-4a88-900d-a9b0d6b5666c'
    )
except Exception as ex:
    log.error(ex)
    raise ex

f = open("contactflow.json", "w")
f.write(response['ContactFlow']['Content'])
f.close()
