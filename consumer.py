import pika
import json 
import requests

def fetch_recall_data(make, model, year):
    nhtsa_url = f"https://api.nhtsa.gov/recalls/vehicle/model?make={make}&model={model}&year={year}"
    response = requests.get(nhtsa_url)

    if response.status_code == 200:
        recalls = response.json().get('results', [])
        return recalls
    else:
        return None

def callback(ch, method, properties, body):
    car_data = json.loads(body)
    make, model, year = car_data.get('make'), car_data.get('model'), car_data.get('year')
    print(f" [x] Received request for recalls of '{make} {model} {year}'")

    recalls = fetch_recall_data(make, model, year)

    if recalls:
        print(f" [x] Found {len(recalls)} recalls for {make} {model} {year}")
        for recall in recalls:
            print(f" - {recall['Summary']}")
    else:
        print(f" No recalls found for {make} {model} {year}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='car_recalls')

channel.basic_consume(queue='car_recalls', on_message_callback=callback, auto_ack=True)

print(' Waiting for car recall requests. To exit press CTRL+C')
channel.start_consuming()
