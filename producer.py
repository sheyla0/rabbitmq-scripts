import pika
import json 

def send_car_model_to_queue(make, model, year):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='car_recalls')

    message = json.dumps({"make": make, "model":model, "year":year})
    channel.basic_publish(exchange='', routing_key='car_recalls', body=message)

    print(f" Sent car data '{make} {model} {year}' to queue")
    connection.close()

make = input("Enter the car make (e.g., 'Hyundai'): ")
model = input("Enter the car model (e.g., 'Kona'): ")
year = input("Enter the car year (e.g., '2020'): ")

send_car_model_to_queue(make, model, year)
