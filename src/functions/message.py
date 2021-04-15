
import json
import boto3

def broadcast_event (event, client_list):
    '''
    Send messages to all clients on list. Return list of invalid ids to be delt with
    :params event: Event to send
    :params client_list: Iterable of clients to send the event
    '''
    event_context = event['requestContext']
    sender = event_context['connectionId']
    print(event_context['routeKey'])
    if event_context['routeKey']=='$default':
        message = f"{sender}: {event['body']}"
    else:
        message = event['body']
    endpoint = f"https://{event_context['domainName']}/{event_context['stage']}/"

    session = boto3.session.Session()
    client = session.client(
        service_name='apigatewaymanagementapi',
        endpoint_url = endpoint
    )
    if not isinstance(client_list, list):
        client_list = [client_list]
    
    invalid_ids = []
    for client_id in client_list:
        if client_id != sender:
            try:
                client.post_to_connection(
                    Data=message, 
                    ConnectionId=client_id
                    )
            except:
                print(f'Invalid client_id! Disconeccting: {client_id}')
                invalid_ids.append(client_id)
    return invalid_ids
                
