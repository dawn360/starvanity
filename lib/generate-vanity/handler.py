import vanitynumber
import boto3
import os
import logging as log
import json

log.getLogger().setLevel(log.INFO)
TABLE_NAME = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

NUM_TO_WORD_DICT = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
               '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}


def spell_out_phone_number(number):
    number = number.replace('-','')
    countryCode = NUM_TO_WORD_DICT[number[0]]
    areaCodeList = [NUM_TO_WORD_DICT[c] for c in number[1:4]]
    officeCodeList = []
    for c in number[4:7]:
        try:
            officeCodeList.append(NUM_TO_WORD_DICT[c])
        except:
            officeCodeList.append(c)
    subCodeList = []
    for c in number[7:]:
        try:
            subCodeList.append(NUM_TO_WORD_DICT[c])
        except:
            subCodeList.append(c)

    return '{} {}<break strength="weak"/>{}<break strength="weak"/>{}'.format(
        countryCode, ' '.join(areaCodeList), ' '.join(officeCodeList), ' '.join(subCodeList))


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
        spelled_nos = [spell_out_phone_number(num) for num in result[:3]]
        message = 'Here are your top vanity numbers <break strength="strong"/>{}<break strength="strong"/>'.format(
            '<break strength="strong"/>'.join(spelled_nos))
        
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
