from src.services.s3 import S3
import json
class ClientDB:
    def __init__(self):
        self.bucket = S3()
        self._filename = 'clients_connected.json'
        try:
            self.client_data = bucket.load(self._filename)
        except:
            self.client_data = {}
    
    def add(self, client_id, channel):
        '''
        Adds client to connected list
        :params add
        '''
        print(f'Adding {client_id}')
        self.client_data[client_id] = channel

    def remove(self, client_id):
        print(f'Removing {client_id}')
        self.client_data.pop(client_id)
    
    def channel_connected(self, channel):
        return filter(lambda k,v: v==channel, self.client_data.items())

    def save(self):
        data = json.dumps(self.client_data)
        self.bucket.upload(data, self._filename)
        
