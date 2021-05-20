import vanitynumber
import boto3
import os
import logging as log
import json

log.getLogger().setLevel(log.INFO)
TABLE_NAME = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    log.debug(event)
    contactRaw = event['Details']['ContactData']['CustomerEndpoint']['Address']
    contactId = event['Details']['ContactData']['ContactId']
    #Format Phone Number
    contactAddress = '{}-{}-{}-{}'.format(contactRaw[1:2],contactRaw[2:5],contactRaw[5:8],contactRaw[8:])
    log.info(contactAddress)
    result = vanitynumber.all_wordifications(contactAddress)
    message = "Sorry, we couldn't a vanity number for your phone number. Please try another Number"
    if result:
        message = 'Here are your top vanity numbers <break strength="strong"/><say-as interpret-as="telephone">{}</say-as><break strength="strong"/>'.format(
            '</<say-as><say-as interpret-as="telephone">'.join(result[:3]))
        item = {
            'contactId': contactId,
            'contactAddress': contactAddress,
            'options': json.dumps(result[:5]),
            'Message': message
        }
        log.info(message)

        # save to dynamo
        try:
            table.put_item(Item=item)
        except Exception as ex:
            log.error(ex)

        return item

    log.info(message)
    return {'Message': message}
