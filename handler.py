from src.functions.client_db import ClientDB
from src.functions.message import broadcast_event
from src.helpers.responses import response
from src.services.s3 import S3

def connection(event=None, context=None):
    '''
    Handler fo connections
    '''
    print(event)
    client_db = ClientDB()
    event_context = event['requestContext']
    client_id = event_context['connectionId']
    event_type = event_context['eventType']
    if event_type == 'CONNECT':
        channel = event_context['channel']
        client_db.add(client_id, channel)
    elif event_type == 'DISCONNECT':
        client_db.remove(client_id)
    else:
        return response['failure']
    client_db.save()
    return response['success']

def default(event=None, context=None):
    bucket = S3()
    client_list = bucket.load('clients.json')
    broadcast_event(event, client_list)
    return response['default']
 
def broadcast_data (event=None, context=None):
    '''
    Send message to all connected clients
    '''
    print(event)
    channel = ''
    client_db = ClientDB()
    channel_clients = client_db.channel_connected(channel)
    invalid_ids = broadcast_event(event, channel_clients)
    for iid in invalid_ids:
        client_db.remove(iid)
    client_db.save()
    return response['success']


