from src.services.s3 import S3
import json
class UserDB:
    def __init__(self):
        '''
        Handles user connections
        '''
        self.bucket = S3()
        self._filename = 'ws_users.json'
        try:
            self.user_data = self.bucket.load(self._filename)
        except:
            print('File not found')
            self.user_data = {}
    
    def add(self, user_id, channel):
        '''
        Adds user to connected list
        :params user_id: Id of user
        :params channel: channel name to be part of        
        '''
        print(f'Adding {user_id}')
        self.user_data[user_id] = channel
        self.save()

    def remove(self, user_id):
        '''
        Remove user from receiving list
        :params user_id: Id of user       
        '''
        print(f'Removing {user_id}')
        try:
            self.user_data.pop(user_id)
            self.save()
        except KeyError:
            pass

    def batch_remove(self, user_ids):
        '''
        Remove user from receiving list
        :params user_id: Id of user       
        '''
        print(f'Removing {user_ids}')
        for uid in user_ids:
            try:
                self.user_data.pop(uid)
            except KeyError:
                pass
        self.save()
    
    def channel_connected(self, channel):
        '''
        Filter users by channel
        :params channel: channel name to be filtered     
        '''
        return filter(lambda x: x[1]==channel, self.user_data.items())
        
    def clear(self):
        groupless = self.channel_connected(None)
        self.batch_remove([k for k,v in groupless])



    def save(self):
        '''
        Save file to bucket
        '''
        data = json.dumps(self.user_data)
        self.bucket.upload(data, self._filename)
        
