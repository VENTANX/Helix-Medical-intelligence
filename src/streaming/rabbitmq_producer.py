import pika
import time
import json
import random
from faker import Faker

# Initialize Faker for generating synthetic data
fake = Faker()

def generate_synthetic_note():
    """
    Generates a random realistic clinical note.
    """
    patient_name = fake.name()
    date = fake.date_this_year().strftime("%m/%d/%Y")
    
    # List of common diseases and medications for synthesis
    conditions = ["hypertension", "type 2 diabetes", "asthma", "pneumonia", "atrial fibrillation"]
    medications = ["Lisinopril", "Metformin", "Albuterol", "Azithromycin", "Warfarin"]
    dosages = ["10 mg", "500 mg", "90 mcg", "250 mg", "5 mg"]
    
    condition = random.choice(conditions)
    medication = random.choice(medications)
    dosage = random.choice(dosages)
    
    # Templates for clinical notes
    templates = [
        f"Patient {patient_name} seen on {date}. Presents with symptoms consistent with {condition}. Prescribed {medication} {dosage} daily.",
        f"Dr. Smith evaluated {patient_name} on {date}. Diagnosis: {condition}. Plan: Start {medication} {dosage}.",
        f"Discharge summary for {patient_name}. Date: {date}. History of {condition}. Medications: {medication} {dosage} PO.",
        f"ID: {random.randint(10000, 99999)}. {patient_name} complains of worsening {condition}. increased {medication} to {dosage}."
    ]
    
    return random.choice(templates)

def main():
    """
    Main loop to publish messages to RabbitMQ.
    """
    connection = None
    channel = None
    
    # Retry logic for connection
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='clinical_notes_stream')
            print("Connected to RabbitMQ.")
            break
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not available, retrying in 5 seconds...")
            time.sleep(5)

    try:
        while True:
            note = generate_synthetic_note()
            message = {'note': note, 'timestamp': time.time()}
            
            channel.basic_publish(exchange='',
                                  routing_key='clinical_notes_stream',
                                  body=json.dumps(message))
            
            print(f" [x] Sent: {note[:50]}...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
