import pika
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

    def callback(ch, method, properties, body):
        contact_id = body.decode('utf-8')
        contact = Contact.objects.get(id=contact_id)
        
        # Імітація функції-заглушки для надсилання email
        print(f"Email sent to {contact.email}")

        # Позначаємо, що повідомлення надіслано
        contact.sent_email = True
        contact.save()

    channel.basic_consume(queue='contacts_queue', on_message_callback=callback, auto_ack=True)

    print('Consumer почав очікування повідомлень з черги...')
    channel.start_consuming()

if __name__ == '__main__':
    main()