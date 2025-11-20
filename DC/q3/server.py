import threading
import time
import uuid
from flask import Flask, jsonify, request


app = Flask(__name__)
api_keys = {}
lock = threading.Lock()


KEY_LIFETIME = 5 
BLOCK_TIMEOUT = 2 

def cleanup_keys():
    while True:
        now = time.time()
        with lock:
            keys_to_delete = []
            for key, data in api_keys.items():
                if now-data['last_alive']>KEY_LIFETIME:
                    keys_to_delete.append(key)
                    continue
                if data['status']=='blocked' and data['blocked_time'] is not None:
                    if data['blocked_time']>BLOCK_TIMEOUT:
                        data['status']='available'
                        data['blocked_time']=None
                        
            for key in keys_to_delete:
                del api_keys[key]
                
        time.sleep(1)
        
        
@app.route('/create_key', methods=['POST'])
def create_key():
    key = str(uuid.uuid4())
    with lock:
        api_keys[key] = {'status': 'available', 'last_alive': time.time(), 'blocked_time': None}
    return jsonify({'key': key}), 201


@app.route('/get_key', methods=['GET'])
def get_key():
    with lock:
        for key, data in api_keys.items():
            if data['status']=='available':
                data['status']='blocked'
                data['blocked_time']=time.time()
                return jsonify({'key': key}), 201
    return jsonify({'error':'No free keys'}), 404

    
@app.route('/free_key', methods=['POST'])
def free_key():
    key = request.json.get('key')
    with lock:
        if key in api_keys and api_keys[key]['status']=='blocked':
            api_keys[key]['status']='available'
            api_keys[key]['blocked_time']=None
            return jsonify({'response': 'key freed'}), 200
    return jsonify({'error': 'key not found'}), 400

@app.route('/keep_alive', methods=['POST'])
def keep_alive():
    key = request.json.get('key')
    with lock:
        if key in api_keys:
            api_keys[key]['last_alive']= time.time()
        return jsonify({'response': 'Key kept alive'}),200
    return jsonify({'error': 'key not found'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)