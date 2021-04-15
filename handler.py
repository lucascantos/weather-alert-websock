from src.helpers.client_db import clients_connected
from src.helpers.message import send, response
from src.helpers.s3 import s3_download

def connection(event=None, context=None):
    '''
    Handler fo connections
    '''
    print(event)
    event_context = event['requestContext']
    if event_context['eventType'] == 'CONNECT':
        clients_connected(event_context['connectionId'], 'add')
        return response['success']
    elif event_context['eventType'] == 'DISCONNECT':
        clients_connected(event_context['connectionId'], 'remove')
        return response['success']
    
def default(event=None, context=None):
    client_list = s3_download()['connected']
    send(event, client_list)
    return response['default']
 
def broadcast_data (event=None, context=None):
    '''
    Send message to all connected clients
    '''
    print(event)
    client_list = s3_download()['connected']
    send(event, client_list)
    return response['success']


