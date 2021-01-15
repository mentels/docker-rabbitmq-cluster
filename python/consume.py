import pika
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--vhost", help="Virtual host", default="/")
parser.add_argument("--queue", help="Queue name", required=True)
parser.add_argument('--manual-ack', help="Whether to turn on auto acknowledgments",
                    default=False, action='store_true')
args = parser.parse_args()

conn_params = pika.ConnectionParameters('localhost', 5672, args.vhost)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()


def callback(ch, method, properties, body):
    if args.manual_ack:
        channel.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Received %r" % body)


channel.queue_declare(args.queue)

channel.basic_consume(
    queue=args.queue, on_message_callback=callback, auto_ack=not args.manual_ack)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
