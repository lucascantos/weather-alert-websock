from src.functions.user_db import UserDB
from src.helpers.responses import response
from src.services.s3 import S3
from src.services.websocket import Websocket
import json

def connection(event=None, context=None):
    '''
    Handler fo connections to WS
    '''
    print('Hello', event)
    event_context = event['requestContext']
    user_id = event_context['connectionId']
    user_db = UserDB()
    event_type = event_context['eventType']
    if event_type == 'CONNECT':
        user_db.add(user_id, None)
    elif event_type == 'DISCONNECT':
        user_db.remove(user_id)
        return response['success']
    else:
        return response['failure']
    user_db.save()
        
    return response['success']

def default(event=None, context=None):
    '''
    WS default route. Send instruction to subscribe to a channel
    '''
    print('Hello', event)
    event_context = event['requestContext']
    user_id = event_context['connectionId']
    ws = Websocket(event_context)
    ws.send_message(user_id, f'Use the route "subscribe" to join a channel.')
    ws.send_message(user_id, f'Channels available: ["lightnings","alerts"]')
    return response['default']

def subscribe(event=None, context=None):
    '''
    WS route for subscription to channel
    '''
    print(event)
    event_context = event['requestContext']
    user_id = event_context['connectionId']
    ws = Websocket(event_context)
    user_db = UserDB()

    body = json.loads(event['body'])
    channel = body.get('channel')

    user_db.add(user_id, channel)
    ws.send_message(user_id, f'Welcome to the channel: {channel}')
    user_db.clear()
    return response['success']

def broadcast_data (event=None, context=None):
    '''
    Send message to all connected users
    '''
    print(event)
    ws = Websocket()
    user_db = UserDB()

    message = event['Records'][0]['Sns']['Message']  
    channel = event['Records'][0]['Sns']['Subject']
    channel_users = user_db.channel_connected(channel)

    invalid_ids = ws.broadcast_message(channel_users, message)
    if invalid_ids:
        user_db.batch_remove(invalid_ids)
    return response['success']


