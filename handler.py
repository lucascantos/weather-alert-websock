from src.functions.client_db import ClientDB
from src.helpers.responses import response
from src.services.s3 import S3
from src.services.websocket import Websocket
import json

def connection(event=None, context=None):
    '''
    Handler fo connections
    '''
    print('HEllo', event)
    event_context = event['requestContext']
    client_id = event_context['connectionId']
    client_db = ClientDB()
    ws = Websocket(event_context)
    event_type = event_context['eventType']
    if event_type == 'CONNECT':
        client_db.add(client_id, None)
    elif event_type == 'DISCONNECT':
        client_db.remove(client_id)
    else:
        return response['failure']
    # client_db.save()
    
    ws.send_message(client_id, f'Use the route "subscribe" to join a channel.')
    ws.send_message(client_id, f'Channels available: ["lightnings","alerts"]')


def default(event=None, context=None):
    print('Hello', event)
    event_context = event['requestContext']
    client_id = event_context['connectionId']
    ws = Websocket(event_context)
    ws.send_message(client_id, f'Use the route "subscribe" to join a channel.')
    ws.send_message(client_id, f'Channels available: ["lightnings","alerts"]')

def subscribe(event=None, context=None):
    print(event)
    event_context = event['requestContext']
    client_id = event_context['connectionId']
    ws = Websocket(event_context)
    client_db = ClientDB()

    body = json.loads(event['body'])
    channel = body.get('channel')

    client_db.add(client_id, channel)
    ws.send_message(client_id, f'Welcome to the channel: {channel}')

def broadcast_data (event=None, context=None):
    '''
    Send message to all connected clients
    '''
    print(event)
    ws = Websocket(event)
    client_db = ClientDB()

    message = json.loads(event['Records'][0]['Sns']['Message'])    
    channel = event['Records'][0]['Sns']['Subject']
    channel_clients = client_db.channel_connected(channel)

    invalid_ids = ws.broadcast_message(channel_clients, message)
    for iid in invalid_ids:
        client_db.remove(iid)
    client_db.save()


