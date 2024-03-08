import json

def read_config():
    with open('../config/rabbitmq_connection.json', 'r') as f:
        return json.load(f)

def connect_to_queue():
    