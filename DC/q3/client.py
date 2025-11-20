
import requests
import time

SERVER_URL = 'http://127.0.0.1:5000'

# Create a new API key
def create_key():
    resp = requests.post(f'{SERVER_URL}/create_key')
    print('Create Key:', resp.json())
    return resp.json().get('key')

# Retrieve an available key
def get_key():
    resp = requests.get(f'{SERVER_URL}/get_key')
    print('Get Key:', resp.json())
    return resp.json().get('key')

# Block (unblock) a key
def block_key(key):
    resp = requests.post(f'{SERVER_URL}/block_key', json={'key': key})
    print('Block Key:', resp.json())

# Keep alive a key

def keep_alive(key):
    resp = requests.post(f'{SERVER_URL}/keep_alive', json={'key': key})
    try:
        data = resp.json()
    except Exception:
        data = {'error': 'Invalid response'}
    print('Keep Alive:', data)
    return data

if __name__ == '__main__':
    print('API Key Manager ---')
    while True:
        # Try to get a key (blocking if necessary)
        key = get_key()
        if not key:
            print('No key available, creating one...')
            create_key()
            time.sleep(1)
            continue
        print('Got key:', key)
        while True:
            result = keep_alive(key)
            if result.get('error'):
                print('Key blocked or unavailable, waiting 2s to retry...')
                time.sleep(2)
                break  # Go back to get_key()
            print('Key kept alive. Sleeping 4s...')
            time.sleep(4)
