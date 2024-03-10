#%%
import json
import pika

def message_handler(ch, method, properties, body):
    print(f"Received {body}") # Received b'0a0c11aba1a942228162cdeb726b4195'

def read_config():
    with open('config/rabbitmq_connection.json', 'r') as f:
        return json.load(f)
    
def connect_to_queue():
    rabbitmq_config = read_config()
    conenction = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_config["rabbitmq"]["host"]))
    channel = conenction.channel()
    channel.basic_consume(queue=rabbitmq_config["rabbitmq"]["queue"], on_message_callback=message_handler, auto_ack=True)
    return channel

## Get meesage as a subscriber
def start_getting_messages():
    channel = connect_to_queue()
    print("Waiting for messages")
    channel.start_consuming()

def get_messages_once():
    config = read_config()
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    queue = config["rabbitmq"]["queue"]
    
    method_frame, header_frame, body = channel.basic_get(queue, auto_ack=True)
    if method_frame:
        print(f"Received {body}")
        return body
    else:
        print("Queue is empty.")
        return None