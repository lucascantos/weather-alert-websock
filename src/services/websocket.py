
import json
import boto3

class Websocket:
    def __init__(self, event_context=None):
        if event_context:
            self.event_context = event_context
        else:
            self.event_context = {
                'connectionId': None,
                'domainName': 'localhost',
                'stage': 'local'
            }

        self.session = boto3.session.Session()
        self.endpoint = f"https://{self.event_context['domainName']}/{self.event_context['stage']}/"
        self.client = self.session.client(
            service_name='apigatewaymanagementapi',
            endpoint_url = self.endpoint
        )
        self.invalid_ids = []

    def send_message(self, client_id, message):
        try:
            self.client.post_to_connection(
                Data=message, 
                ConnectionId=client_id
                )
        except:
            print(f'Invalid client_id! Disconeccting: {client_id}')
            self.invalid_ids.append(client_id)
            return client_id

    def broadcast_message(self, client_list, message):
        '''
        Send messages to all clients on list, except the sender. Return list of invalid ids to be delt with
        :params event: Event to send
        :params client_list: Iterable of clients to send the event
        '''
        sender = self.event_context['connectionId']        
        if not isinstance(client_list, list):
            client_list = [client_list]        
        invalid_ids = []
        for client_id in client_list:
            if client_id != sender:
                try:
                    self.client.post_to_connection(
                        Data=message, 
                        ConnectionId=client_id
                        )
                except:
                    print(f'Invalid client_id! Disconeccting: {client_id}')
                    self.invalid_ids.append(client_id)
        return invalid_ids
                
