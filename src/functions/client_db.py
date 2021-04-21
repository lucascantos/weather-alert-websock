from src.services.s3 import S3
import json
class ClientDB:
    def __init__(self):
        '''
        Handles client connections
        '''
        self.bucket = S3()
        self._filename = 'ws_users.json'
        try:
            self.client_data = bucket.load(self._filename)
        except:
            self.client_data = {}
    
    def add(self, client_id, channel):
        '''
        Adds client to connected list
        :params client_id: Id of client
        :params channel: channel name to be part of        
        '''
        print(f'Adding {client_id}')
        self.client_data[client_id] = channel

    def remove(self, client_id):
        '''
        Remove client from receiving list
        :params client_id: Id of client       
        '''
        print(f'Removing {client_id}')
        self.client_data.pop(client_id)
    
    def channel_connected(self, channel):
        '''
        Filter clients by channel
        :params channel: channel name to be filtered     
        '''
        return filter(lambda k,v: v==channel, self.client_data.items())

    def save(self):
        '''
        Save file to bucket
        '''
        data = json.dumps(self.client_data)
        self.bucket.upload(data, self._filename)
        
