import json

import pika
import app


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    first_song_id = message["FirstSongId"]
    second_song_id = message["SecondSongId"]
    recommendation = app.song_recommender(first_song_id, second_song_id)

    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(
        pika.URLParameters('amqps://pfbmrmpp:hVkZYh8JRSAssyUzcyjWwFcS_tFg0o4h@rat.rmq2.cloudamqp.com/pfbmrmpp'))
    channel = connection.channel()

    # Опубликовать результат рекомендации в новую очередь
    channel.queue_declare(queue='QueueResponse')  # Создать очередь, если ее нет
    channel.basic_publish(exchange='', routing_key='QueueResponse', body=recommendation.to_json(orient='records'))

    # Закрыть соединение
    connection.close()


def consume():
    try:
        connection = pika.BlockingConnection(pika.URLParameters('amqps://pfbmrmpp:hVkZYh8JRSAssyUzcyjWwFcS_tFg0o4h@rat.rmq2.cloudamqp.com/pfbmrmpp'))
        channel = connection.channel()

        channel.queue_declare(queue='QueueRequest')

        channel.basic_consume(queue='QueueRequest', on_message_callback=callback, auto_ack=True)


        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        connection.close()
