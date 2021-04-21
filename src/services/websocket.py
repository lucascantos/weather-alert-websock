
import json
import boto3

class Websocket:
    def __init__(self, event_context=None):
        if event_context:
            self.event_context = event_context
        else:
            self.event_context = {
                'connectionId': None,
                'domainName': 'z8ltbocqnl',
                'stage': 'prod'
            }

        self.session = boto3.session.Session()
        self.endpoint = f"https://{self.event_context['domainName']}/{self.event_context['stage']}/"
        self.client = self.session.client(
            service_name='apigatewaymanagementapi',
            endpoint_url = self.endpoint
        )
        self.invalid_ids = []

    def send_message(self, user_id, message):
        try:
            self.client.post_to_connection(
                Data=message, 
                ConnectionId=user_id
                )
        except:
            print(f'Invalid user! Disconeccting: {user_id}')
            self.invalid_ids.append(user_id)
            return user_id

    def broadcast_message(self, user_list, message):
        '''
        Send messages to all users on list, except the sender. Return list of invalid ids to be delt with
        :params event: Event to send
        :params user_list: Iterable of users to send the event
        '''
        sender = self.event_context['connectionId']              
        invalid_ids = []
        for user_id in user_list:
            print(user_id)
            if user_id != sender:
                try:
                    self.user.post_to_connection(
                        Data=message, 
                        ConnectionId=user_id[0]
                        )
                except:
                    print(f'Invalid user_id! Disconeccting: {user_id}')
                    self.invalid_ids.append(user_id)
        return invalid_ids
                
