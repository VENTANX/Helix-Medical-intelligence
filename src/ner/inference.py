import sys
import os
import time
import json
import pika

# Add src to python path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.deidentification.phi_removal import PHIRemover
from src.ner.clinicalbert import NERModel

PROCESSED_DATA_FILE = os.path.join(os.path.dirname(__file__), '../../data/processed_notes.jsonl')

def callback(ch, method, properties, body, model, phi_remover):
    """
    Callback function to process incoming messages.
    """
    message = json.loads(body)
    raw_text = message['note']
    
    print(f" [x] Received: {raw_text[:50]}...")
    
    # 1. De-identification
    cleaned_text = phi_remover.deidentify(raw_text)
    
    # 2. NER Inference
    entities = model.extract_entities(cleaned_text)
    
    # 3. Store Result (Simulating a database or processed queue)
    result = {
        "timestamp": message['timestamp'],
        "original_text_masked": cleaned_text, # Don't store PHI even in logs if avoiding it
        "entities": entities
    }
    
    # Append to a JSONL file for the dashboard to read
    with open(PROCESSED_DATA_FILE, 'a') as f:
        f.write(json.dumps(result) + '\n')
    
    print(f" [✓] Processed and saved.")

def main():
    print("Loading NER Model... (this may take a moment)")
    ner_model = NERModel()
    phi_remover = PHIRemover()
    print("Model loaded. Connecting to Queue...")

    connection = None
    channel = None

    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='clinical_notes_stream')
            print(" [*] Waiting for messages. To exit press CTRL+C")
            break
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not available, retrying in 5 seconds...")
            time.sleep(5)

    # Use a lambda or partial to pass the model to the callback
    channel.basic_consume(queue='clinical_notes_stream',
                          on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties, body, ner_model, phi_remover),
                          auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping inference worker...")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
