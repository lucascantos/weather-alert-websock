from src.services import s3
def clients_connected (client_id, action, channel):   
    action = action.upper() 
    try:
        client_data = s3.s3_download()
    except:
        client_data = {}

    channel_connections = client_data.getdefault(channel, [])

    if action == "ADD":
        print(f'Adding {client_id}')
        channel_connections.append(client_id)
    elif action == 'REMOVE':
        print(f'Removing {client_id}')
        channel_connections.remove(client_id)
    else:
        print("action must be 'add' or 'remove' ")
    s3.s3_upload(client_data)
