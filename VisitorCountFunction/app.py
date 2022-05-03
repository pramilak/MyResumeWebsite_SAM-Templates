import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
TableName_EV = os.environ['DynamoDBTableName']
TableName = dynamodb.Table(TableName_EV)

def lambda_handler(event, context):

    print('Lambda Handler Begins Here')

    #Get items having "Label=VISITOR_COUNTER"
    try:
        response = TableName.query(KeyConditionExpression=Key('Label').eq('VISITOR_COUNTER'))
    except Exception as E:
        print('Sorry. Something went wrong, unable to Query from DB')
        print(E)
        err_resp = {"body": "Sorry. Something went wrong"}
        return err_resp

    #print(response["Items"])

    #When first Request is made
    if len(response["Items"]) == 0:
        try:
            resp1 = TableName.put_item(Item={'Label': "VISITOR_COUNTER",'Counter': "1"})

            return {
                    "statusCode": 200,
                    "headers": {
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*',
                        'Content-Type': 'application/json'
                    },                    
                    "body": json.dumps(
                    {
                        "VisitorCount": 1
                    }
                    )
            }

        except Exception as E:
            print('Sorry. Something went wrong, unable to write first item into DB')
            print(E)
            err_resp = {"body": "Sorry. Something went wrong"}
            return err_resp
    else:
        #Second subsequent requests
        try:
            resp2 = TableName.get_item(Key={'Label': "VISITOR_COUNTER"})
        except Exception as E:
            print('Sorry. Something went wrong, unable to read item from DB')
            print(E)  
            err_resp = {"body": "Sorry. Something went wrong"}
            return err_resp

    
        key_list = list(resp2['Item'].keys())
        val_list = list(resp2['Item'].values())

        position = key_list.index('Counter')
        #print(val_list[position])

        inter_count = int(val_list[position]) + 1
        #print(inter_count)

        try:
            resp3 = TableName.put_item(Item={'Label': "VISITOR_COUNTER", 'Counter':inter_count})
        except Exception as E:
            print('Sorry. Something went wrong, unable to write item into DB')
            print(E)  
            err_resp = {"body": "Sorry. Something went wrong"}
            return err_resp

    
        print('Lambda Handler Ends')
        
        return {
                "statusCode": 200,
                "headers": {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*',
                    'Content-Type': 'application/json'
                },                    
                "body": json.dumps(
                {
                    "VisitorCount": inter_count
                }
                )
            }