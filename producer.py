import sys
import pika
from faker import Faker
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect("my_database", host="mongodb+srv://MYNAME:PASSWORD@cluster0.ct1p0gg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Підключення до RabbitMQ
def main(host='localhost', port=5672, username='guest', password='guest'):
    # Підключення до RabbitMQ
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Створення черги
    channel.queue_declare(queue='contacts_queue')

    # Генерування фейкових контактів та запис у базу даних
    fake = Faker()
    for _ in range(10):  # Генеруємо 10 контактів
        full_name = fake.name()
        email = fake.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()

        # Надсилання повідомлення до черги RabbitMQ
        channel.basic_publish(exchange='', routing_key='contacts_queue', body=str(contact.id))

    print("Фейкові контакти створені та надіслані до черги")

    connection.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(host=sys.argv[1], port=int(sys.argv[2]), username=sys.argv[3], password=sys.argv[4])
    else:
        main()