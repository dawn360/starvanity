const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = process.env.TABLE_NAME || '';

export const handler = async (event: any = {}): Promise<any> => {
  console.log(JSON.stringify(event, null, 2))

  /**
    with more time we can check for scenarios where the contactPhoneNo is "Private"
    in such a case we can route the failure to a contact flow block which will ask the client 
    for his phone number
   */
  // assuming we always have the phone number
  var contactPhoneNo = event['Details']['ContactData']['CustomerEndpoint']['Address'];

  let item = {
    recId: contactPhoneNo,
    option1: contactPhoneNo,
    option2: contactPhoneNo,
    option3: contactPhoneNo,
  }
  const params = {
    TableName: TABLE_NAME,
    Item: item
  };

  try {
    await db.put(params).promise();
    return item;
  } catch (dbError) {
    console.log(dbError);
  }
};