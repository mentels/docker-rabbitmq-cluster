import pika
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--queue", help="Queue name", required=True)
args = parser.parse_args()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.queue_declare(args.queue)

channel.basic_consume(
    queue=args.queue, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
